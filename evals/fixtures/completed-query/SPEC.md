# 朋友共同空闲

Status: Ready for implementation

### R-003 — 小组

小组最多 10 人，成员共享忙碌时间，离开后撤销读取权限。

### R-004 — 全员共同空闲

选至少两名成员，返回每人都空闲且达到最短时长的连续区间。缺少成员安排时说明缺失，不把部分人的空闲当全员空闲。

| ID | Goal | Requirements | Depends on | Done when | Status |
| --- | --- | --- | --- | --- | --- |
| T-003 | 小组 | R-003 | None | 成员和权限验收通过 | Complete |
| T-004 | 全员查询 | R-004 | T-003 | 旧 R-004 场景通过，证据为本合成设定中的历史记录 | Complete |
