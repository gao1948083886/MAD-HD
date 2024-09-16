# import json
# import pandas as pd
#
# # 输入数据
# data = []
# with open("../test_suite/data-dev.jsonl", "r") as f:
#     for line in f:
#         data.append(json.loads(line))
#
# print(data[:5])
#
# # 初始化转换后的数据
# output_data = []
#
# # 循环遍历输入数据并做转换
# for i, item in enumerate(data, start=1):
#     claim = item['claim']
#     label = item['label']
#
#     # IsHallucination设置为1如果label是INCORRECT，0如果label是CORRECT
#     is_hallucination = 0 if label == "CORRECT" else 1
#
#     # 构造输出行
#     output_data.append({
#         "DataID": i,
#         "SentenceID": 1,  # 统一设置为1
#         "Sentence": claim,
#         "IsHallucination": is_hallucination,
#         "Consistency": ""  # Consistency不需要设置，空着
#     })
#
# # 转换为DataFrame
# df = pd.DataFrame(output_data)
#
# # 显示结果
# df.to_csv("../test_suite/FactCC503/FactCC503_raw_response.tsv", sep='\t', index=False)

import pandas as pd
import os
import json

# Specify the file path
file_path = '../test_suite/test-00000-of-00001.parquet'

# Load the Parquet file into a DataFrame
df = pd.read_parquet(file_path, engine='pyarrow')  # Or use engine='fastparquet'

# Display the first few rows to check
print(df.head())

# 输入数据
data = []
with open("../test_suite/data-dev.jsonl", "r") as f:
    for line in f:
        data.append(json.loads(line))


# 提取 ID 中的唯一部分
def extract_unique_id(full_id):
    return full_id.split('-')[-1]


# 创建保存文章的文件夹
output_dir = '../test_suite/FactCC503/src'
os.makedirs(output_dir, exist_ok=True)

# 循环处理每条数据
for idx, item in enumerate(data, start=1):
    # 提取id中的唯一部分
    unique_id = extract_unique_id(item['id'])

    # 根据unique_id查找对应的article
    matching_row = df[df['id'].str.contains(unique_id)]

    if not matching_row.empty:
        # 获取 article 列的内容
        article_content = matching_row['article'].values[0]

        # 将 article 内容写入文件，文件名为1.txt, 2.txt等
        output_file_path = os.path.join(output_dir, f"{idx}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(article_content)

        print(f"Saved article {idx} to {output_file_path}")
    else:
        print(f"No matching article found for ID: {unique_id}")
