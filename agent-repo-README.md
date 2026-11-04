# ai-agent-8weeks-roadmap

> 8 周转行 AI Agent 开发高强度冲刺计划 —— 用工程化的方式监督自己：任务拆解为 Issue，进度呈现在 Project 看板，每日提交保持绿墙。

## 项目简介

本仓库记录我从零基础起步、系统学习 AI Agent（智能体）开发的完整过程。学习路线遵循「先跑通、再理解、最后造系统」的原则：不纠缠底层算法推导，聚焦**工程编排与系统设计能力** —— 这是 Agent 应用工程师岗位的核心竞争力。

- **周期**：8 周（Day 1 – Day 56），总计约 200 有效学时（工作日 3h + 周末 5h）
- **主线技术栈**：Python（asyncio / Pydantic）· OpenAI / DeepSeek SDK · ReAct · RAG（Chroma）· MCP 协议 · LangGraph · Langfuse · Eval 评估
- **最终产出**：1 个端到端商业级 Agent 开源项目 + 完整 README、架构图与量化评估报告

## 8 周计划总览

| 周次 | 主题 | 阶段里程碑 |
|------|------|------------|
| Week 1 | Python 进阶、Pydantic、原生 Function Calling | 60 行纯原生 Agent 脚本 |
| Week 2 | ReAct 范式、RAG 检索、上下文裁剪 | 带长上下文防护的 RAG Agent |
| Week 3 | MCP 协议、手写本地 MCP Server | 即插即拔 MCP 工具的 Agent |
| Week 4 | LangGraph 状态机、条件路由、持久化 | 高容错 LangGraph 状态图引擎 |
| Week 5 | 多 Agent 协作、Human-in-the-Loop 审批 | 带审批流的多 Agent 协同框架 |
| Week 6 | Langfuse 可观测性、Eval 评估体系 | 全链路监控与指标评分体系 |
| Week 7 | 端到端毕业项目攻坚 | 商业级 Agent 项目主干完成 |
| Week 8 | 量化压测、开源包装、面试复盘 | 全套求职物料与成熟项目上线 |

> 每周的每日细化任务见配套文件《AI_Agent_8周转行高强度冲刺任务表.xlsx》（详细任务表 + 阶段总览与学时规划）。

## 目录结构

```
ai-agent-8weeks-roadmap/
├── week01_foundations/        # 第 1 周：异步、Pydantic、原生调用
├── week02_rag_react/          # 第 2 周：ReAct 循环、RAG、上下文管理
├── week03_mcp_servers/        # 第 3 周：MCP 协议与本地 Server
├── week04_langgraph_core/     # 第 4 周：LangGraph 状态机
├── week05_multi_agent/        # 第 5 周：多 Agent 与人工审批流
├── week06_eval_observability/ # 第 6 周：链路追踪与 Eval 评估
├── week07_final_project/      # 第 7 周：端到端毕业项目
├── week08_job_hunting/        # 第 8 周：压测、包装、面试复盘
├── .env.example               # 环境变量模板（复制为 .env 后填入自己的 Key）
├── .gitignore                 # 忽略密钥、虚拟环境与缓存（.env 绝不入库）
└── requirements.txt           # Python 依赖清单
```

## 环境准备

```bash
# 1. 克隆仓库
git clone https://github.com/Ccvi03/ai-agent-8weeks-roadmap.git
cd ai-agent-8weeks-roadmap

# 2. 创建虚拟环境并安装依赖
python -m venv .venv
pip install -r requirements.txt

# 3. 配置 API Key（复制模板后填入自己的密钥，切勿提交 .env）
cp .env.example .env
```

## 进度管理方式

- **Issues**：每个 1–2 天的任务是一个 Issue，标题格式 `[Day X] 任务名`，按周归入里程碑 M1–M4
- **Project 看板**：Todo → In Progress → Blocked → Done，每天开工先移动卡片
- **提交规范**：完成任务时用 `git commit -m "feat: ..., close #Issue编号"` 自动关闭对应 Issue
- **每日打卡**：当天目标 / 实际进度 / 有效学时 / 是否达成交付物

## 学习进度

- [ ] Week 1 · 工程打底与原生 API 闭环
- [ ] Week 2 · ReAct 与 RAG
- [ ] Week 3 · MCP 协议与工具生态
- [ ] Week 4 · LangGraph 图编排
- [ ] Week 5 · 多 Agent 与审批流
- [ ] Week 6 · 可观测性与 Eval
- [ ] Week 7 · 毕业项目
- [ ] Week 8 · 包装与求职
