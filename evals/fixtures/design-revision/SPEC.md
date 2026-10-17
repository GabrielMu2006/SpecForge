# 阅读摘录工具

Status: Ready for implementation
Current assignment: specification and design-plan revision only

当前文件：本文件拥有产品规则；[旧界面方案](UI-PLAN-OLD.md) 拥有现行视觉要求；[验收记录](ACCEPTANCE.md) 保存实际证据。

### R-001 — 审核摘录关系

用户看原文证据后自行确认关系，不显示真假或可信度评分。日期来自真实保存记录。

### R-002 — 界面

现行方向为深色工作台，包含摘录列表、原文对照和关系审核。

| ID | Goal | Requirements | Depends on | Done when | Status |
| --- | --- | --- | --- | --- | --- |
| T-001 | 关系审核 | R-001 | None | 原文与用户确认可用 | Complete |
| T-002 | 深色界面 | R-002 | T-001 | 当前深色方案验收通过，证据见验收记录 | Complete |
