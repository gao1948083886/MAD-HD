import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import logging
import os
import sys
sys.path.append('..')
from pathlib import Path
import time
from tqdm import tqdm
from CoNLI.modules.arguments import DetectionArguments, create_openai_arguments, create_ta_arguments
from CoNLI.modules.data.data_loader import DataLoader
from CoNLI.modules.entity_detector import EntityDetectorFactory
from CoNLI.modules.sentence_selector import SentenceSelectorFactory
from CoNLI.modules.hallucination_detector import HallucinationDetector
from CoNLI.modules.hd_constants import AllHallucinations, FieldName
from CoNLI.modules.utils.logging_utils import init_logging
from CoNLI.modules.utils.conversion_utils import str2bool

def get_optional_field(hallucination, field_name, default_value = ''):
    if field_name in hallucination:
        return str(hallucination[field_name])
    else:
        return default_value

def get_required_field(hallucination, field_name):
    return str(hallucination[field_name])

def save_hallucinations(hallucinations, output_folder : str):
    hallucination_finalresults = os.path.join(output_folder, 'HallucinationFinal.tsv')
    
    # Sort all of the hallucinations by data and sentence id
    # hallucinations contextual order before passing to requester
    hallucinations = sorted(
            hallucinations,
            key=lambda d: (
                d[FieldName.DATA_ID],
                d[FieldName.SENTENCE_ID],
                d[FieldName.DETECTION_TYPE],
                d[FieldName.SENTENCE_TEXT]
            )
        )
    
    with open(hallucination_finalresults, 'w') as outFinal:
        outFinal.write('data_id\tsentenceid\tdetectiontype\tspan\treason\tname\ttype\n')
    
        required_field_names = [
                        FieldName.DATA_ID,
                        FieldName.SENTENCE_ID,
                        FieldName.DETECTION_TYPE,
                        FieldName.SENTENCE_TEXT,
                        FieldName.REASON
                        ]
        optional_field_names = [
                        FieldName.NAME,
                        FieldName.TYPE
                        ]
        for h in hallucinations:
            field_values = [get_required_field(h, fn) for fn in required_field_names] + [get_optional_field(h, fn) for fn in optional_field_names]
            outFinal.write('\t'.join(field_values) + '\n')

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output_folder',
        required=True,
        help='运行数据的输出文件夹路径',
        type=str)
    parser.add_argument(
        '--input_hypothesis',
        required=True,
        help='存放所有原始响应的文件夹路径; 也可以加载包含以下列的句子级 tsv 文件：DataID, SentenceID, Sentence。Sentence 将作为检测的输入字符串',
        type=str)
    parser.add_argument(
        '--input_src',
        required=True,
        help='存放所有源文档的文件夹路径',
        type=str)
    parser.add_argument(
        '--entity_detector_type',
        default="text_analytics",
        help='实体检测器类型: pass_through, text_analytics。如果是集成类型，必须指定为 ensembled:type1,type2 ...',
        type=str)
    parser.add_argument(
        '--sentence_selector_type',
        default="pass_through",
        help='句子选择器类型: pass_through, None。如果是集成类型，必须指定为 ensembled:type1,type2 ...',
        type=str)
    parser.add_argument(
        '--aoai_config_file',
        default=(Path(__file__).absolute()).parent / "configs" / "aoai_config.json",
        help='aoai 端点配置的 JSON 文件路径',
        type=str)
    parser.add_argument(
        '--aoai_config_setting',
        default='gpt-35-turbo',
        help='要使用的配置设置 (aoai_config.json)',
        type=str)
    parser.add_argument(
        '--ta_config_file',
        default=(Path(__file__).absolute()).parent / "configs" / "ta_config.json",
        help='文本分析端点配置的 JSON 文件路径',
        type=str)
    parser.add_argument(
        '--ta_config_setting',
        required=False,
        default='ta-general',
        help='要使用的配置设置 (ta_config.json)',
        type=str)
    parser.add_argument(
        '--max_parallel_data',
        default=50,
        help='并行处理的数据最大数量。如果设置为 1，将按顺序运行',
        type=int)
    parser.add_argument(
        '--max_parallelism',
        default=2,
        help='每个幻觉检测模块并行发送的 GPT 请求最大数量。如果设置为 1，将按顺序运行',
        type=int)
    parser.add_argument(
        '--entity_detection_parallelism',
        default=2,
        help='每个幻觉检测模块并行处理的实体检测批次最大数量。如果设置为 1，将按顺序运行',
        type=int)
    parser.add_argument(
        '--simple_progress_bar',
        default='True',
        help='显示简化的进度条（数据级进度，而不是按不同批次的幻觉检测请求划分）',
        type=str)
    parser.add_argument(
        '--test_mode',
        default=0,
        help='测试用的简单迭代过滤器。将执行 E2E 但仅限于前 <N> 个数据，<N> 由该整数指定',
        type=int)
    parser.add_argument(
        '--gpt_batch_size',
        default=1,
        type=int,
        help='每批次的 GPT 请求数量')
    parser.add_argument(
        '--log_level',
        default='info',
        type=str,
        help='日志记录级别')
    parser.add_argument(
        '--logfile_name',
        default=None,
        type=str,
        help='日志文件名')

    args = parser.parse_args()

    args.max_parallel_data = max(args.max_parallel_data, 1)
    args.max_parallelism = max(args.max_parallelism, 1)
    args.entity_detection_parallelism = max(args.entity_detection_parallelism, 1)
    args.test_mode = max(args.test_mode, 0)
    args.simple_progress_bar = str2bool(args.simple_progress_bar)

    print(f'输入参数: {args}')
    return args

if __name__ == '__main__':
    args = parse_arguments()
    
    os.makedirs(args.output_folder, exist_ok=True)

    init_logging(args.log_level, args.logfile_name)
    logging.info('Starting Hallucination Detection')

    openai_args = create_openai_arguments(args.aoai_config_setting, args.max_parallelism, config_file=args.aoai_config_file)
    ta_args = create_ta_arguments(args.ta_config_setting, ta_config_file=args.ta_config_file)

    detector_args = DetectionArguments()
    detector_args.batch_size = args.gpt_batch_size
    
    print('Enabling parallelism for the tokenizer')
    os.environ['TOKENIZERS_PARALLELISM'] = 'true'
    print('Disabling Azure Telemetry (Doesnt handle parallelism well)')
    os.environ['AZURE_CORE_COLLECT_TELEMETRY'] = 'false'

    start_time = time.time()

    hallucination_result_folder = os.path.join(args.output_folder, 'hallucinations')
    os.makedirs(hallucination_result_folder, exist_ok=True)
    intermediate_result_folder = os.path.join(args.output_folder, 'intermediate')
    os.makedirs(intermediate_result_folder, exist_ok=True)
    
    disable_progress_bar = not args.simple_progress_bar

    dataloader = DataLoader(
        hypothesis=args.input_hypothesis,
        src_folder=args.input_src,
        test_mode=args.test_mode)

    hypothesis = dataloader._hypothesis  # Not used
    source_docs = dataloader._src_docs
    hyp_sentences_preproc = dataloader._hypothesis_preproc_sentences
    data_ids = dataloader._data_ids


    # Configure the medical bkg hallucination detection module.
    # The input consists of the ground truth file for analysis and a block
    # list (of medical terms you find later that you'd like to ignore)
    pbar_disabled_data_level = not args.simple_progress_bar
    pbar_disabled_batch_request_level = args.simple_progress_bar

    sentence_selector = None
    if args.sentence_selector_type:
        sentence_selector = SentenceSelectorFactory.create_sentence_selector(args.sentence_selector_type)

    entity_detector = None
    if args.entity_detector_type:
        if args.entity_detector_type == "text_analytics":
            args.entity_detector_type = "ta-general"
        entity_detector = EntityDetectorFactory.create_entity_detector(args.entity_detector_type,ta_args=ta_args)

    detection_agent = HallucinationDetector(
        sentence_selector=sentence_selector,
        entity_detector=entity_detector,
        openai_args=openai_args,
        detection_args=detector_args,
        aoai_config_file=args.aoai_config_file,
        entity_detection_parallelism=args.entity_detection_parallelism,
        disable_progress_bar=pbar_disabled_batch_request_level)

    allHallucinations = []
    retval_jsonl = []

    max_worker_threads = min(args.max_parallel_data, len(data_ids))
    with tqdm(total=len(data_ids), disable=pbar_disabled_data_level) as pbar:
        with ThreadPoolExecutor(max_workers=max_worker_threads) as executor:
            data_tasks = {
                executor.submit(
                    detection_agent.detect_hallucinations,
                    data_id,
                    source_docs[data_id],
                    hyp_sentences_preproc[data_id],): data_id for data_id in data_ids}
            for task in as_completed(data_tasks):
                try:
                    data_id = data_tasks[task]
                    hallucinations = task.result()
                    for h in hallucinations:
                        allHallucinations.append(h)
                except Exception as exc:
                    print(f'Error!! {type(exc).__name__}: {exc}')
                else:
                    num_sentences : int = len(hyp_sentences_preproc[data_id])
                    num_hallucinations : int = len(hallucinations)
                    hallucination_rate : float = num_hallucinations / num_sentences if num_sentences > 0 else 0.0
                    hallucinated : bool = num_hallucinations > 0
                    retval_jsonl.append(
                        {
                            AllHallucinations.DATA_ID: data_id,
                            AllHallucinations.HALLUCINATED: hallucinated,
                            AllHallucinations.HALLUCINATION_SCORE: hallucination_rate,
                            AllHallucinations.HALLUCINATIONS: hallucinations,
                            AllHallucinations.NUM_TOTAL_SENTENCES: num_sentences,
                            AllHallucinations.NUM_TOTAL_HALLUCINATIONS: num_hallucinations,
                        })
                pbar.update(1)

        retval_jsonl = sorted(retval_jsonl, key=lambda d: (d[AllHallucinations.DATA_ID]))
        outputFilePath = os.path.join(
            hallucination_result_folder,
            'allhallucinations.jsonl')
        with open(outputFilePath, 'w') as hallucinationOutputF:
            for kvp in retval_jsonl:
                hallucinationOutputF.write(json.dumps(kvp) + '\n')

        #detection_agent.PrintHallucinations(allHallucinations)
        save_hallucinations(allHallucinations, intermediate_result_folder)
        # detection_agent.SortDebugHallucinations()

    end_time = time.time() - start_time
    print('Hallucination Detection Has Finished')
    print(f'Total wall-clock time: {end_time} seconds')
    print(f'Final output written to {outputFilePath}')
