from drlaw_agent.agents.utils.views import print_agent_output
from drlaw_agent.agents.utils.model import check_agenttype_service_exists
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from datetime import datetime


SYSTEM_MESSAGE = """你是一个法律机构内的专业客服，擅长回答客户提出的公司和法律信息的问题，你能够将根据用户的问题，分解成不同的子问题，
分别向不同的助理询问信息，直至收集到足够的信息，能完整回答用户问题，提升用户的满意度。

你有以下助理：
1. 公司信息助理:能根据公司名称提供给该公司的基本信息，包含子公司和母公司等详情
2. 案件信息助理:能根据案件名称提供该案件的基本信息和根据公司名称、上市公司名称、公司简称、公司代码和统一信用代码查询该公司参与的案件有涉案次数、涉案金额总和涉案金额最高的案件信息和第二高的案件等信息
3. 法院信息助理:能根据法院名称法院代字提供该法院相关信息
4. 律师事务所信息助理:能根据律师事务所名称提供该律师事务所相关信息和统计数据
5. 限制高消费信息助理:能根据案件号和公司名称查询该案件或公司限制高消费的相关信息
6. 地理信息助理:能根据根据地址查该地址对应的省份城市区县和获取该客户问题中指定日期的天气情况
7. 公司数据报告写作助理:能够根据要求收集公司的数据，写作这个公司数据整合报告
8. 起诉状信息收集与写作助理:能根据针对公司法人起诉公司法人、公司法人起诉公司、公司起诉公司法人、公司起诉公司这四种起诉场景收集相关信息并写作起诉状。用户要求写起诉状，直接询问他即可。
9. API调用信息助理:能够统计各个助理在检索信息过程中调用的API类型和次数

根据客户问题和已知信息，你需要判断需要向哪一个助理询问,一次能向一位助理询问，不允许超过一位。
"#"这个符号表示询问，询问格式为:
#公司信息助理: XXX
输出例子: #案件信息助理: 上海晨光文具股份有限公司的涉案次数为？（起诉日期在2020年）作为被起诉人的次数及总金额为？

根据获取的助理提供的信息，你需要判断是否可以完整回答该问题，如果可以则回复客户。
"@"这个符号表示可以回复客户，如下格式：
@客户: XXX

注意事项：
1.必须遵从以上规则,"#"和"@"这两个符号每次回答中必须要使用

当前日期：{current_date}
"""

USER_MESSAGE = """

"""


class AssistanterAgent:
    """
    助理智能体，专门根据负责向其它智能体询问问题,并生成最终答案
    """

    def __init__(self):
        pass

    async def call_assistant(self, drlaw_state: dict) -> str:
        # task = drlaw_state.get("task")
        # query = task.get("query")
        history_message = drlaw_state.get("messages")
        print(history_message)
        prompt = ChatPromptTemplate.from_messages(history_message)

        need_assistant = (
            prompt
            # | ChatOpenAI(model=task.get("model"), temperature=0.1)
            | ChatOpenAI(
                model="glm-4-0520",
                temperature=0.95,
                max_tokens=4095,
                model_kwargs={
                    "tools": [
                        {
                            "type": "web_search",
                            "web_search": {
                                "enable": False  # 禁用：False，启用：True，默认为 True。
                            },
                        }
                    ],
                },
            )
            | StrOutputParser()
        )
        print_agent_output("助理正在思考询问信息", agent="ASSISTANT")
        result = need_assistant.invoke({})
        return result

    async def run(self, drlaw_state: dict):
        if not drlaw_state.get("messages"):
            task = drlaw_state.get("task")
            query = task.get("query")
            return {
                "messages": [
                    (
                        "system",
                        SYSTEM_MESSAGE.format(current_date=datetime.now().isoformat()),
                    ),
                    ("human", query),
                ],
                "agent_type": "客服助理",
            }
        if drlaw_state.get("agent_type") == "错误信息助理":
            return drlaw_state

        result = await self.call_assistant(drlaw_state)
        sub_query = ""
        answer = ""
        print_agent_output(f"助理下一步计划:\n{result}", agent="ASSISTANT")
        if "#" in result:
            info_split = result.split("#")
            agent_info = info_split[1]  # 获取第一个询问信息
            agent_type = agent_info.split(":")[0]  # 获取第一个询问助理类型
            sub_query = agent_info.split(":")[1]
            print_agent_output(
                f"助理下一步需要询问助理: {agent_type}", agent="ASSISTANT"
            )
        elif "@" in result:  # 结束
            info_split = result.split("@")
            agent_info = info_split[1]
            agent_type = agent_info.split(":")[0]  # 获取第一个询问助理类型
            answer = agent_info.split(":")[1]  # 获取答案
            print_agent_output(
                f"客服助理已知道答案，提供给: {agent_type}", agent="ASSISTANT"
            )
        elif ":" in result:
            agent_info = result
            agent_type = result.split(":")[0]
            sub_query = agent_info.split(":")[1]
            print_agent_output(
                f"助理下一步需要询问助理: {agent_type}", agent="ASSISTANT"
            )
        else:
            # 出错记录，由错误处理助理进行操作
            agent_info = "未询问助理也未生成答案:\n" + result
            agent_type = "错误信息助理"

        if not check_agenttype_service_exists(agent_type):
            # 出错记录，助理类型不存在
            agent_info = "助理类型不存在:\n" + result
            agent_type = "错误信息助理"

        return {
            "messages": [("ai", agent_info)],
            "agent_type": agent_type,
            "call_agents": [agent_type],
            "sub_query": [sub_query.strip()],
            "answer": answer.strip(),
        }


if __name__ == "__main__":
    import asyncio

    a = AssistanterAgent()
    asyncio.run(
        a.run(
            {
                "task": {
                    "query": "通过案号(2019)鄂0103民初12292号，可否请您协助查询一下该判决所依据的法律条文？"
                }
            }
        )
    )
