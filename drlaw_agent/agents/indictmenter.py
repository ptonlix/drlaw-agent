from drlaw_agent.agents.utils.views import print_agent_output
import jsonlines


class IndictmenterAgent:
    """
    起诉状写作助理:
    能根据针对公民起诉公民、公民起诉公司、公司起诉公民、公司起诉公司四种场景写作不同的起诉状
    """

    def __init__(self):
        pass

    async def run(self, drlaw: dict):
        print_agent_output("起诉状写作助理正在编写起诉状", agent="INDICTMENTER")
        # 提取问题中关键信息
        # 调用工具获取信息
        # 返回起诉状字符串
        return {"messages": [("human", "案件信息")]}
