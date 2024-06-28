from colorama import Fore, Style
from .utils.views import print_agent_output
from datetime import datetime
import re
from ast import literal_eval
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain_core.tools import BaseTool
from drlaw_agent.agents.toolkits import (
    com_info_tools,
    com_register_tools,
    sub_com_info_tools,
    company_law_tools,
)

USER_MESSAGE = """
当前日期：{current_date}

用户查询问题:
{query}

当前回答:
{answer}

你是一个专业的金融和法律信息检查员,需要分析用户输入的查询问题,检查当前回答是否能解答完全用户的问题
如果能请回复“可以”，如果不能，请回复“不可以”，并阐述理由
"""


class ReviewerAgent:
    def __init__(self):
        self.all_tools = []

        self.all_tools.extend(com_info_tools)
        self.all_tools.extend(com_register_tools)
        self.all_tools.extend(sub_com_info_tools)
        self.all_tools.extend(company_law_tools)

    def get_toolkits_instructions(self, tools: List[BaseTool]) -> str:
        instructions = ""
        for i, tool in enumerate(tools):
            # tool_instructions = convert_to_openai_tool(tool)
            instructions += f"<tool id='{i}'>\n工具名称:{tool.name}\n工具描述:{tool.description}\n</tool>\n"
        return instructions

    def get_toolkit_name_list(self, tools: List[BaseTool]) -> list[str]:
        return [tool.name for tool in tools]

    async def answer_review(self, research_state: dict):
        task = research_state.get("task")
        query = task.get("query")
        answer = research_state.get("answer")
        toolkits = research_state.get("toolkits")
        tool_select_context = research_state.get("tool_select_context")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("human", USER_MESSAGE),
            ]
        ).partial(
            current_date=datetime.now().isoformat(),
            toolkits=self.get_toolkits_instructions(self.all_tools),
        )

        need_review = (
            prompt
            | ChatOpenAI(model=task.get("model"), temperature=0.1)
            | StrOutputParser()
        )
        print_agent_output("正在检查问题的回答是否满意", agent="REVIEWER")
        review_result = need_review.invoke({"query": query, "answer": answer})

        print(
            f"{Fore.GREEN}Question:\n{query}\n Answer:\n{answer}\n Review Result:\n{review_result} {Style.RESET_ALL}"
        )

        review_bool = not ("不可以" in review_result)

        reselect_num = research_state.get("reselect_num") + 1

        return {
            "task": task,
            "tool_select_context": tool_select_context,
            "toolkits": toolkits,
            "answer": answer,
            "review": review_bool,
            "review_reason": review_result,
            "reselect_num": research_state.get("reselect_num") + 1,
            "iferror": True if reselect_num > 2 else False,
        }
