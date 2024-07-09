"""
0. 客服助理:专门根据负责向其它智能体询问问题,并生成最终答案
1. 公司信息助理:能根据公司名称提供给该公司的基本信息，包含子公司和母公司等详情
2. 案件信息助理:能根据案件名称提供该案件的基本信息和根据公司名称、上市公司名称、公司简称、公司代码和统一信用代码查询该公司参与的案件有涉案次数、涉案金额总和涉案金额最高的案件信息和第二高的案件等信息
3. 法院信息助理:能根据法院名称法院代字提供该法院相关信息
4. 律师事务所信息助理:能根据律师事务所名称提供该律师事务所相关信息和统计数据
5. 限制高消费信息助理:能根据案件号和公司名称查询该案件或公司限制高消费的相关信息
6. 地理信息助理:能根据根据地址查该地址对应的省份城市区县和获取该客户问题中指定日期的天气情况
7. 公司数据报告写作助理:能够根据要求收集公司的数据，写作这个公司数据整合报告
8. 起诉状写作助理:能根据针对公民起诉公民、公民起诉公司、公司起诉公民、公司起诉公司四种场景写作不同的起诉状
9. API调用信息助理:能够统计各个助理在检索信息过程中调用的API类型和次数
10. 错误信息助理:记录各类异常信息
11. 客户:将问题答案答复客户
"""

AgentTypeService = {
    "客服助理": "assistanter",
    "公司信息助理": "companyer",
    "案件信息助理": "legaler",
    "法院信息助理": "courter",
    "律师事务所信息助理": "lawfirmer",
    "限制高消费信息助理": "xzgxfer",
    "地理信息助理": "addresser",
    "公司数据报告写作助理": "reporter",
    "起诉状写作助理": "indictmenter",
    "API调用信息助理": "apier",
    "错误信息助理": "errorer",
    "客户": "publisher",
}


# 检查助理类型是否存在
def check_agenttype_service_exists(name):
    return name in AgentTypeService