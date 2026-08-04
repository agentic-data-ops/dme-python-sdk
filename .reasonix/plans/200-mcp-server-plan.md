# Plan: 200-mcp-server-plan（v2：独立项目 dme-mcp-server）

将 MCP Server 从「修改 dme-python-sdk 的 cli.py」改为**独立 Python 项目**实现：新建 `/home/g00ahui/workspace/dme-mcp-server`，以 `dme-python-sdk`（git 依赖）为唯一业务依赖，独立实现 docstring 解析、MCP tool 注册、黑名单控制与 server 启动。

## Objective

1. 新项目 `dme-mcp-server`（pyproject `name = "dme-mcp-server"`，命令行入口 `dme-mcp-server`），核心文件 `server.py`。
2. 依赖 `dme-python-sdk`：`pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git`（与 SDK 的 git origin `agentic-data-ops/dme-python-sdk` 一致）；DME 连接命令行入参参考 SDK 的 `cli.py`。
3. 采用 **MCP V1**（`mcp>=1.28,<2`，实测 1.29.0），FastMCP + Starlette。
4. **每个 actions module 独立路径、共享 endpoint**，端点格式 `<endpoint>/mcp/v1/<module>`（如 `http://127.0.0.1:8000/mcp/v1/san`）。
5. 独立的函数注释解析器：把 action 函数的 docstring 转换为 tool 的 `description` / `inputSchema` / `outputSchema`。
6. 每个 tool 添加 annotation：`topic`、`subtopic`、`action`。
7. 黑名单控制机制参考 `cli.py`（用户目录覆盖 + 包默认回退 + `--accept-risk`/`DME_ACCEPT_RISK`）。

## Background（关键实测事实，mcp 1.29.0 / v1 线）

- `FastMCP.add_tool(fn, name=, title=, description=, annotations=, icons=, meta=, structured_output=)`：`meta` dict 完整透传到 `tools/list` 返回的 Tool（实测 `{"topic":"san","subtopic":"lun","action":"list"}` 原样保留）；`structured_output` 控制 outputSchema。
- **docstring 不参与 schema 生成**：v1 不解析 docstring（`description = description or fn.__doc__`），参数描述只能经 `Annotated[type, Field(description=...)]` 注入 inputSchema（实测有效）；`client` 参数若不去除会原样暴露且 `required`（实测）。
- **outputSchema**：由返回注解 + `structured_output=True` 驱动，需为可序列化的 pydantic model；`-> dict` + structured_output 会抛 `InvalidSignature`（实测）。docstring 的 Returns 文本不会自动进 outputSchema。
- 因此「Returns 注释 → outputSchema」必须**独立解析 Returns 文本 → 动态构造 pydantic model → 作为 wrapper 返回注解**（实测可生成字段级 outputSchema：`properties` 含类型与 description，`additionalProperties: true` 兜底）。
- 多 server 聚合：FastMCP v1 无 `mount()`；官方方式为 Starlette `Mount(prefix, app=sub.streamable_http_app())`。子 server 设 `streamable_http_path="/"` 时，Mount 前缀即完整端点路径。
- 运行配置：`FastMCP(name, host=, port=, streamable_http_path=)`（默认 `127.0.0.1:8000`，路径 `/mcp`）；环境变量前缀 `FASTMCP_`；`run()` 无 host/port，streamable-http 用 `uvicorn.run(app, host, port)` 托管。
- SDK 打包：`dme-python-sdk` 的 pyproject 无 package-data 配置，git 安装的 wheel **很可能不含 `pydme/config/blacklist.json`**——黑名单模块必须做三级来源回退（见 Blacklist 节）。

## Architecture

```
dme-mcp-server (命令行: dme-mcp-server --mcp-server 0.0.0.0:8000 --endpoint ... )
        │
        ▼  main()
  ├─ argparse：DME 连接参数（参考 cli.py）+ --mcp-server / --mcp-transport / --accept-risk
  ├─ DMEAPIClient 初始化 + login（共享单实例）
  ├─ 模块发现：pkgutil 扫描 pydme.actions → 16 个 topic
  └─ streamable-http（默认）
        │
        ▼
  ┌──────────────────────────── Starlette app (uvicorn host:port) ────────────────────────────┐
  │  Mount("/mcp/v1/san",  app=san FastMCP ASGI,  streamable_http_path="/")  → /mcp/v1/san    │
  │  Mount("/mcp/v1/nas",  app=nas FastMCP ASGI,  streamable_http_path="/")  → /mcp/v1/nas    │
  │  Mount("/mcp/v1/storage", ...)  → /mcp/v1/storage       （共 16 个 module 子 server）       │
  └───────────────────────────────────────────────────────────────────────────────────────────┘
        │ 每个子 server 注册本 module 全部 action：
        ▼
  wrapper(**kwargs) → func(shared_client, **kwargs)
        │  meta={"topic","subtopic","action"}；黑名单守卫；结构化输出经动态 model 校验
        ▼
  DME REST API
```

- **stdio**（`--mcp-transport stdio`）：无 URL 前缀概念，单个 FastMCP 注册全部 topic（tool 名带 topic 前缀唯一），`run("stdio")`；`--mcp-server` 仅作启动开关。

## Design

### CLI 参数（参考 cli.py）

```python
# DME 连接（与 cli.py 一致，含环境变量默认值）
--endpoint/-e (DME_API_ENDPOINT)   --user/-u (DME_API_USERNAME)
--password/-p (DME_API_PASSWORD)   --token (DME_API_AUTH_TOKEN)
--timeout (默认 90)                --no-cache-auth-token
--accept-risk                      # 黑名单放行开关（同 cli.py 语义）

# MCP server
--mcp-server      # 监听地址 host:port；默认 os.environ.get('DME_MCP_SERVER')
--mcp-transport   # choices=['streamable-http','stdio']，默认 'streamable-http'
```

校验：无 `--token` 且无完整 endpoint/user/password → 报错退出（同 cli.py）。`--mcp-server` 解析兼容 IPv6（`[::1]:8000`）。

### 模块发现与 action 收集

独立实现（不 import cli.py）：
- `discover_topics()`：`pkgutil.iter_modules` 扫描 `pydme.actions` 包目录，跳过 `_` 前缀。
- `get_topic_actions(topic)`：遍历 module `ACTIONS`，跳过无 `func` 的子主题声明；若存在 `module` 字段则展开子模块（参考 cli.py 逻辑，当前 16 个 module 均无此字段，纯兼容）。
- 每个 action 记录 `{func, subtopic, description, action_key}`；`action` 名 = `action_key` 剥离 `subtopic` 前缀（`subtopic ` 空格 / `subtopic_` 下划线，参考 cli.py）。

### 独立 docstring 解析器（docstring_parser.py）

不依赖 cli.py 的 `parse_docstring`，按同一规则重写并扩展：

```python
def parse_docstring(doc: str) -> dict:
    """返回 {description, params: {name: desc}, returns: str}。
    参考 cli.py 规则：Args 前为描述；Args 内解析 'name: desc'（
    跟踪 '参数格式如下：[{' / '属性格式如下：{' 花括号嵌套深度，
    嵌套块内容归入当前参数描述，不误判为新参数）；Returns 起
    到 Raises/Note/Example 前为返回说明。"""

def parse_returns_fields(returns_text: str) -> list[tuple[str, str, str]]:
    """启发式解析 Returns 顶层字段 → [(name, type_hint, desc)]。
    顶层判定：跟踪 { } [ ] 深度（'参数格式如下：' 进入嵌套块）；
    字段行匹配 r'^\s*(\w+):\s*([^(,{]*?)(?:\(([^)]*)\))?[,。]?\s*$'。
    例：'count: LUN数量 (int32),' → ('count','int32','LUN数量')。"""

TYPE_MAP = {'int32':'integer','int64':'integer','int':'integer',
            'string':'string','char':'string','boolean':'boolean','bool':'boolean',
            'double':'number','float':'number'}   # List<X> → array（items 按 X 映射）

def build_output_model(fields) -> pydantic.BaseModel | None:
    """fields 非空时 create_model：字段 Optional、默认 None、
    ConfigDict(extra='allow')（容忍真实返回多字段）；返回 None 表示无结构化输出。"""
```

### Tool 注册（server.py 核心）

```python
def register_action(mcp, topic, action_key, info, client, risky):
    func, subtopic = info['func'], info.get('subtopic')
    action = strip_subtopic_prefix(action_key, subtopic)
    parsed = parse_docstring(inspect.getdoc(func) or '')
    output_model = build_output_model(parse_returns_fields(parsed['returns']))

    # 1) 参数：剔除 client，其余注入 Field(description)（多行描述原样保留）
    new_params = []
    for name, p in inspect.signature(func).parameters.items():
        if name == 'client':
            continue
        ann = p.annotation if p.annotation is not inspect.Parameter.empty else Any
        if pdesc := parsed['params'].get(name):
            ann = Annotated[ann, Field(description=pdesc)]
        new_params.append(p.replace(annotation=ann))

    # 2) wrapper：闭包注入 client；黑名单守卫；结构化输出
    def wrapper(**kwargs):
        if risky and not accept_risk_enabled():
            return {'error': f'高风险操作已拒绝：{topic} {action_key}'
                             '（--accept-risk 或 DME_ACCEPT_RISK=true 可放行）',
                    'code': 'RISK_BLOCKED'}
        result = func(client, **kwargs)
        if output_model is not None:
            return output_model(**result) if isinstance(result, dict) else result
        return result

    tool_name = f'{topic}.{action_key}'          # 点分命名（官方分组语义）
    wrapper.__signature__ = inspect.signature(func).replace(
        parameters=new_params, return_annotation=output_model or Any)
    wrapper.__annotations__ = {p.name: p.annotation for p in new_params}
    if output_model is not None:
        wrapper.__annotations__['return'] = output_model

    mcp.add_tool(wrapper, name=tool_name,
                 description=parsed['description'] or info.get('description', ''),
                 meta={'topic': topic, 'subtopic': subtopic or '', 'action': action},
                 structured_output=output_model is not None)
```

映射到协议：
- `description` ← 解析出的函数描述（干净文本，不含 Args/Returns 段；参数细节已在 schema 中，避免 docstring 全文进 description 的 token 浪费）
- `inputSchema` ← 签名 + `Annotated Field` 参数描述（无 `client` 字段）
- `outputSchema` ← Returns 解析出的动态 model（`structured_output=True`）
- annotation ← `meta={'topic','subtopic','action'}`

### 黑名单控制（blacklist.py，参考 cli.py）

```python
def load_blacklist() -> dict:
    """三级回退：
    1) ~/.config/pydme/blacklist.json（用户覆盖，权威）
    2) importlib.resources.files('pydme.config').joinpath('blacklist.json')（SDK 若打包）
    3) 基于 pydme.__file__ 的 config/blacklist.json（源码/本地安装）
    全部失败 → 打印警告返回 {}（同 cli.py 行为，不阻断启动）"""

def is_risky(blacklist, topic, action_key) -> bool
def accept_risk_enabled(args=None) -> bool   # --accept-risk 或 DME_ACCEPT_RISK in true/1/yes
```

注册时计算 `risky = is_risky(...)`（每个 action 一次），运行时 wrapper 只查 `accept_risk_enabled()`；命中返回结构化错误而非 `sys.exit`（MCP 调用无交互）。

### 端点与启动（run_mcp_server）

```python
def run_mcp_server(args, client):
    topics = discover_topics()
    if args.mcp_transport == 'stdio':
        mcp = FastMCP('dme')
        for topic in topics:
            register_topic(mcp, topic, client, args)
        mcp.run(transport='stdio')
        return
    host, port = parse_host_port(args.mcp_server)
    routes = []
    for topic in topics:
        sub = FastMCP(f'dme-{topic}', streamable_http_path='/')   # 端点 = Mount 前缀
        register_topic(sub, topic, client, args)
        routes.append(Mount(f'/mcp/v1/{topic}', app=sub.streamable_http_app()))
    app = Starlette(routes=routes)
    uvicorn.run(app, host=host, port=port, log_level='info')
```

客户端连接：`http://host:port/mcp/v1/san`、`/mcp/v1/nas`、…（每 module 独立 endpoint、共享端口）。

### 文件结构

```
/home/g00ahui/workspace/dme-mcp-server/
├── pyproject.toml
├── README.md
└── dme_mcp_server/
    ├── __init__.py
    ├── server.py            # main()、argparse、client 初始化、模块发现、tool 注册、路由
    ├── docstring_parser.py  # 独立 docstring 解析 + Returns→outputSchema model
    └── blacklist.py         # 黑名单加载与风险判定（参考 cli.py）
```

## Implementation steps

1. **pyproject.toml**：`name = "dme-mcp-server"`，`[project.scripts] dme-mcp-server = "dme_mcp_server.server:main"`，依赖 `mcp>=1.28,<2` 与 `dme-python-sdk @ git+https://github.com/agentic-data-ops/dme-python-sdk.git`，`requires-python = ">=3.10"`。
   **注意**：仓库名是 dme-python-sdk，但安装后的包名为 **pydme**，依赖须写作 `pydme @ git+...`（实测 `dme-python-sdk @ git+...` 因 metadata name 不匹配无法安装）。
2. **docstring_parser.py**：实现 `parse_docstring` / `parse_returns_fields` / `build_output_model`（含 `TYPE_MAP`、嵌套深度跟踪、extra='allow'）。
3. **blacklist.py**：实现三级回退加载与 `is_risky` / `accept_risk_enabled`。
4. **server.py**：argparse（参考 cli.py 参数 + `--mcp-server`/`--mcp-transport`/`--accept-risk`）、`discover_topics`/`get_topic_actions`、`register_action`/`register_topic`、`run_mcp_server`（Starlette Mount 路由 + lifespan）。
5. **验证**（见下）。

## 实现过程中的关键发现（已实测解决）

1. **SDK 中 `def list` 遮蔽 builtins.list**：`fcswitch.py`/`storage.py` 定义了 `def list(client: DMEAPIClient, ...)`，使同模块内 `x: list` 注解绑定为**函数对象**——pydantic 生成 Callable schema 并递归其签名（含 `client`），注册即崩（`PydanticInvalidForJsonSchema: IsInstanceSchema DMEAPIClient`）。修复：`make_wrapper` 中 `_is_json_schema_type()` 检查，非 JSON 可序列化注解（函数等）回退 `Any`。
2. **挂载禁内置 lifespan**：`Mount(...)` 挂载子 server 后首请求报 `RuntimeError: Task group is not initialized`——宿主必须用 `AsyncExitStack` 进入每个子 server 的 `session_manager.run()`（`Starlette(routes, lifespan=...)`）。
3. **mcp 1.29 客户端行为**：`ClientSession.__aenter__` **不自动 initialize**（须手动 `await session.initialize()`）；`list_tools()` 返回 `ListToolsResult`（`.tools` 属性），非裸列表；服务端对未 initialize 的请求返回 400。
4. **outputSchema 设计**：`-> dict` + `structured_output=True` 抛 `InvalidSignature`；必须用 Returns 解析出的动态 pydantic model 作为 wrapper 返回注解（实测字段级 outputSchema + `additionalProperties: true` 兜底）。
5. **黑名单守卫时机**：wrapper 参数校验（pydantic）先于函数体执行——高风险 action 用空参数调用时返回的是校验错误而非 RISK_BLOCKED；带必填参数调用时守卫生效（不执行函数、无副作用，安全无漏洞）。

## Files touched

| File | Change |
|------|--------|
| `/home/g00ahui/workspace/dme-mcp-server/pyproject.toml` | 新建（项目名 dme-mcp-server、entry point dme-mcp-server） |
| `/home/g00ahui/workspace/dme-mcp-server/dme_mcp_server/docstring_parser.py` | 新建：独立注释解析 + outputSchema model |
| `/home/g00ahui/workspace/dme-mcp-server/dme_mcp_server/blacklist.py` | 新建：黑名单三级回退 + 风险判定 |
| `/home/g00ahui/workspace/dme-mcp-server/dme_mcp_server/server.py` | 新建：入口与 MCP server 全部实现 |
| `/home/g00ahui/workspace/dme-mcp-server/dme_mcp_server/__init__.py`、`README.md` | 新建 |
| `dme-python-sdk` | **不改动**（仅作为 git 依赖被安装） |

## Risks & considerations

1. **MCP 版本**：`mcp>=1.28,<2` 必须显式 pin；PyPI 最新 2.0.0 是重构版（FastMCP→MCPServer）。本地验证用 venv 装 1.29.0（已实测）。
2. **outputSchema 启发式解析**：Returns 文本非标准 JSON Schema，字段级解析为尽力而为；解析不到字段时回退 `output_model=None`（`structured_output=False`，outputSchema 缺省），保证 427 个 action 全部可注册、不因解析失败崩溃。动态 model 用 `extra='allow'` + Optional 字段，容忍真实返回与注释不一致。
3. **黑名单缺失**：SDK wheel 可能不含 `blacklist.json`（无 package-data 配置）——三级回退 + 空黑名单警告，不阻断启动；用户可在 `~/.config/pydme/blacklist.json` 自建。
4. **`client` 暴露**：wrapper 剔除 + `__signature__`/`__annotations__` 覆盖是硬性要求（实测不剔除会 required）。
5. **多端点**：streamable-http 下每 module 一个 endpoint（`/mcp/v1/<module>`），客户端按需连接；stdio 单端点全量。
6. **token 过期**：`DMEAPIClient` 内部 session 超时自动重登，运行期无需处理。
7. **description 精简**：只放解析出的函数描述（不含 Args/Returns 段），控制注入 token 量；参数描述在 inputSchema，返回结构在 outputSchema。
8. **本地开发**：`pip install -e .` 前先 `pip install -e /path/to/dme-python-sdk`（git URL 用于发行安装）。

## Verification

```bash
# 0) 本地开发安装（venv 已含 mcp 1.29 + SDK -e）
cd /home/g00ahui/workspace/dme-mcp-server
.venv/bin/pip install -e .

# 1) 语法与导入
.venv/bin/python -m py_compile dme_mcp_server/*.py
.venv/bin/python -c "from dme_mcp_server.server import main; from dme_mcp_server.docstring_parser import parse_docstring; print('ok')"

# 2) 启动（streamable-http，无 DME 连接时用假 endpoint 验证注册不依赖登录）
DME_MCP_SERVER=127.0.0.1:8123 DME_API_ENDPOINT=https://127.0.0.1:9999 \
  .venv/bin/python -m dme_mcp_server.server &   # 或用 dme-mcp-server

# 3) 端点探活（应非 404）
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8123/mcp/v1/san
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8123/mcp/v1/nas

# 4) 客户端断言（mcp v1 streamable-http client）：
#    - san.lun.list 存在；inputSchema 无 'client'
#    - meta == {'topic':'san','subtopic':'lun','action':'list'}
#    - description 无 'Args:'/'Returns:' 段
#    - outputSchema.properties 非空（Returns 解析成功）
#    - 高风险 action（如黑名单中的）调用返回 {'code':'RISK_BLOCKED'}

# 5) stdio 冒烟
printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}' \
  | .venv/bin/python -m dme_mcp_server.server --mcp-server x --mcp-transport stdio \
      --endpoint ... --user ... --password ...
```

---

*Plan generated: 2026-08-03（v2：独立项目 dme-mcp-server，MCP V1，端点 /mcp/v1/<module>）*
