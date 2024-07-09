from typing import TypedDict, List
from typing import Annotated
import operator
from langgraph.graph.message import add_messages


class DrlawState(TypedDict):
    task: dict
    messages: Annotated[list, add_messages]
    agent_type: str  # 选择哪个助手
    sub_query: Annotated[list, operator.add]
    answer: str  # 问题答案
    call_agents: Annotated[list, operator.add]  # 记录询问的助理
