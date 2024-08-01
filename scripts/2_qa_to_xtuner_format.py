import json


# 定义读取和转换函数
def convert_json_file(input_file_path, output_file_path):
    # 读取原始JSON文件
    with open(input_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 转换数据格式
    converted_data = []
    for item in data:
        conversation_item = {
            "conversation": [
                {
                    "input": item["question"],
                    "output": item["answer"]
                }
            ]
        }
        converted_data.append(conversation_item)

    # 保存为新的JSON文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=4)

    print(f"JSON文件已转换并保存到 {output_file_path}")


# 示例调用
input_file_path = 'QA.json'  # 输入文件路径
output_file_path = 'converted_QA.json'  # 输出文件路径

convert_json_file(input_file_path, output_file_path)
