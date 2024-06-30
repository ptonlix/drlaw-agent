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

SYSTEM_MESSAGE = """
当前日期：{current_date}

工具库:
```
{toolkits}
```

用户查询问题:
{query}

当前回答:
{now_answer}

当前回答不满意的理由
{review_reason}

你是一个专业的金融和法律信息检索员,需要分析用户输入的查询问题、当前的回答与不满意的理由，为了获取用户想要查询的答案,请务必根据以下要求，挑选合适查询工具:
1.学习工具库中工具名称、工具描述和参考例子
2.分析用户查询问题、当前的回答与不满意的理由,根据工具名称和工具描述，要按步骤输出工具调用过程
3.按照Python列表类型的形式输出整个过程所需要的工具的名称,一定不要返回工具调用的参数! 返回示例:["company_name_retriever_by_info", "company_counter_by_industry"]
4.如果用户查询问题为法律法规通识问题或金融监管上市公司等通识问题，比如: 1.简述侵犯著作权罪的客观行为 2.上市公司因涉嫌金融诈骗面临的法律风险有哪些等，这些不需要使用查询工具，必须返回空列表。

注意:你是挑选工具，不要回答问题
注意:返回的工具名称，必须是在工具库中，不能杜撰和错一个字母

"""


class ToolSelectAgent:
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

    def del_toolkit_name_list(
        self, tools: List[BaseTool], del_tools: List[str]
    ) -> List[BaseTool]:
        return [tool for tool in tools if tool.name not in del_tools]

    def check_tools(self, select_tools: List[str]) -> List[str]:
        # 检查如果出现多个get_parent_company_info_getter 时合并成一个get_multiple_parent_company_info_getter
        if select_tools.count("get_parent_company_info_getter") > 1:
            while "get_parent_company_info_getter" in select_tools:
                select_tools.remove("get_parent_company_info_getter")
            select_tools.append("get_multiple_parent_company_info_getter")

        # 检查如果出现get_sub_company_info_getter,换成投资信息查询get_company_investment_information_getter
        if "get_sub_company_info_getter" in select_tools:
            while "get_sub_company_info_getter" in select_tools:
                select_tools.remove("get_sub_company_info_getter")
            select_tools.append("get_company_investment_information_getter")

        # 检查如果出现get_sub_company_of_largest_holding_ratio_getter，则不需要get_all_sub_company_counter
        if (
            "get_sub_company_of_largest_holding_ratio_getter" in select_tools
            and "get_all_sub_company_counter" in select_tools
        ):
            select_tools.remove("get_all_sub_company_counter")

        return select_tools

    async def tool_select(self, research_state: dict):
        task = research_state.get("task")
        query = task.get("query")

        now_toolkits = (
            research_state.get("toolkits") if research_state.get("toolkits") else []
        )
        now_answer = (
            research_state.get("answer") if research_state.get("answer") else ""
        )
        review_reason = (
            research_state.get("review_reason")
            if research_state.get("review_reason")
            else ""
        )

        # parser = PydanticOutputParser(pydantic_object=NeedTools)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("human", SYSTEM_MESSAGE),
            ]
        ).partial(
            current_date=datetime.now().isoformat(),
            toolkits=self.get_toolkits_instructions(
                self.del_toolkit_name_list(self.all_tools, now_toolkits)
            ),
            now_answer=now_answer,
            review_reason=review_reason,
        )

        need_tools = (
            prompt
            | ChatOpenAI(model=task.get("model"), temperature=0.1)
            # | ChatOpenAI(model="glm-4-air", temperature=0.1)
            | StrOutputParser()
        )
        print_agent_output("正在从工具库选取工具", agent="TOOLSELECT")
        reasoning = need_tools.invoke(
            {
                "query": query,
            }
        )

        pattern = r"(\[.*?\])"
        match = re.search(pattern, reasoning)
        if match:
            list_str = match.group(1)
            # 将提取的字符串转换为list实例
            toolkits = literal_eval(list_str)
            # 确保工具是在生成工具中
            toolkits = [
                tool
                for tool in toolkits
                if tool in self.get_toolkit_name_list(self.all_tools)
            ]
            # 为大模型打补丁
            toolkits = self.check_tools(toolkits)
        else:
            toolkits = []

        print(
            f"{Fore.GREEN}Question:\n{query}\n\nSelect Tool Reason: \n{reasoning}\n\n Select Tool:\n {toolkits}{Style.RESET_ALL}"
        )

        now_toolkits.extend(toolkits)
        reselect_num = research_state.get("reselect_num")
        print(reselect_num)
        return {
            "task": task,
            "tool_select_context": reasoning,
            "toolkits": now_toolkits,
            "reselect_num": reselect_num if reselect_num else 0,
        }
