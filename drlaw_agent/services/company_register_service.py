import json
from drlaw_agent.apis import (
    get_company_register,
    search_company_name_by_register,
    search_company_and_registered_capital_by_industry,
)
from drlaw_agent.utils import convert_to_float
from drlaw_agent.services.base import re_get_full_name, _get_full_name


def get_company_register_service(company_name: str) -> str:
    """
    根据公司名称，获得该公司所有注册信息。

    例如：
        输入：
        {"company_name": "广州发展集团股份有限公司"}
        输出：
        {'企业类型': '股份有限公司（上市、国有控股）',
         '公司名称': '广州发展集团股份有限公司',
         '区县': '天河区',
         '参保人数': '207.0',
         '城市': '广州市',
         '成立日期': '1992-11-13',
         '曾用名': '广州发展实业控股集团股份有限公司、广州电力企业集团股份有限公司',
         '注册号': '440101000196724',
         '注册资本': '354405.5525',
         '登记状态': '在业',
         '省份': '广东省',
         '组织机构代码': '23124317-3',
         '统一社会信用代码': '91440101231243173M'}
    """
    company_name = _get_full_name(company_name)
    rsp = get_company_register(company_name)
    if not rsp:
        company_name = re_get_full_name(company_name)
        rsp = get_company_register(company_name)
    json_str = json.dumps(rsp, ensure_ascii=False)
    return json_str


def search_company_name_by_registration_number_service(registration_number: str) -> str:
    """
    根据注册号查询公司名称。
    """
    rsp = search_company_name_by_register("注册号", registration_number)
    json_str = json.dumps(rsp, ensure_ascii=False)
    return json_str


def search_company_name_by_register_service(key: str, value: str) -> str:
    """
    根据公司注册信息 key 是某个 value 来查询具体的公司名称。
    key 可以是 '企业类型','区县','参保人数','城市','成立日期','曾用名','注册号','注册资本',
    '登记状态','省份','组织机构代码'或者'统一社会信用代码'。

    例如：
        输入：
        {"key": "注册号",  "value": "440101000196724"}
        输出：
        {"公司名称": "广州发展集团股份有限公司"}
    """
    rsp = search_company_name_by_register(key, value)
    json_str = json.dumps(rsp, ensure_ascii=False)
    return json_str


def search_cnr_by_industry_service(industry_name: str) -> str:
    """根据行业名称查询属于该行业的公司及其注册资本。"""
    rsp = search_company_and_registered_capital_by_industry(industry_name)
    count = len(rsp)
    if rsp:
        sorted_list = sorted(
            rsp,
            key=lambda x: convert_to_float(x["注册资本"]),
            reverse=True,
        )

        top_value = sorted_list[:3]

    return f"该{industry_name}注册资本最大前3公司为:{top_value}\n该行业所属全部公司详细信息如下:\n公司数量:{count}家\n 公司详情:{rsp}\n"


if __name__ == "__main__":
    print(search_cnr_by_industry_service("电气机械和器材制造业"))
    # print(search_company_name_by_registration_number_service("320512400000458"))
    # print(get_company_register_service("健帆生物科技集团股份有限公司"))
