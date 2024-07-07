from drlaw_agent.apis.address_data_query_api import (
    get_address_info,
    get_address_code,
    get_temp_info,
)
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json


def get_address_info_service(address: str) -> str:
    """
    根据地址查该地址对应的省份城市区县,包括"地址"、"省份" "城市" "区县" "城市区划代码" "区县区划代码"等信息
    例子:
        输入
        {address:"保定市天威西路2222号"}
        输出：
        {
            "地址": "保定市天威西路2222号",
            "省份": "河北省",
            "城市": "保定市",
            "区县": "竞秀区"
            "城市区划代码":
            "区县区划代码":
        }
    """
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [
        {"地址": address},
    ]

    # 遍历所有查询条件，尝试获取法院信息
    for query in query_conditions:
        address_info = get_address_info(query_conds=query, need_fields=[])
        if address_info:
            address_code = get_address_code(
                query_conds={
                    "省份": address_info[0]["省份"],
                    "城市": address_info[0]["城市"],
                    "区县": address_info[0]["区县"],
                },
                need_fields=[],
            )
            address_merge = {**address_info[0], **address_code[0]}
            return json.dumps(address_merge, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return f"查找不到该 {address} 地址的省份城市区县的信息"


USER_MESSAGE = """
{question}
请将提取这句话中时间，省份、城市。 返回格式为JSON：例如{{"省份": "北京市", "城市": "北京市", "日期": "2020年1月1日"}}
注意日期必须是XXXX年XX月XX日格式
注意直辖市省份城市是同一个
"""


def get_answer_info(question: str) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("human", USER_MESSAGE),
        ]
    )

    get_about_info = (
        prompt
        | ChatOpenAI(
            model="glm-4-0520",
            temperature=0.1,
            model_kwargs={
                "tools": [
                    {
                        "type": "web_search",
                        "web_search": {
                            "enable": False  # 禁用：False，启用：True，默认为 True。
                        },
                    }
                ]
            },
        )
        | JsonOutputParser()
    )

    return get_about_info.invoke(question)


def get_temp_info_service(question: str) -> str:
    """
    根据提问的问题，获取该问题中说明的省份城市在指定日期的天气情况，包含"最高温度" "最低温度" "湿度"等信息
    例子:
        输入
        {address_date:"2021年8月19日这一天,这个地址的上海市闵行区新骏环路138号1幢401室的天气如何?"}
        输出：
        {
            "日期": "2020年1月1日",
            "省份": "北京市",
            "城市": "北京市",
            "天气": "晴",
            "最高温度": "11",
            "最低温度": "1",
            "湿度": "55"
        }
    """

    #  大模型查询
    info = get_answer_info(question)
    # 定义一个查询条件的列表，包含所有可能的查询条件
    query_conditions = [info]
    # 遍历所有查询条件，尝试获取法院信息
    for query in query_conditions:
        legal_info = get_temp_info(query_conds=query, need_fields=[])
        if legal_info:
            return json.dumps(legal_info, ensure_ascii=False)

    # 如果没有找到任何信息，返回错误消息
    return "查找不到该地址和日期的天气信息"


if __name__ == "__main__":
    # print(get_address_info_service("保定市天威西路2222号"))
    print(
        get_temp_info_service(
            "2021年8月19日这一天,这个地址的上海市闵行区新骏环路138号1幢401室的天气如何?其最高温度和最低温度分别是多少?然后在帮我查下这个地址的区县名称以及他的区县区划代码?"
        )
    )
