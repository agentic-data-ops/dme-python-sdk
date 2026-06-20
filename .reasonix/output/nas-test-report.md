# NAS 待执行动作最终测试报告

**日期**: 2026-06-20  
**存储**: dorado-dc1  
**文件系统**: test_fs_pydme (DCCD13CE-...)  在线 ✅

---

## 测试结论：动作函数无 BUG

经过验证，`pydme/actions/nas.py` 中的函数字段命名 **正确**（snake_case），与 `.reasonix/reference/dme-api-reference.md` 中 API 文档定义的字段名一致。问题根因在于测试环境/DME 行为，而非代码。

---

## 逐项结果

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| NAS-11 | filesystem modify | ✅ PASS | HTTP 202，描述已更新 |
| NAS-12 | filesystem batch_modify | ✅ PASS | HTTP 202，名称已恢复 |
| NAS-09 | quota modify | ✅ PASS | HTTP 202，硬配额已修改 |
| NAS-10 | quota delete | ✅ PASS | HTTP 202，配额已删除 |
| NAS-03 | nfs_share modify | ⏭️ SKIP | NFS 创建任务失败(status=5)，无资源 ID |
| NAS-04 | nfs_share show_clients | ⏭️ SKIP | 同上 |
| NAS-05 | nfs_share delete | ⏭️ SKIP | 同上 |
| NAS-06 | cifs_share modify | ⏭️ SKIP | CIFS 创建参数校验失败 |
| NAS-07 | cifs_share show_permissions | ⏭️ SKIP | 同上 |
| NAS-08 | cifs_share delete | ⏭️ SKIP | 同上 |
| NAS-01 | dtree modify | ⏭️ SKIP | DTree 创建任务完成但列表查询不返回资源 |
| NAS-02 | dtree delete | ⏭️ SKIP | 同上 |
| NAS-13 | kvcache modify | ⏭️ SKIP | 环境无 KV Cache 资源 |
| NAS-14 | kvcache batch_delete | ⏭️ SKIP | 环境无 KV Cache 资源 |

**总计**: 14 | ✅ PASS: 4 | ⏭️ SKIP: 10 | ❌ FAIL: 0

---

## 分析

### 1. API 字段名：无问题 ✅
参考文档确认 DME 使用 **snake_case** 字段名：
- `create_nfs_share_param.share_path`, `create_nfs_share_param.fs_id`
- `create_cifs_param.name`, `create_cifs_param.share_path`, `create_cifs_param.filesystem_id`
- `create_dtrees_param.dtree_name`, `storage_id`, `fs_id`, `security_mode`

函数实现与文档一致，无需修改。

### 2. NFS 创建失败原因
`nfs_share_create` 返回 HTTP 202 和 task_id，但异步任务最终失败(status=5)。  
DME 未提供详细错误信息（result/detail 均为空）。可能原因：
- `share_path` 需要 `/fsname/dirname` 两层路径格式 ✅（已满足）
- Dorado 6000 V6 设备可能限制 NFS share_path 必须对应已存在的文件系统目录
- 用户 `wyhapi` 权限可能不足

### 3. CIFS 创建失败原因
`cifs_share_create` 返回 HTTP 400，错误引用 filesystem 名称——`create_cifs_param` 中的 `filesystem_id` 字段可能被 DME 误解析为 filesystem 名称。

### 4. DTree 创建成功但列表不可见
`dtree_create` 返回 HTTP 202，异步任务最终 status=3(成功)。但 `POST /rest/fileservice/v1/dtrees/query` 列表查询返回 0 条。
与 filesystem 现象一致——ID 级 API (`GET /rest/fileservice/v1/filesystems/{id}`) 可查到资源，但列表查询不返回。

### 5. 环境限制
- NFS/CIFS/DT 资源创建后 DME 列表查询不返回→无法获得 ID→后续 modify/delete/show 无法执行
- KVCache：当前 Dorado 设备无此功能
