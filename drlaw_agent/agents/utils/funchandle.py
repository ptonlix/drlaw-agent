from typing import Any, List
import re
from langchain_core.tools import StructuredTool


def parse_and_call_function(docstring: str, tools: List[StructuredTool]) -> Any:
    # 提取函数名和参数
    func_name_pattern = re.compile(r"(\w+)\n```python\ntool_call\((.*)\)\n```")
    match = func_name_pattern.search(docstring)

    if not match:
        return "Failed to parse the function name or parameters."

    func_name = match.group(1)
    params_str = match.group(2)

    # 提取参数并构造参数字典
    params = dict(re.findall(r"(\w+)='([^']+)'", params_str))

    # 查找并调用相应的工具
    for tool in tools:
        if func_name == tool.name:
            try:
                return tool.run(params)
            except Exception as e:
                return f"Function {func_name} call failed, error: {e}"

    return f"Function {func_name} does not exist."
