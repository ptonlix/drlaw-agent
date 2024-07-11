import copy
from drlaw_agent.apis.company_data_query_api import (
    get_company_info,
    get_company_register,
    get_company_register_name,
    get_sub_company_info,
    get_sub_company_info_list,
)
from drlaw_agent.apis.cal_data_query_api import get_sum
from drlaw_agent.services.base_service import convert_to_str, convert_to_float
import json
from typing import List


def get_company_name_service(company_name: str) -> str:
    # 定义一个查询条件的列表，包含所有可能的查询条件
    # 上市公司
    query_conditions = [
        {"公司名称": company_name},
        {"公司简称": company_name},
        {"公司代码": company_name},
        {"公司名称": company_name.replace("(", "（").replace(")", "）")},
        {"公司名称": company_name.replace("（", "(").replace("）", ")")},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        company_info = get_company_info(query_conds=query, need_fields=[])
        if company_info:
            return company_info[0]["公司名称"]
    # 统一信用代码查询
    company_name = get_company_register_name_service(company_name)

    return company_name


def get_company_info_service(company_name: str) -> str:
    """
    根据上市公司名称、公司简称和公司代码查询公司的基本信息
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"公司名称": company_name},
        {"公司简称": company_name},
        {"公司代码": company_name},
        {"公司名称": company_name.replace("(", "（").replace(")", "）")},
        {"公司名称": company_name.replace("（", "(").replace("）", ")")},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        company_info = get_company_info(query_conds=query, need_fields=[])
        if company_info:
            # 如果找到了公司信息，返回序列化后的JSON字符串
            return json.dumps(company_info, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该公司 {company_name} 的基本信息"


def get_company_register_service(company_name: str) -> str:
    """
    根据公司名称、上市公司名称、公司简称、公司代码和统一信用代码查询公司的工商注册信息
    """

    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"公司名称": company_name},
        {"公司名称": get_company_name_service(company_name)},
        {"公司名称": company_name.replace("(", "（").replace(")", "）")},
        {"公司名称": company_name.replace("（", "(").replace("）", ")")},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        company_info = get_company_register(query_conds=query, need_fields=[])
        if company_info:
            # 如果找到了公司信息，返回序列化后的JSON字符串
            return json.dumps(company_info, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该公司 {company_name} 的工商信息"


def get_company_register_name_service(company_social_code: str) -> str:
    """
    根据统一社会信用代码查询公司的名称
    例如:
        输入:
        {company_social_code:"91620702581156176Q"}
        输出:
        北京格润美顺环境科技有限公司
    """

    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [{"统一社会信用代码": company_social_code}]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        company_info = get_company_register_name(query_conds=query, need_fields=[])
        if company_info:
            # 如果找到了公司名称，返回序列化后的JSON字符串
            return company_info[0]["公司名称"]

    return ""


def get_parent_company_info_service(company_name: str) -> str:
    """
    根据公司名称、统一社会信用代码查询该公司的母公司信息
    """

    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"公司名称": company_name},
        {
            "公司名称": get_company_register_name_service(company_name)
        },  # 根据统一社会信用代码查询
        {"公司名称": company_name.replace("(", "（").replace(")", "）")},
        {"公司名称": company_name.replace("（", "(").replace("）", ")")},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        company_info = get_sub_company_info(query_conds=query, need_fields=[])
        if company_info:
            # 如果找到了公司名称，返回序列化后的JSON字符串
            company_detail = company_info[0]
            return f"{company_name}的母公司是 {company_detail['关联上市公司全称']}\n\
母公司的参股比例为:{company_detail['上市公司参股比例']}%\n\
母公司的投资金额为:{company_detail['上市公司投资金额']}\n\
母公司与{company_name}的关系为:{company_detail['上市公司关系']}"

    return f"查询不到{company_name}的母公司信息"


def _add_investment_amount(amount: List[str]) -> float:

    return get_sum(amount)


def get_sub_company_info_list_service_for_report(company_name: str) -> str:
    """
    根据公司名称、上市公司名称、公司简称、公司代码和统一信用代码查询该公司的子公司信息详情
    """

    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"关联上市公司全称": company_name},
        {"关联上市公司全称": get_company_name_service(company_name)},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        company_info = get_sub_company_info_list(query_conds=query, need_fields=[])
        if company_info:
            # 如果找到了公司信息，返回序列化后的JSON字符串
            return json.dumps(company_info, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该公司 {company_name} 的基本信息"


def get_sub_company_info_list_service(company_name: str) -> str:
    """
    根据公司名称、上市公司名称、公司简称、公司代码和统一信用代码查询该公司的子公司信息详情
    """

    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"关联上市公司全称": company_name},
        {"关联上市公司全称": get_company_name_service(company_name)},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        company_info = get_sub_company_info_list(query_conds=query, need_fields=[])
        if company_info:
            # 如果找到了公司名称，返回序列化后的JSON字符串
            sub_company_count = len(company_info)
            total_investment_amount = _add_investment_amount(
                [sub_company["上市公司投资金额"] for sub_company in company_info]
            )
            max_investment = copy.deepcopy(
                max(company_info, key=lambda x: x["上市公司投资金额"])
            )
            del max_investment["关联上市公司全称"]
            max_investment = json.dumps(max_investment, ensure_ascii=False)
            min_investment = copy.deepcopy(
                min(company_info, key=lambda x: x["上市公司投资金额"])
            )
            del min_investment["关联上市公司全称"]
            min_investment = json.dumps(min_investment, ensure_ascii=False)
            wholly_owned = [
                {k: v for k, v in sub_company.items() if k != "关联上市公司全称"}
                for sub_company in company_info
                if convert_to_float(sub_company["上市公司投资金额"]) > 1e8
                and sub_company["上市公司参股比例"] == "100.0"
            ]
            wholly_owned_str = json.dumps(wholly_owned, ensure_ascii=False)
            return f"{company_name}的子公司信息如下:\n\
子公司总数是: {sub_company_count}家\n\
对子公司的全部投资总额为:{total_investment_amount:.3f}元\n\
投资金额最高的子公司是: {max_investment}\n\
投资金额最低的子公司是: {min_investment}\n\
投资金额过亿的全资子公司数量为: {len(wholly_owned)}家, 详情如下:\n{wholly_owned_str}\n"

    return f"查询不到{company_name}的子公司信息"


if __name__ == "__main__":
    # print(get_company_info_service("上海妙可蓝多食品科技股份有限公司"))
    # print(get_company_register_service("四川青石建设有限公司"))
    # print(get_company_register_name_service("91110113344302387N"))
    print(get_parent_company_info_service("91411625MA40GA2H02"))
    # print(get_sub_company_info_list_service("金迪克"))
