# NAS 全量覆盖测试最终报告

**测试日期**: 2026-06-20  
**存储**: dorado-dc1 (OceanStor Dorado 6000 V6)  
**文件系统**: fs_nas_test  

## 结果

| 子主题 | 动作 | 状态 | 说明 |
|--------|------|:----:|------|
| **dtree** | create | ✅ PASS | HTTP 202，异步任务成功 |
| | modify | ✅ PASS | HTTP 202，名称修改成功 |
| | delete | ✅ PASS | HTTP 202，删除成功 |
| **nfs_share** | create | ✅ PASS | 路径需为 `/{filesystem}/{dtree}` 格式 |
| | modify | ✅ PASS | description 修改成功 |
| | show_clients | ✅ PASS | HTTP 200，返回客户端列表 |
| | delete | ✅ PASS | HTTP 202，删除成功 |
| **cifs_share** | create | ✅ PASS | fs_id 为顶层参数（非 create_cifs_param 内部） |
| | modify | ✅ PASS | description 修改成功 |
| | show_permissions | ✅ PASS | **已修复**: URL 缺少 `cifs_share_id` 参数 BUG |
| | delete | ✅ PASS | HTTP 202，删除成功 |
| **quota** | create | ✅ PASS | |
| | modify | ✅ PASS | |
| | delete | ✅ PASS | |
| **filesystem** | modify | ✅ PASS | (之前已验证) |
| | batch_modify | ✅ PASS | (之前已验证) |

**总计: 16/16 全部 PASS** ✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅

## 发现并修复的 BUG

### `cifs_share_show_permissions` — URL 路径参数缺失（已修复 🔧）

函数中 3 个子请求的 URL 包含 `{cifs_share_id}` 占位符，但调用 `client.post()` 时未传入 `params={"cifs_share_id": cifs_share_id}`，导致请求发送到字面量 URL（`.../{cifs_share_id}/...`），返回错误。

修复：给 3 个 `client.post()` 调用添加了 `params={"cifs_share_id": cifs_share_id}`，并去除了重复的 `payload = {}` 初始化（不影响功能但冗余）。

### `cifs_share_create` — docstring 误导（已修复 🔧）

`create_cifs_param` 的 docstring 中列出了 `filesystem_id` 和 `storage_id`，但参考文档显示它们不属于内部。`fs_id` 是**顶层参数**。已修正 docstring。

## 核心发现

| 发现 | 详情 |
|------|------|
| **NFS share_path 格式** | `/{filesystem_name}/{dtree_name}` — 先创建 DTree 再共享其路径 |
| **CIFS share_path 格式** | 同上，需要 DTree 路径已存在 |
| **CIFS fs_id 位置** | **顶层参数**，与 `create_cifs_param` 平级 |
| **DTree 提升序** | 创建 DTree → NFS/CIFS 共享 → 最后删除 DTree |
| **create 异步任务** | 均返回 task_id (HTTP 202)，资源 ID 从任务 resources 中提取 |
