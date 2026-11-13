# 同一请求中的规格与实现

日期为 2026-11-14。评测对象是工作树中的 SpecForge 0.2.0，包含同一请求先交付规格、再执行获授权且未被阻塞的实现的新增指令。两个案例分别使用新建临时目录与独立的 Codex CLI 0.159.2 会话，启动时指定 `gpt-6.1-sol`。每个会话只收到合成项目输入、同一版运行文件和一条用户请求。评测标准和另一个案例的产物未随请求提供。

| 案例 | 规格与实际写入顺序 | 实现范围与结果 |
| --- | --- | --- |
| 无阻塞 | 首份完整规格和最终规格均为 `Ready for implementation`。完整规格快照先于首次 `clean.py` 变更约 115 毫秒。原始工具事件也记录了规格写入（item_4）在清洗补丁（item_5）前完成。 | 仅实现名单清洗。计数留在 V1 的需求、验收与任务内，`counts.py` 前后字节一致。清洗断言通过。 |
| 部分阻塞 | 首份完整规格和最终规格均为 `Draft`。完整 Draft 先于首次 `clean.py` 变更约 10.714 秒。工具事件中的规格补丁（item_6）在清洗补丁（item_7）前完成。 | 仅实现并验证清洗。待合作方确认的 CSV 表头未被代选，规格将导出和依赖该导出的联调保留在待办中。获授权但被阻塞的 `export.py` 与仅要求写入规格的 `counts.py` 均与输入字节一致。 |

两轮均在同一回复中交付磁盘上的规格。上述顺序以第一次写完可用规格为起点。无阻塞案例曾短暂出现零字节的规格文件，随后写入完整内容。两个案例都在实施和检查后更新了规格里的任务状态与检查记录。两个评测会话均成功结束。无阻塞案例第一次调用 `python` 因命令不存在而退出，随后用 `python3` 成功执行检查。

### 证据

- 无阻塞。[用户请求](2026-11-14-mixed-request/no-blocker/request.txt) · [实施前的完整规格](2026-11-14-mixed-request/no-blocker/versions/02-SPEC.md) · [最终规格](2026-11-14-mixed-request/no-blocker/after/SPEC.md) · [返回文本](2026-11-14-mixed-request/no-blocker/response.txt) · [写入记录](2026-11-14-mixed-request/no-blocker/writes.jsonl) · [原始工具事件](2026-11-14-mixed-request/no-blocker/events.jsonl)
- 部分阻塞。[用户请求](2026-11-14-mixed-request/partial-blocker/request.txt) · [实施前的 Draft](2026-11-14-mixed-request/partial-blocker/versions/01-SPEC.md) · [最终 Draft](2026-11-14-mixed-request/partial-blocker/after/SPEC.md) · [返回文本](2026-11-14-mixed-request/partial-blocker/response.txt) · [写入记录](2026-11-14-mixed-request/partial-blocker/writes.jsonl) · [原始工具事件](2026-11-14-mixed-request/partial-blocker/events.jsonl)
- 目录内保留了每轮实际输入与最终文件、每次观察到的内容变更快照、运行文件及输入的哈希、评测调用参数与最终文件哈希。[独立复核结果](2026-11-14-mixed-request/verification.json) · [复核脚本](2026-11-14-mixed-request/verify.py) · [运行脚本](2026-11-14-mixed-request/run.py)

独立复核逐一对照工具完成事件、约 5 毫秒轮询保存的内容快照和文件修改时间。轮询只能观测采样时的内容，不能保证捕获间隔内所有短暂写入。对每个案例的清洗实现分别执行六组输入断言，并复核首份与最终规格的结构。无阻塞案例均为 2 项需求、2 项任务，部分阻塞案例均为 3 项需求、5 项任务。复核已确认与本轮实现无关的文件哈希一致。

本轮覆盖本机 CLI 的两个显式加载案例，未评测自动路由、其他宿主或 E-01 至 E-18 的访谈行为。
