from drlaw_agent.apis.law_data_query_api import (
    get_legal_abstract,
    get_legal_document,
    get_legal_document_list,
)
from drlaw_agent.apis.cal_data_query_api import get_sum, lawrank
from drlaw_agent.services.company_service import get_company_name_service
from drlaw_agent.services.base_service import convert_to_str, convert_to_float
from typing import List
from datetime import datetime
import json
import re


def extract_year_and_code(s: str) -> tuple[str]:
    # 使用正则表达式匹配括号内的年份和随后的地区代码
    pattern = r"\((\d{4})\)([沪津渝沈辽吉黑冀晋蒙陕甘宁新青藏川鄂湘赣皖苏鲁豫浙闽粤桂琼渝台]\d{4})"
    matches = re.search(pattern, s)

    if matches:
        year = matches.group(1)
        code = matches.group(2)
        return (year + "年", code)
    else:
        return ("", "")


def get_legal_document_service(legal_name: str) -> str:
    """
    根据案号查询裁判文书相关信息,包括"原告"、"被告" "原告律师事务所" "被告律师事务所", "案件摘要"等信息
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"案号": legal_name},
        {"案号": legal_name.replace("(", "（").replace(")", "）")},
        {"案号": legal_name.replace("（", "(").replace("）", ")")},
        {"案号": legal_name.replace("【", "(").replace("】", ")")},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        legal_info = get_legal_document(query_conds=query, need_fields=[])
        if legal_info:
            # 明确裁判文书中的日期为审理日期
            legal_info[0]["审理日期"] = legal_info[0]["日期"]
            del legal_info[0]["日期"]
            prosecute_year, court_code = extract_year_and_code(legal_info[0]["案号"])
            legal_info[0]["起诉(立案)日期"] = prosecute_year
            legal_info[0]["审理法院代字"] = court_code
            legal_abstract = get_legal_abstract_service(legal_name)
            # TODO更改时间名称 起诉（立案）日期 审理日期

            legal_info_str = json.dumps(legal_info, ensure_ascii=False)
            return f"查询该案号 {legal_name}的裁判文书信息如下:\n{legal_info_str}\n案件摘要信息如下:\n{legal_abstract}"

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该案号 {legal_name} 的裁判文书信息"


def get_legal_abstract_service(legal_name: str) -> str:
    """
    根据案号查询裁判文书摘要信息,包括"文件名" "案件摘要"等信息
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"案号": legal_name},
        {"案号": legal_name.replace("(", "（").replace(")", "）")},
        {"案号": legal_name.replace("（", "(").replace("）", ")")},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        legal_abstract = get_legal_abstract(query_conds=query, need_fields=[])
        if legal_abstract:
            # 如果找到了公司信息，返回序列化后的JSON字符串
            return json.dumps(legal_abstract, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该案号 {legal_name} 的裁判文书摘要信息"


def get_legal_document_list_service(
    company_name: str, need_fields: List[str]
) -> List[dict]:
    """
    根据公司名称、上市公司名称、公司简称、公司代码和统一信用代码查询该公司的关联的所有裁判文书信息
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"关联公司": company_name},
        {"关联公司": get_company_name_service(company_name)},
        {"关联公司": company_name.replace("(", "（").replace(")", "）")},
        {"关联公司": company_name.replace("（", "(").replace("）", ")")},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        legal_info = get_legal_document_list(query_conds=query, need_fields=need_fields)
        if legal_info:
            # # 如果找到了公司信息，返回序列化后的JSON字符串
            # legal_info_new = []
            # for legal in legal_info:
            #     legal_new = {**legal}
            #     # 明确裁判文书中的日期为审理日期
            #     legal_new["审理日期"] = legal["日期"]
            #     prosecute_year, court_code = extract_year_and_code(legal["案号"])
            #     legal_new["起诉(立案)日期"] = prosecute_year
            #     legal_new["审理法院代字"] = court_code
            #     legal_info_new.append(legal_new)
            return legal_info

    # 如果没有找到任何信息，返回错误消息
    return []


def _add_legal_amount(amount: List[str]) -> float:

    return get_sum(amount)


def get_legal_document_about_company_service(company_name: str) -> List[dict]:
    """
    根据公司名称、上市公司名称、公司简称、公司代码和统一信用代码查询该公司参与的案件有涉案次数、涉案金额总和涉案金额最高的案件信息和第二高的案件信息
    """
    info = get_legal_document_list_service(company_name, need_fields=[])
    count = len(info)
    amount = _add_legal_amount([i["涉案金额"] for i in info])
    amount_list = [i["涉案金额"] for i in info]
    rank_info = lawrank(info, amount_list)

    amount_top1_company = rank_info[-1]
    amount_top2_company = rank_info[-2]

    return f"该 {info[0]['关联公司']}涉及案件次数为{count}, 涉及案件金额总和为{amount}元\n\
涉案金额最高的案件详情如下:\n{amount_top1_company}\n\
涉案金额第二高的案件详情如下:\n{amount_top2_company}"


def get_legal_document_about_accused_service(
    company_name: str, prosecute_year: str = ""
) -> str:
    """
    根据公司名称、上市公司名称、公司简称、公司代码和统一信用代码查询该公司参与的案件中作为被起诉人的数据信息
    year 表示筛选出在特定起诉(立案)年份的数据,如"2020年"
    """
    info = get_legal_document_list_service(
        company_name, need_fields=["关联公司", "案号", "涉案金额", "被告"]
    )
    accused_info = []
    if not prosecute_year:
        accused_info = [i for i in info if i["关联公司"] in i["被告"]]
        year_str = ""
    else:
        for i in info:
            date_obj, _ = extract_year_and_code(i["案号"])  # 起诉时间
            # 将日期字符串转换为datetime对象
            # date_obj = datetime.strptime(i["日期"], "%Y-%m-%d %H:%M:%S") #审理时间
            if prosecute_year in date_obj and i["关联公司"] in i["被告"]:
                accused_info.append(i)
        year_str = f"在{prosecute_year}, "

    count = len(accused_info)
    amount = _add_legal_amount([i["涉案金额"] for i in accused_info])

    return (
        year_str
        + f"该 {info[0]['关联公司']} 作为被起诉人,涉及案件{count}起, 涉及案件金额总和为{amount}元"
    )


def get_legal_document_about_amount_service(
    company_name: str, maximum: str = "-1", minimum: str = "-1"
) -> str:
    """
    根据公司名称、上市公司名称、公司简称、公司代码和统一信用代码查询该公司的关联的所有裁判文书信息中涉案金额大于minimum小于maximum的案件信息
    """
    info = get_legal_document_list_service(
        company_name, need_fields=["案号", "涉案金额"]
    )
    if maximum != "-1" and minimum != "-1":
        info_filter = [
            i
            for i in info
            if convert_to_float(i["涉案金额"]) < convert_to_float(maximum)
            and convert_to_float(i["涉案金额"]) > convert_to_float(minimum)
        ]
        legal_detail = (
            f"该{company_name}涉案金额大于{minimum}小于{maximum}的案件信息如下:\n"
        )
        for legal in info_filter:
            legal_detail += f"案号 {legal['案号']} 涉案金额为: {legal['涉案金额']}\n"
        return legal_detail

    if maximum == "-1" and minimum != "-1":
        info_filter = [
            i
            for i in info
            if convert_to_float(i["涉案金额"]) > convert_to_float(minimum)
        ]
        legal_detail = f"该{company_name}涉案金额大于{minimum}的案件信息如下:\n"
        for legal in info_filter:
            legal_detail += f"案号 {legal['案号']} 涉案金额为: {legal['涉案金额']}\n"
        return legal_detail

    return f"该{company_name}未查询到相关案件信息"


if __name__ == "__main__":
    # print(get_legal_document_service("（2019）沪0115民初61975号"))
    # print(get_legal_abstract_service("（2019）沪0115民初61975号"))
    print(get_legal_document_about_company_service("浙江晨丰科技股份有限公司"))
    # print(
    #     get_legal_document_about_accused_service("上海晨光文具股份有限公司", "2020年")
    # )
