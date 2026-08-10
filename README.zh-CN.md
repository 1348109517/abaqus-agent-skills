# Abaqus Agent Skills

[English](README.md) · [快速开始](docs/quickstart.md) · [技能选择](docs/skill-selection.md)

这是一个面向 AI 编码代理的 Abaqus 自动化工作流集合，首版包含 10 个可独立使用的
skills。项目强调输入可追溯、命名一致、先诊断后修改，以及明确区分“求解器完成”和
“工程结论成立”。

## 内容

- 项目脚手架、依赖预检、共享命名清单和脚本调试；
- 隧道局部网格拓扑与映射检查；
- 边界条件、荷载、材料、分析步和 ODB 只读检查；
- 双语总览、选择矩阵、示例、贡献规范和自动验证。

## 安装

从 `skills/` 复制所需技能目录到你的代理所识别的 skills 目录，并保留
`SKILL.md` 文件名。仓库不包含 Abaqus 软件、求解器、官方手册、破解内容或工程数据。

## 验证

```bash
python -m unittest discover -s tests -v
```

验证不需要 Abaqus 许可证。所有工程结论仍需由有资质的人员结合模型、单位、边界、
网格、收敛和现场证据独立审查。

本项目与 Dassault Systemes 或 SIMULIA 无隶属或背书关系。许可证为 Apache-2.0。
