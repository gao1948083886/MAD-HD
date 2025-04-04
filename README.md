# MAD-HD: Multi-Agent Debate-Driven Ungrounded Hallucination Detection

**We are working on releasing the code and datasets**

## Introduction
Python implementation of our paper: [MAD-HD: Multi-Agent Debate-Driven Ungrounded Hallucination Detection].

We propose a Multi-Agent Debate framework based on Qwen2.5-Instruct series(7B, 14B, 32B, and 72B), and Llama-3.1-Instruct series (8B and 70B) to effectively detect hallucinations.
=======

# MAD-HD: Multi-Agent Debate-Driven Ungrounded Hallucination Detection
MAD-HD 是一种基于多智能体辩论机制的无根据幻觉检测框架。该方法通过多轮辩论，使多个智能体在每轮中更新其判断和理由，最终通过投票达成共识。我们在四个公共数据集上评估了该方法，平均 F1 分数相比现有最先进的方法提高了约 2.6%。

## 项目结构
```
MAD-HD/
├── configs/
│   ├── aoai_config.json/
├── data_process/
│   ├── FactCC503.py/  
├── modules/
│   ├── data
│   ├── eval
│   ├── utils
│   └── ...
├── test_suite/
│   ├── FactCC503
│   └── ...
├── README.md
└── requirements.txt
```

## 安装依赖
在开始之前，请确保你已经安装了 Python 和必要的依赖库。你可以通过以下命令安装所有依赖项：
```bash
pip install -r requirements.txt
```

## 数据准备
数据集已经在test_suite文件夹中准备好。

## 运行代码
你可以通过以下命令运行主程序：
首先配置configs里的文件，随后配置run_detection.sh里的参数，最后运行：bash run_detection.sh


## 参数说明
- `--dataset`: 数据集名称（如 `FactCC503`、`SummEval` 等）。
- `--model`: 使用的模型名称（如 `Qwen2.5-72B-Instruct`、`Llama-3.1-70B-Instruct` 等）。
- `--agents`: 智能体数量（如 `3`）。
- `--rounds`: 辩论轮数（如 `3`）。

## 实验结果
我们在四个基准数据集上进行了实验，以下是主要结果：

+----------------------+-----------------------+-----------------------+-----------------------+-----------------------+
|                      |       FactCC503       |        SummEval       |       QAGS-CNNDM      |        QAGS-XSUM      |
+----------------------+-----------------------+-----------------------+-----------------------+-----------------------+
| Method               |   F1  | N-Hal |  Hal  |   F1  | N-Hal |  Hal  |   F1  | N-Hal |  Hal  |   F1  | N-Hal |  Hal  |
+----------------------+-----------------------+-----------------------+-----------------------+-----------------------+
| FactCC               | 0.706 | 0.919 | 0.493 | 0.641 | 0.819 | 0.462 | 0.688 | 0.664 | 0.712 | 0.644 | 0.635 | 0.653 |
| FactCC(Oracle)       | 0.710 | 0.923 | 0.496 | 0.651 | 0.833 | 0.468 | 0.689 | 0.678 | 0.700 | 0.649 | 0.653 | 0.644 |
| AlignScore-L         | 0.820 | 0.952 | 0.687 | 0.656 | 0.917 | 0.395 | 0.549 | 0.701 | 0.397 | 0.723 | 0.760 | 0.686 |
| AlignScore-L(Oracle) | 0.765 | 0.923 | 0.606 | 0.753 | 0.919 | 0.586 | **0.829** | 0.837 | **0.821** | 0.745 | 0.755 | 0.734 |
| CoNLI(SOTA Method)   | 0.876 | 0.971 | 0.780 | 0.784 | 0.935 | 0.632 | 0.799 | 0.814 | 0.783 | 0.812 | **0.819** | 0.804 |
| MAD-HD-Llama         | 0.881 | 0.972 | 0.790 | 0.789 | 0.935 | **0.642** | 0.788 | 0.805 | 0.770 | 0.797 | 0.812 | 0.782 |
| MAD-HD-Qwen          | **0.903** | **0.979** | **0.826** | **0.810** | **0.943** | 0.676 | 0.823 | **0.839** | 0.807 | **0.819** | 0.816 | **0.821**|
+----------------------+-----------------------+-----------------------+-----------------------+-----------------------+

---
