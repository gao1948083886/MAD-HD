#!/bin/bash

# 定义可配置的参数
model_name="glm4"
dataset="qags_xsum"  # qags_xsum, qags_cnndm, summeval
task_name="3_agents_2_rounds"  # single, 3_agents_2_rounds

# 运行脚本
python run_hallucination_sentence_gt_evaluator.py \
    --gtfile ./test_suite/${dataset}/${dataset}_raw_response.tsv \
    --hd_result_folder ./result/${model_name}_output/${dataset}/${task_name}/intermediate \
    --output_folder ./result/${model_name}_output/${dataset}/${task_name} \

#    "gtfile": "./data/qags_xsum/qags_xsum_raw_response.tsv",  # 地面真实数据的 TSV 文件路径
#    "hd_result_folder": "../gsm/hallucination_detect_result",  # 幻觉检测结果的输出文件夹路径
#    "filter": "",  # 额外的过滤条件，格式为 "列名=值"（例如 "Severity=critical"）
#    "output_folder": "../gsm/hallucination_detect_result",  # 分析结果的输出文件夹路径

