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
    iferror: bool  # 是否发生错误
    errorinfo: str
    reselect_num: int
    review: bool  # 答案检查结果
    review_reason: str  # 理由
