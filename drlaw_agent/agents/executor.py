from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import List
from datetime import datetime
import importlib
from colorama import Fore, Style
from drlaw_agent.agents.utils.views import print_agent_output

TOOL_CALL_ERROR_MESSAGE = """
用户查询问题:
我想了解天味食品的法定代表人、注册地和电子邮箱分别为何？

注意: 请不要直接返回如下工具调用信息给用户,应该需要通过你自身tool_calls来传递
company_name_retriever_by_info
```python
tool_call()
```
"""


class ExecutorAgent:

    def __init__(self):
        pass

    def create_assistant_graph(
        self, model: str, temperature: float, tools: List[str], tool_select_context: str
    ) -> AgentExecutor:
        """
        通过提供的工具查询接口，生成一位智能金融法律助理
        参数： tools:工具名称
        """

        toolkits = importlib.import_module("drlaw_agent.agents.toolkits")

        agent_tools = [getattr(toolkits, tool) for tool in tools]
        system_message = "你是一个擅长回答金融和法律有关的问题的专家，会通过调用工具来检索信息对问题作出回答，必须回答不能放弃。如果是开放性问题,请结合自身知识进行回答。"

        model = ChatOpenAI(model=model, temperature=temperature, max_tokens=8192)
        app = create_react_agent(model, agent_tools, system_message, debug=True)
        return app

    def answer_by_llm(self, model: str, query: str) -> str:
        SYSTEM_MESSAGE = "你是一个擅长回答金融和法律有关的问题的专家，会利用自己能力来检索信息，通过一步一步拆解并分析问题，最终得出最准确的答案。\n当前日期:{current_date}"

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_MESSAGE),
                ("human", "{query}"),
            ]
        ).partial(
            current_date=datetime.now().isoformat(),
        )

        answer = prompt | ChatOpenAI(model=model, temperature=0.1) | StrOutputParser()

        return answer.invoke({"query": query})

    async def produce_assistant(self, research_state: dict):
        task = research_state.get("task")
        toolkits = research_state.get("toolkits")
        tool_select_context = research_state.get("tool_select_context")

        query = task.get("query")
        model_name = task.get("model")
        temperature = task.get("temperature")
        recursion_limit = task.get("recursion_limit")
        print_agent_output(
            f"Running produce_assistant on the following query and tools:\n {query} \n {toolkits}",
            agent="EXECUTOR",
        )

        dragent = self.create_assistant_graph(
            model_name, temperature, toolkits, tool_select_context
        )

        try:
            messages = dragent.invoke(
                {"messages": [("human", query)]},
                {"recursion_limit": recursion_limit},
            )
            answer = messages["messages"][-1].content
            if "tool_call" in answer:
                raise Exception(answer)
            elif "很抱歉" in answer:
                return {
                    "task": task,
                    "answer": answer,
                    "toolkits": toolkits,
                    "tool_select_context": tool_select_context,
                    "reselect_num": research_state.get("reselect_num"),
                }
            return {
                "task": task,
                "answer": answer,
                "toolkits": toolkits,
                "tool_select_context": tool_select_context,
                "reselect_num": research_state.get("reselect_num"),
            }
        except Exception as e:
            print(f"{Fore.RED}Error in answer questiong {query}: {e}{Style.RESET_ALL}")
            return {
                "task": task,
                "reselect_num": research_state.get("reselect_num"),
            }
