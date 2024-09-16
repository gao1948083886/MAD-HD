#!/bin/bash

# 定义可配置的参数
model_name="qwen72b"  # glm4, qwen72b

dataset="qags_cnndm"  # FactCC503, summeval, qags_cnndm, qags_xsum
task_name="5_agents_1_rounds"  # single, 3_agents_2_rounds

# 定义目录路径
hall_folder="./result/${model_name}_output/${dataset}/${task_name}/hallucinations"
inter_folder="./result/${model_name}_output/${dataset}/${task_name}/intermediate"
logs_folder="./result/${model_name}_output/${dataset}/${task_name}/logs"
mitigation_folder="./result/${model_name}_output/${dataset}/${task_name}/mitigation_result"

# 检查并创建hall_folder
if [ ! -d "$hall_folder" ]; then
    mkdir -p "$hall_folder"
    echo "Directory created: $hall_folder"
else
    echo "Directory already exists: $hall_folder"
fi

# 检查并创建inter_folder
if [ ! -d "$inter_folder" ]; then
    mkdir -p "$inter_folder"
    echo "Directory created: $inter_folder"
else
    echo "Directory already exists: $inter_folder"
fi

# 检查并创建logs_folder
if [ ! -d "$logs_folder" ]; then
    mkdir -p "$logs_folder"
    echo "Directory created: $logs_folder"
else
    echo "Directory already exists: $logs_folder"
fi

# 检查并创建mitigation_folder
if [ ! -d "$mitigation_folder" ]; then
    mkdir -p "$mitigation_folder"
    echo "Directory created: $mitigation_folder"
else
    echo "Directory already exists: $mitigation_folder"
fi


# 使用变量替换原有路径中的硬编码部分
python run_hallucination_detection.py \
    --output_folder ./result/${model_name}_output/${dataset}/${task_name} \
    --input_hypothesis ./test_suite/${dataset}/${dataset}_raw_response.tsv \
    --input_src ./test_suite/${dataset}/src

# 生成指标
python run_hallucination_sentence_gt_evaluator.py \
    --gtfile ./test_suite/${dataset}/${dataset}_raw_response.tsv \
    --hd_result_folder ./result/${model_name}_output/${dataset}/${task_name}/intermediate \
    --output_folder ./result/${model_name}_output/${dataset}/${task_name} \

#    "output_folder": None,  # 必填，无默认值
#    "input_hypothesis": None,  # 必填，无默认值
#    "input_src": None,  # 必填，无默认值
#    "entity_detector_type": "text_analytics",  # 实体检测器类型
#    "sentence_selector_type": "pass_through",  # 句子选择器类型
#    "aoai_config_file": "(Path(__file__).absolute()).parent/'configs'/'aoai_config.json'",  # aoai 端点配置文件路径
#    "aoai_config_setting": "gpt-35-turbo",  # aoai 配置设置
#    "ta_config_file": "(Path(__file__).absolute()).parent/'configs'/'ta_config.json'",  # 文本分析端点配置文件路径
#    "ta_config_setting": "ta-general",  # 文本分析配置设置
#    "max_parallel_data": 2,  # 并行处理的数据最大数量
#    "max_parallelism": 2,  # 每个幻觉检测模块并行发送的 GPT 请求最大数量
#    "entity_detection_parallelism": 2,  # 幻觉检测模块并行处理的实体检测批次最大数量
#    "simple_progress_bar": "True",  # 简化进度条
#    "test_mode": 0,  # 测试模式下的数据数量
#    "gpt_batch_size": 1,  # 每批次的 GPT 请求数量
#    "log_level": "info",  # 日志记录级别
#    "logfile_name": None  # 日志文件名