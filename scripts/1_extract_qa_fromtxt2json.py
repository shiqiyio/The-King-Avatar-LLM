import json
import re
from tqdm import tqdm
def extract_qa_pairs(file_path):
    qa_pairs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in tqdm(lines):
            match = re.search(r'\{"question": "(.*?)", "answer": "(.*?)"\}', line)
            if match:
                question = match.group(1)
                answer = match.group(2)
                qa_pairs.append({"question": question, "answer": answer})
    return qa_pairs

def save_to_json(qa_pairs, output_path):
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(qa_pairs, json_file, ensure_ascii=False, indent=4)

# 使用示例
txt_file_path = './gen_QA1.txt'
json_output_path = './QA.json'

qa_pairs = extract_qa_pairs(txt_file_path)
save_to_json(qa_pairs, json_output_path)

print(f"提取的问答对已保存到 {json_output_path}")
