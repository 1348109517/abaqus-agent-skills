# Abaqus Agent Skills

[English](README.md) · [快速开始](docs/quickstart.md) · [演示指南](docs/demo.md) · [技能选择](docs/skill-selection.md) · [兼容性边界](docs/compatibility.md)

这是一个面向 AI 编码代理的 Abaqus 自动化工作流集合，当前包含 17 个可独立使用的
skills。项目强调输入可追溯、命名一致、先诊断后修改，以及明确区分“求解器完成”和
“工程结论成立”。

## 三分钟快速开始

可运行演示只使用 Python 标准库。它检查一份小型、完全合成的隧道—土体模型契约，
生成确定性的 Markdown 和 JSON 报告；不会安装 Abaqus，也不会运行求解器。

```bash
git clone https://github.com/1348109517/abaqus-agent-skills.git
cd abaqus-agent-skills
python scripts/run_demo.py
```

如果 Windows 检出时报 `Filename too long`，请改在靠近文件系统根目录的短路径下
克隆；详见[兼容性边界](docs/compatibility.md)。

默认命令检查 `complete` 场景，并生成：

```text
build/demo/complete/report.json
build/demo/complete/report.md
```

也可以显式选择三个场景名称：

```bash
python scripts/run_demo.py --scenario complete
python scripts/run_demo.py --scenario naming-drift
python scripts/run_demo.py --scenario evidence-overreach
```

`complete` 场景有 8 项静态检查通过；`naming-drift` 报告未解析的区域引用；
`evidence-overreach` 报告跳过求解器证据或物理审查的工程声明。后两个仍是已完成的
静态审计，虽然包含 `REVIEW_REQUIRED`，仍会以状态码 0 结束。

如需预览技能安装而不复制文件：

```bash
python scripts/install_skill.py abaqus-mesh --target build/install-check
```

安装器默认是 dry-run。只有在审查其打印出的源目录、目标目录和冲突状态后，才添加
`--apply`。

使用下列命令验证代码库：

```bash
python -m unittest discover -s tests -v
```

演示和代码库测试不需要 Abaqus、ODB、许可证或第三方 Python 包。

## 内容

- 项目脚手架、依赖预检、共享命名清单和脚本调试；
- 隧道局部网格拓扑与映射检查；
- 边界条件、荷载、材料、分析步和 ODB 只读检查；
- API 文档核验、几何、网格、接触/约束、初始场、输出和受控导出；
- 双语总览、选择矩阵、示例、贡献规范和自动验证。

## 安装

从 `skills/` 复制所需技能目录到你的代理所识别的 skills 目录，并保留
`SKILL.md` 文件名。仓库不包含 Abaqus 软件、求解器、官方手册、破解内容或工程数据。

请阅读[演示指南](docs/demo.md)，了解契约数据流、报告格式、场景和 finding code；阅读
[架构说明](docs/architecture.md)，了解静态检查、可选求解器证据、物理审查和工程声明
之间的边界。

## 贡献与引用

提交 issue 或 pull request 前请阅读 [CONTRIBUTING](CONTRIBUTING.md)。贡献必须使用合成
或 clean-room 材料，并说明实际检查过哪些证据。如果本项目对你的工作有帮助，请使用
[CITATION.cff](CITATION.cff) 中的元数据引用。

## 验证

```bash
python -m unittest discover -s tests -v
```

验证不需要 Abaqus 许可证。跨 Abaqus/CAE 或嵌入式 Python 版本使用前，请先阅读
[兼容性边界](docs/compatibility.md)。所有工程结论仍需由有资质的人员结合模型、单位、边界、
网格、收敛和现场证据独立审查。

演示只执行静态契约检查。报告通过不表示求解器完成、ODB 已检查、模型具有物理有效性，
也不表示工程声明已获批准。本项目与 Dassault Systemes 或 SIMULIA 无隶属或背书关系。
许可证为 Apache-2.0。参见 [NOTICE](NOTICE)、[CONTRIBUTING](CONTRIBUTING.md) 和
[社区发布指南](docs/community-launch.md)。
