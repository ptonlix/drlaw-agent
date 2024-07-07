from drlaw_agent.apis.law_data_query_api import (
    get_court_code,
    get_court_info,
)
from drlaw_agent.apis.cal_data_query_api import get_sum, lawrank
from drlaw_agent.services.company_service import get_company_name_service
from drlaw_agent.services.base_service import convert_to_str, convert_to_float
from typing import List
from datetime import datetime
import json


def get_court_info_service(court_name: str) -> str:
    """
    根据法院名称查询法院名录相关信息,包括"法院名称"、"法院负责人" "成立日期" "法院地址" "法院联系电话" "法院官网"等信息
    例子:
        输入
        {court_name:"广东省高级人民法院"}
        输出：
        {
            "法院名称": "河南省洛阳市中级人民法院",
            "法院负责人": "曲海滨",
            "成立日期": "2017-12-25",
            "法院地址": "河南省洛阳市洛龙区展览路1号",
            "法院联系电话": "-",
            "法院官网": "-"
        }
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"法院名称": court_name},
    ]

    # 遍历所有查询条件，尝试获取法院信息
    for query in query_conditions:
        legal_info = get_court_info(query_conds=query, need_fields=[])
        if legal_info:
            # 如果找到了法院信息，返回序列化后的JSON字符串
            return json.dumps(legal_info, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该 {court_name} 的法院信息"


def get_court_code_service(court_name: str) -> str:
    """
    根据法院名称和法院代字查询法院相关信息,包括"法院名称"、"行政级别" "法院级别" "法院代字" "区划代码" "级别"等信息
    例子:
        输入
        {court_name:"广东省高级人民法院"} 或 {court_name:"粤0100"}
        输出：
        {
            "法院名称": "广东省高级人民法院",
            "行政级别": "省级",
            "法院级别": "高级法院",
            "法院代字": "粤",
            "区划代码": "440000",
            "级别": "1"
        }
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [{"法院名称": court_name}, {"法院代字": court_name}]

    # 遍历所有查询条件，尝试获取法院信息
    for query in query_conditions:
        legal_info = get_court_code(query_conds=query, need_fields=[])
        if legal_info:
            # 如果找到了法院信息，返回序列化后的JSON字符串
            return json.dumps(legal_info, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该 {court_name} 的法院信息"


if __name__ == "__main__":
    print(get_court_info_service("湖北省高级人民法院"))
    print(get_court_code_service("湖北省高级人民法院"))
