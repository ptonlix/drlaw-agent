from drlaw_agent.agents.utils.views import print_agent_output
import jsonlines


class ReporterAgent:
    """
    公司数据报告写作助理:
    能够根据要求收集公司的数据，写作这个公司数据整合报告
    """

    def __init__(self):
        pass

    async def run(self, drlaw: dict):
        print_agent_output("公司数据报告写作助理正在编写起诉状", agent="REPORTER")
        # 提取问题中关键信息
        # 调用工具获取信息
        # 返回起诉状字符串
        return {"messages": [("human", "案件信息")]}
