from typing import Iterable
import jsonlines


# 定义一个函数read_jsonl，用于读取jsonl文件
def read_jsonl(path):
    # 初始化一个空列表，用于存储读取到的内容
    content = []
    # 使用jsonlines库打开jsonl文件，并设置为只读模式
    with jsonlines.open(path, "r") as json_file:
        # 遍历json文件的每一行，将其转换为字典类型
        for obj in json_file.iter(type=dict, skip_invalid=True):
            # 将每一行添加到content列表中
            content.append(obj)
    # 返回content列表
    return content


def save_answers(
    queries: Iterable,
    results: Iterable,
    result_file: str = "./dataset/DeepRead_result.json",
):
    answers = []
    for query, result in zip(queries, results):
        answers.append(
            {"id": query["id"], "question": query["question"], "answer": result}
        )

    # use jsonlines to save the answers
    def write_jsonl(path, content):
        with jsonlines.open(path, "w") as json_file:
            json_file.write_all(content)

    # 保存答案 result_file 指定位置
    write_jsonl(result_file, answers)


def read_txt_file_to_list(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # 使用列表推导式将每一行转换为列表的元素
            data_list = [line.strip() for line in file]
            data_list = [ele for ele in data_list if ele != ""]
        return data_list
    except FileNotFoundError as e:
        print(f"File {file_path} not found.")
        raise e


def convert_to_float(s):
    if s is None:
        return 0

    # 使用正则表达式将字符串中的数字和中文符号替换为英文符号
    s = s.replace("亿", "e8").replace("万", "e4")

    try:
        # 使用float函数将字符串转换为浮点数
        result = float(s)
    except Exception as e:
        result = 0

    return result


def convert_to_str(f):
    if f > 1e8:
        f = f / 1e8
        return f"{round(f, 2):.2f}" + "亿"
    if f > 1e4:
        f = f / 1e4
        return f"{round(f, 2):.2f}" + "万"
    return f"{round(f, 2):.2f}"


def convert_to_tuple(d: dict) -> tuple:
    """Converts a dictionary to a tuple of its items."""
    return tuple(sorted(d.items()))


def convert_to_dict(t: tuple) -> dict:
    """Converts a tuple of items back to a dictionary."""
    return dict(t)


def intersection_dict_lists(list1: list, list2: list) -> list:
    """Returns the intersection of two lists of dictionaries."""
    set1 = set(convert_to_tuple(d) for d in list1)
    set2 = set(convert_to_tuple(d) for d in list2)

    union_set = set1 & set2  # intersection of the two sets

    return [convert_to_dict(t) for t in union_set]


if __name__ == "__main__":
    querys = read_jsonl("./dataset/question_example.json")
    results = read_jsonl("./dataset/帝阅DeepRead_result.json")
    for i, query in enumerate(results):
        print(f"test{i}")
        if i != results[i].get("id"):
            results_id = results[i].get("id")
            print(f"{i} {results_id}")

    for i, query in enumerate(querys):
        content = {
            "id": query.get("id"),
            "question": query.get("question"),
            "answer": results[i].get("answer"),
        }
        with jsonlines.open("./dataset/DeepRead_result.json", "a") as json_file:
            json_file.write(content)
