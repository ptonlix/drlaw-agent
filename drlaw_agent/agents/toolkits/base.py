from typing import List
from langchain_core.tools import BaseTool


def get_toolkits_instructions(tools: List[BaseTool]) -> str:
    instructions = ""
    for i, tool in enumerate(tools):
        # tool_instructions = convert_to_openai_tool(tool)
        instructions += f"<tool id='{i}'>\n工具名称:{tool.name}\n工具描述:{tool.description}\n</tool>\n"
    return instructions


def get_toolkit_name_list(tools: List[BaseTool]) -> list[str]:
    return [tool.name for tool in tools]
