def split_by_length(file_path, length=2000):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 按照指定长度切分
    parts = [content[i:i+length] for i in range(0, len(content), length)]

    return parts

# 示例用法
file_path = './novel1.txt'
length = 3000  # 每部分的字符数
parts = split_by_length(file_path, length)

# # 打印每一部分的内容
# for idx, part in enumerate(parts):
#     print(f"Part {idx+1}:\n{part}\n{'='*40}\n")
#
# print(len(parts[1]))



"""
def split_chapters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 用正则表达式匹配章标题
    import re
    chapters = re.split(r'(第[一二三四五六七八九十百千万]*章)', content)

    # 合并章标题和内容
    chapter_list = []
    for i in range(1, len(chapters), 2):
        chapter_title = chapters[i]
        chapter_content = chapters[i + 1] if i + 1 < len(chapters) else ""
        chapter_list.append(chapter_title + chapter_content)

    return chapter_list


# 示例用法
file_path = './novel.txt'
chapters = split_chapters(file_path)

# # 打印每一章的内容
# for idx, chapter in enumerate(chapters):
#     print(f"Chapter {idx + 1}:\n{chapter}\n{'=' * 40}\n")
# print(chapters[20])
# print(type(chapters))
# print(len(chapters[104]))

for i in chapters:
    if len(i)<2500:
        print(len(i))

"""