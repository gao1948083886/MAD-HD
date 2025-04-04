# MAD-HD: Multi-Agent Debate-Driven Ungrounded Hallucination Detection

MAD-HD is a hallucination detection framework based on a multi-agent debate mechanism. This approach involves multiple agents engaging in several rounds of debate, updating their judgments and rationales in each round based on the evolving results of others, ultimately reaching a consensus through voting. We evaluated our method on four public datasets, achieving an average F1 score improvement of approximately 2.6% compared to state-of-the-art methods.

## Project Structure
```
MAD-HD/
├── configs/
│   └── aoai_config.json
├── data_process/
│   └── FactCC503.py
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

### Dependencies Installation
Before you begin, ensure that you have Python and the necessary dependencies installed. You can install all dependencies with the following command:
```bash
pip install -r requirements.txt
```

### Data Preparation
The datasets are already prepared in the `test_suite` folder.

### Running the Code
You can run the main program by following these steps:
1. Configure the files in the `configs` directory.
2. Set the parameters in `run_detection.sh`.
3. Run the following command:
   ```bash
   bash run_detection.sh
   ```
