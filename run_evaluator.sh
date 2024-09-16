#!/bin/bash

# 定义可配置的参数
model_name="glm4"
dataset="qags_xsum"  # qags_xsum, qags_cnndm, summeval
task_name="single"  # single, 3_agents_2_rounds

# 使用变量替换原有路径中的硬编码部分
python run_hallucination_evaluator.py \
    --hallucinationjsonl ./result/${model_name}_output/${dataset}/${task_name}/hallucinations/allhallucinations.jsonl
