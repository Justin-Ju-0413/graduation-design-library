# Notion Sync: Final Defense Roadmap

## Target

`毕业设计管理中心`

## Section Title

从当前进度到最终答辩 / Final Defense Roadmap

## Description

这张表用于统一管理从 2026-04-28 当前工程状态到最终毕业设计答辩的全部任务。工程、论文和答辩共用同一条证据链：

`RTL_PASS -> full-SoC PASS -> hello_e203 board run -> cnn_accel_demo board evidence -> final defense`

## Database Columns

- 名称
- 状态
- 截止日期
- 优先级
- 任务类型
- 描述

## Rows

| 名称 | 状态 | 截止日期 | 优先级 | 任务类型 | 描述 |
| --- | --- | --- | --- | --- | --- |
| Phase 1 Current Engineering Freeze | 进行中 | 2026年4月30日 | 高 | 工程闭环 | 确认分支、commit、仿真基线、Vivado/JTAG 现状，输出当前状态表、证据索引和风险列表 |
| Phase 2 hello_e203 Board Runtime Closure | 未开始 | 2026年5月5日 | 高 | 上板验证 | 用 hello_e203 验证 E203v2 能从 bitstream 预初始化程序启动，并通过 UART 输出 |
| Phase 3 CNN/NICE Board Validation Closure | 未开始 | 2026年5月12日 | 高 | 加速器验证 | 运行 cnn_accel_demo，收集软件 baseline、硬件输出、结果对比、cycle 计数和 speedup |
| Phase 4 Thesis Main Writing | 未开始 | 2026年5月18日 | 高 | 论文撰写 | 完成 Introduction、Related Work、Architecture、RTL、full-SoC、FPGA bring-up 和 Conclusion |
| Phase 5 Final Defense Package | 未开始 | 2026年5月24日 | 高 | 最终答辩 | 完成最终 PPT、逐页讲稿、QA、证据包和 8-12 分钟彩排版本 |

## Success Rule

如果板级证据还没收集到，就写清楚缺口和下一步，不把它写成已经完成。

