import json

from drlaw_agent.apis import (
    get_listed_company_info,
    search_company_name_by_super_info,
)
from drlaw_agent.utils import convert_to_float, convert_to_str, intersection_dict_lists
from drlaw_agent.services.base import re_get_full_name, _get_full_name


def get_company_investment_information(
    company_name: str, holding_ratio: str = "0", investment_amount: str = "0万"
) -> str:
    """
    根据公司的公司名称、控股比例和投资金额,查询该公司投资情况，包括查询该公司母公司投资情况或者该公司投资子公司情况
    投资情况包括: 投资金额、控股比例 等信息
    例如：
        输入：
        {"company_name": "冠昊生物科技股份有限公司",
         "holding_ratio": "50.0",
         "investment_amount": "5000万"}
    """
    parent_company = get_parent_company_info_service(company_name)
    # 查询不到母公司信息
    if "母公司名称" not in parent_company:
        parent_company = ""
    sub_company = get_sub_company_info_service(company_name)
    sub_company_obj = json.loads(sub_company)
    sub_company_count = len(sub_company_obj)

    sub_company_str = (
        f"子公司总数量为{sub_company_count}家,具体投资信息:{sub_company_obj},"
    )

    # 过滤出符合条件的子公司
    qualified_companies_by_ratio = []
    qualified_companies_by_investment = []
    qualified_companies = []
    if holding_ratio != "0":
        qualified_companies_by_ratio = [
            company
            for company in sub_company_obj
            if company["上市公司参股比例"]
            and convert_to_float(company["上市公司参股比例"])
            > convert_to_float(holding_ratio)
        ]
        qualified_companies = qualified_companies_by_ratio

    if investment_amount != "0万":
        qualified_companies_by_investment = [
            company
            for company in sub_company_obj
            if company["上市公司投资金额"]
            and convert_to_float(company["上市公司投资金额"])
            > convert_to_float(investment_amount)
        ]
        qualified_companies = qualified_companies_by_investment

    if holding_ratio != "0" and investment_amount != "0万":
        qualified_companies = intersection_dict_lists(
            qualified_companies_by_ratio, qualified_companies_by_investment
        )

    count = len(qualified_companies)
    sub_company_str_detail = (
        f"{company_name}控股比例超过{holding_ratio}并且投资金额大于{investment_amount}的子公司数量为{count}家,具体投资信息如下:{qualified_companies}"
        if holding_ratio != "0" or investment_amount != "0万"
        else sub_company_str
    )

    return (
        f"{company_name}投资信息如下:\n母公司投资信息:{parent_company}\n"
        + sub_company_str_detail
    )


def count_wholly_owned_sub_company_service(company_name: str) -> str:
    """
    根据公司的公司名称，查询该公司下属全资子公司的数量
    """
    sub_company = get_sub_company_info_service(company_name)
    sub_company = json.loads(sub_company)
    count = 0
    for sub in sub_company:
        if sub["上市公司参股比例"] == "100.0":
            count += 1
    return count


def get_multiple_parent_company_info_service(
    company_name_list: list[str] | dict,
) -> str:
    """
    根据多个子公司的公司名称，查询出这些子公司的母公司的信息
    母公司信息包括'母公司名称'、'母公司参股比例'、'母公司投资金额'。
    参数例子 : company_name_list=["宁波均理汽车系统有限公司", "株洲岱勒新材料有限责任公司","广州云瑞君益数据信息技术有限公司"]

    注意:如果要查询子公司控股比例、投资金额超过多少的数量,应当使用 get_company_investment_information
    """
    company_name_list_input = []
    if isinstance(company_name_list, dict):
        company_name_list_input = company_name_list.get("Items", [])
    else:
        company_name_list_input = company_name_list
    result = ""
    for company_name in company_name_list_input:
        result += get_parent_company_info_service(company_name) + "\n"
    return result


def get_parent_company_info_service(company_name: str) -> str:
    """
    根据子公司的公司名称，查询该公司的母公司信息，或者说查询该公司是哪家公司旗下的子公司。
    母公司信息包括'母公司名称'、'母公司参股比例'、'母公司投资金额'。

    注意:涉及到查询多个子公司的母公司信息时，应当使用get_multiple_parent_company
    """
    company_name = _get_full_name(company_name)
    rsp = get_listed_company_info(company_name)
    if not rsp:
        company_name = re_get_full_name(company_name)
        rsp = get_listed_company_info(company_name)
    ret = {"公司名称": company_name}
    if "关联上市公司全称" in rsp:
        ret["母公司名称"] = rsp["关联上市公司全称"]
    if "上市公司参股比例" in rsp:
        ret["母公司参股比例"] = rsp["上市公司参股比例"]
    if "关联上市公司全称" in rsp:
        ret["母公司投资金额"] = rsp["上市公司投资金额"]
    json_str = json.dumps(ret, ensure_ascii=False)
    return json_str


def get_sub_company_name_service(company_name: str) -> str:
    """
    根据母公司的公司名称，获得该公司旗下的所有子公司的名称。
    """
    company_name = _get_full_name(company_name)
    rsp = search_company_name_by_super_info("关联上市公司全称", company_name)
    if not rsp:
        company_name = re_get_full_name(company_name)
        rsp = search_company_name_by_super_info("关联上市公司全称", company_name)
    for item in rsp:
        sub_company_name = item["公司名称"]
        del item["公司名称"]
        item["子公司名称"] = sub_company_name
    json_str = json.dumps(rsp, ensure_ascii=False)
    return json_str


def get_sub_company_info_service(company_name: str) -> str:
    """
    根据母公司的公司名称，获得该公司的所有子公司、投资对象和资金投向的信息。
    包括'上市公司关系'、'上市公司参股比例'、'上市公司投资金额'、'公司名称'、'关联上市公司全称'，
    值得注意的是关联上市公司是该公司的名称，公司名称是该公司的子公司的名称。

    注意:根据母公司名称可以为:公司简称、英文名称或者公司的全称
    """
    company_name = _get_full_name(company_name)
    rsp = search_company_name_by_super_info("关联上市公司全称", company_name)
    if not rsp:
        company_name = re_get_full_name(company_name)
        rsp = search_company_name_by_super_info("关联上市公司全称", company_name)
    sub_company_name_list = [item["公司名称"] for item in rsp]
    listed_company_info_list = []
    for i in range(0, len(sub_company_name_list), 50):
        batch_list = sub_company_name_list[i : i + 50]
        listed_company_info_list.extend(get_listed_company_info(batch_list))
    for listed_company_info in listed_company_info_list:
        del listed_company_info["关联上市公司股票代码"]
        del listed_company_info["关联上市公司股票简称"]
    json_str = json.dumps(listed_company_info_list, ensure_ascii=False)
    return json_str


def count_sub_company_service(
    company_name: str, holding_ratio: str = "0", investment_amount: str = "0万"
) -> str:
    """
    根据母公司的公司名称、控股比例和投资金额，统计该公司相关子公司的数量。

    例如：
        输入：
        {"company_name": "冠昊生物科技股份有限公司",
         "holding_ratio": "50.0",
         "investment_amount": "5000万"}
    """
    company_name = _get_full_name(company_name)
    all_sub_company_name = search_company_name_by_super_info(
        "关联上市公司全称", company_name
    )
    if not all_sub_company_name:
        company_name = re_get_full_name(company_name)
        all_sub_company_name = search_company_name_by_super_info(
            "关联上市公司全称", company_name
        )
    owned_count = count_wholly_owned_sub_company_service(company_name)

    sub_company = get_sub_company_info_service(company_name)
    sub_company_obj = json.loads(sub_company)

    # 过滤出符合条件的子公司
    qualified_companies_by_ratio = []
    qualified_companies_by_investment = []
    qualified_companies = []
    if holding_ratio != "0":
        qualified_companies_by_ratio = [
            company
            for company in sub_company_obj
            if company["上市公司参股比例"]
            and convert_to_float(company["上市公司参股比例"])
            > convert_to_float(holding_ratio)
        ]
        qualified_companies = qualified_companies_by_ratio

    if investment_amount != "0万":
        qualified_companies_by_investment = [
            company
            for company in sub_company_obj
            if company["上市公司投资金额"]
            and convert_to_float(company["上市公司投资金额"])
            > convert_to_float(investment_amount)
        ]
        qualified_companies = qualified_companies_by_investment

    if holding_ratio != "0" and investment_amount != "0万":
        qualified_companies = intersection_dict_lists(
            qualified_companies_by_ratio, qualified_companies_by_investment
        )

    count = len(qualified_companies)
    sub_company_str = (
        f"{company_name}控股比例超过{holding_ratio}并且投资金额大于{investment_amount}的子公司数量为{count}家,具体投资信息如下:{qualified_companies}"
        if holding_ratio != "0" or investment_amount != "0万"
        else "无"
    )

    ret = {
        "公司名称": company_name,
        f"{company_name}所有子公司的数量": len(all_sub_company_name),
        f"{company_name}所属全资子公司的数量": owned_count,
        "其他信息": sub_company_str if sub_company_str else "无",
    }
    json_str = json.dumps(ret, ensure_ascii=False)
    return json_str


def search_company_name_by_super_info_service(key: str, value: str) -> str:
    """
    根据关联上市公司信息某个字段是某个值来查询具体的公司名称。
    可以输入的字段有['上市公司关系','上市公司参股比例','上市公司投资金额','关联上市公司全称',
    '关联上市公司股票代码','关联上市公司股票简称',]

    例如：
        输入：
        {"key": "关联上市公司全称",
         "value": "冠昊生物科技股份有限公司"}
        输出：
        [{'公司名称': '北昊干细胞与再生医学研究院有限公司'},
         {'公司名称': '北京申佑医学研究有限公司'},
         {'公司名称': '北京文丰天济医药科技有限公司'},
         {'公司名称': '冠昊生命健康科技园有限公司'}]
    """
    rsp = search_company_name_by_super_info(key, value)
    json_str = json.dumps(rsp, ensure_ascii=False)
    return json_str


def query_total_amount_invested_in_subsidiaries(company_name: str) -> str:
    """根据上市公司的公司名称、公司简称或英文名称，查询该公司在子公司投资的总金额。"""
    full_name = _get_full_name(company_name)
    rsp = search_company_name_by_super_info("关联上市公司全称", full_name)
    if not rsp:
        full_name = re_get_full_name(company_name)
        rsp = search_company_name_by_super_info("关联上市公司全称", full_name)
    total_amount = 0
    for item in rsp:
        sub_company_name = item["公司名称"]
        listed_company_info = get_listed_company_info(sub_company_name)
        if "上市公司投资金额" not in listed_company_info:
            continue
        amount = listed_company_info["上市公司投资金额"]
        if amount is None:
            continue
        total_amount += convert_to_float(amount)
    rsp = {
        "公司名称": company_name,
        "在子公司投资的总金额": convert_to_str(total_amount),
    }
    json_str = json.dumps(rsp, ensure_ascii=False)
    return json_str


def search_company_name_by_stock_bref(company_name: str) -> str:
    """
    根据公司的股票简称名称查询该公司名称

    参数：
        company_name: 股票简称
    返回：
        公司名称列表
    例如：
        输入：
        company_name="文灿股份"
        输出：
        {'公司名称':'文灿集团股份有限公司'}
    """
    sub_company = search_company_name_by_super_info_service(
        key="关联上市公司股票简称", value=company_name
    )
    sub_company = json.loads(sub_company)
    if not sub_company:
        return {"公司名称": ""}
    if isinstance(sub_company, dict):
        sub_company = sub_company.get("公司名称")
    elif isinstance(sub_company, list):
        sub_company = sub_company[0].get("公司名称")
    return {"公司名称": get_listed_company_info(sub_company).get("关联上市公司全称")}


if __name__ == "__main__":
    # print(get_company_investment_information("湖北振华化学股份有限公司"))
    # print(count_wholly_owned_sub_company("烟台北方安德利果汁股份有限公司"))
    # print(get_sub_company_info_service("深圳市大族数控科技股份有限公司"))
    # print(get_parent_company_info_service("象山激智新材料有限公司"))
    print(count_sub_company_service("北京当升材料科技股份有限公司", "50.0", "5000万"))
    # print(count_sub_company_service("金宏气体股份有限公司", "50.0"))
    # 上海百钠新能源科技有限公司、伊春碧水环保工程有限公司、浙江天能物联网科技有限公司
    # print(
    #     get_multiple_parent_company_info_service(
    #         company_name_list={
    #             "Items": [
    #                 "上海百钠新能源科技有限公司",
    #                 "伊春碧水环保工程有限公司",
    #                 "浙江天能物联网科技有限公司",
    #             ]
    #         }
    #     )
    # )
