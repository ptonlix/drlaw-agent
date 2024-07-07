from drlaw_agent.apis.law_data_query_api import (
    get_lawfirm_info,
    get_lawfirm_log,
)
from drlaw_agent.apis.cal_data_query_api import get_sum, lawrank
from drlaw_agent.services.company_service import get_company_name_service
from drlaw_agent.services.base_service import convert_to_str, convert_to_float
from typing import List
from datetime import datetime
import json


def get_lawfirm_info_service(lawfirm_name: str) -> str:
    """
    根据律师事务所查询律师事务所名录,包括"律师事务所名称"、"律师事务所负责人" "律师事务所唯一编码" "事务所成立日期" "律师事务所地址" "律所登记机关"等信息
    例子:
        输入
        {lawfirm_name:"爱德律师事务所"}
        输出：
        {
            "律师事务所名称": "爱德律师事务所",
            "律师事务所唯一编码": "31150000E370803331",
            "律师事务所负责人": "巴布",
            "事务所注册资本": "10万元人民币",
            "事务所成立日期": "1995-03-14",
            "律师事务所地址": "呼和浩特市赛罕区大学西街110号丰业大厦11楼",
            "通讯电话": "0471-3396155",
            "通讯邮箱": "kehufuwubu@ardlaw.cn",
            "律所登记机关": "内蒙古自治区呼和浩特市司法局"
        }
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"律师事务所名称": lawfirm_name},
    ]

    # 遍历所有查询条件，尝试获取法院信息
    for query in query_conditions:
        legal_info = get_lawfirm_info(query_conds=query, need_fields=[])
        if legal_info:
            # 如果找到了法院信息，返回序列化后的JSON字符串
            return json.dumps(legal_info, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该 {lawfirm_name} 的律师事务所信息"


def get_lawfirm_log_service(lawfirm_name: str) -> str:
    """
    根据律师事务所查询律师事务所统计数据,包括"律师事务所名称"、"业务量排名" "服务已上市公司数量" "报告期间所服务上市公司违规事件数量" "报告期所服务上市公司接受立案调查数量" 等信息
    例子:
        输入
        {lawfirm_name:"爱德律师事务所"}
        输出：
        {
            "律师事务所名称": "北京市金杜律师事务所",
            "业务量排名": "2",
            "服务已上市公司": "68",
            "报告期间所服务上市公司违规事件": "23",
            "报告期所服务上市公司接受立案调查": "3"
        }
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"律师事务所名称": lawfirm_name},
    ]

    # 遍历所有查询条件，尝试获取法院信息
    for query in query_conditions:
        legal_info = get_lawfirm_log(query_conds=query, need_fields=[])
        if legal_info:
            # 如果找到了法院信息，返回序列化后的JSON字符串
            return json.dumps(legal_info, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该 {lawfirm_name} 的律师事务所统计数据"


if __name__ == "__main__":
    print(get_lawfirm_info_service("爱德律师事务所"))
    print(get_lawfirm_log_service("北京市金杜律师事务所"))
