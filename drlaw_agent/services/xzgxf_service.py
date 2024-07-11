from drlaw_agent.apis.law_data_query_api import (
    get_xzgxf_info,
    get_xzgxf_info_list,
)
from drlaw_agent.services.company_service import get_company_name_service
from drlaw_agent.apis.cal_data_query_api import get_sum, lawrank
from drlaw_agent.services.company_service import get_company_name_service
from drlaw_agent.services.base_service import convert_to_str, convert_to_float
from typing import List
from datetime import datetime
import json


def get_xzgxf_info_service_for_report(legal_name: str) -> List[dict]:
    """
    根据案号查询限制高消费相关信息,包括"限制高消费企业名称"、"法定代表人" "申请人" "涉案金额" "执行法院" "立案日期" "限高发布日期"等信息
    例子：
        输入：
        {legal_name:（2018）鲁0403执1281号}
        返回：
        {
        "限制高消费企业名称": "枣庄西能新远大天然气利用有限公司",
        "案号": "（2018）鲁0403执1281号",
        "法定代表人": "高士其",
        "申请人": "枣庄市人力资源和社会保障局",
        "涉案金额": "12000",
        "执行法院": "山东省枣庄市薛城区人民法院",
        "立案日期": "2018-11-16 00:00:00",
        "限高发布日期": "2019-02-13 00:00:00"
        }
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"案号": legal_name},
        {"案号": legal_name.replace("(", "（").replace(")", "）")},
        {"案号": legal_name.replace("（", "(").replace("）", ")")},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        legal_info = get_xzgxf_info(query_conds=query, need_fields=[])
        if legal_info:
            return [legal_info]

    return []


def get_xzgxf_info_service(legal_name: str) -> str:
    """
    根据案号查询限制高消费相关信息,包括"限制高消费企业名称"、"法定代表人" "申请人" "涉案金额" "执行法院" "立案日期" "限高发布日期"等信息
    例子：
        输入：
        {legal_name:（2018）鲁0403执1281号}
        返回：
        {
        "限制高消费企业名称": "枣庄西能新远大天然气利用有限公司",
        "案号": "（2018）鲁0403执1281号",
        "法定代表人": "高士其",
        "申请人": "枣庄市人力资源和社会保障局",
        "涉案金额": "12000",
        "执行法院": "山东省枣庄市薛城区人民法院",
        "立案日期": "2018-11-16 00:00:00",
        "限高发布日期": "2019-02-13 00:00:00"
        }
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"案号": legal_name},
        {"案号": legal_name.replace("(", "（").replace(")", "）")},
        {"案号": legal_name.replace("（", "(").replace("）", ")")},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        legal_info = get_xzgxf_info(query_conds=query, need_fields=[])
        if legal_info:
            # 如果找到了公司信息，返回序列化后的JSON字符串
            return json.dumps(legal_info, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该案号 {legal_name} 的限制高消费信息"


def get_xzgxf_info_list_service(company_name: str) -> str:
    """
    根据企业名称查询所有限制高消费相关信息,包括"限制高消费企业名称"、"法定代表人" "申请人" "涉案金额" "执行法院" "立案日期" "限高发布日期"等信息
    例子：
        输入：
        {company_name: "欣水源生态环境科技有限公司"}
        返回：
        [{
        "限制高消费企业名称": "欣水源生态环境科技有限公司",
        "案号": "（2023）黔2731执恢130号",
        "法定代表人": "刘福云",
        "申请人": "四川省裕锦建设工程有限公司惠水分公司",
        "涉案金额": "7500000",
        "执行法院": "贵州省黔南布依族苗族自治州惠水县人民法院",
        "立案日期": "2023-08-04 00:00:00",
        "限高发布日期": "2023-11-09 00:00:00"
        }]
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"限制高消费企业名称": company_name},
        {"限制高消费企业名称": get_company_name_service(company_name)},
        {"限制高消费企业名称": company_name.replace("(", "（").replace(")", "）")},
        {"限制高消费企业名称": company_name.replace("（", "(").replace("）", ")")},
    ]

    # 遍历所有查询条件，尝试获取公司信息
    for query in query_conditions:
        legal_info = get_xzgxf_info_list(query_conds=query, need_fields=[])
        if legal_info:
            # 如果找到了公司信息，返回序列化后的JSON字符串
            return json.dumps(legal_info, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该 {company_name} 的限制高消费信息"


if __name__ == "__main__":
    print(get_xzgxf_info_service("（2018）鲁0403执1281号"))
    print(get_xzgxf_info_list_service("欣水源生态环境科技有限公司"))
