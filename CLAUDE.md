# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## 项目定位

跨学科科研项目，核心工作为论文写作。所有论文使用 Elsevier **els-cas-templates** 模版。

## 语言偏好

始终使用中文与用户交流。论文内容根据目标期刊/会议要求使用对应语言。

## 目录结构

```
paper/
├── els-cas-templates/       # 模版源（不可直接修改，作为新论文的蓝本）
│   ├── cas-sc.cls           # 单栏文档类
│   ├── cas-dc.cls           # 双栏文档类
│   ├── cas-common.sty       # 公共样式
│   ├── cas-model2-names.bst # 参考文献格式
│   ├── figs/                # 模板自带图片
│   └── doc/                 # 模板文档
├── my-paper/                # 当前论文（示例）
└── <新论文文件夹>/           # 每篇论文独立一个文件夹
experiments/                 # 实验脚本
data/                        # 数据文件
notebooks/                   # 临时探索性分析
references/                  # 文献笔记
```

## 论文写作工作流

### 开新论文

1. 复制 `paper/els-cas-templates/` 到 `paper/<论文名>/`
2. 只保留必要文件（.cls、.sty、.bst），删除示例文件
3. 根据目标期刊选择文档类：
   - `\documentclass[a4paper,fleqn]{cas-sc}` — 单栏
   - `\documentclass[a4paper,fleqn]{cas-dc}` — 双栏
4. 使用 `\bibliographystyle{cas-model2-names}` 处理参考文献
5. 参考文献统一用 `.bib` 文件管理

### 编译流程

```bash
cd paper/<论文名>
pdflatex -shell-escape <文件名>
bibtex <文件名>
pdflatex -shell-escape <文件名>
pdflatex -shell-escape <文件名>
```

### 论文内容规范

- 标题：`\title[mode = title]{...}`
- 作者信息：使用 `\author[]{}` + `\affiliation[]{}` + `\ead{}`
- 关键词：`\begin{keywords}...\sep...\end{keywords}`
- 研究亮点：`\begin{highlights} \item ... \end{highlights}`
- 表格使用 `booktabs` 样式（`\toprule`、`\midrule`、`\bottomrule`）
- 图片放在论文文件夹内的 `figs/` 目录

### 论文结构（建议）

1. Introduction
2. Problem Formulation / Related Work
3. Methodology
4. Results and Discussion
5. Conclusion
6. Acknowledgments
7. References (BibTeX)

## 组织原则

- 保持项目根目录整洁，文件按用途归类到子目录
- 每篇论文独立一个文件夹在 `paper/` 下
- 新工具/脚本先确认存放位置再创建
- 不要直接修改 `els-cas-templates/`，它作为干净的模版源保留
