from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from colorama import Fore, Style
from drlaw_agent.agents.utils.views import print_agent_output
from drlaw_agent.agents.toolkits.api import api_info_tools


class ApiAgent:
    """
    API调用信息助理:
    能够统计各个助理在检索信息过程中调用的API类型和次数
    """

    def __init__(self):
        pass

    async def run(self, drlaw_state: dict):
        print_agent_output("API调用信息助理正在查询信息", agent="APIER")

        task = drlaw_state.get("task")
        recursion_limit = task.get("recursion_limit")
        # complete_query = task.get("query")  # 完整问题
        query = drlaw_state.get("sub_query")[-1]  # 子查询

        system_message = """你是一个擅长回答与API调用信息有关的问题的专家，会通过调用工具来检索信息。
如果遇到比较复杂的复合问题，你可以先拆解成多个小问题，然后依次回答小问题，最后将多个小问题的答案组合起来回答整个问题。
如果遇到开放问题，你可以自由作答。
"""

        model = ChatOpenAI(
            model="glm-4",
            temperature=0.1,
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
        app = create_react_agent(model, api_info_tools, system_message, debug=True)

        try:
            messages = app.invoke(
                {"messages": [("human", query)]},
                {"recursion_limit": recursion_limit},
            )
            answer = messages["messages"][-1].content
            if "tool_call" in answer:
                raise Exception(answer)
            return {
                "messages": [
                    (
                        "human",
                        f"#客服助理:{answer}",
                    )
                ],
                "agent_type": "客服助理",
            }
        except Exception as e:
            print(f"{Fore.RED}Error in answer questiong {query}: {e}{Style.RESET_ALL}")
            agent_info = f"{self.__class__.__name__}出错:\n {query}: {e}"
            return {
                "messages": [("human", agent_info)],
                "agent_type": "错误信息助理",
            }
