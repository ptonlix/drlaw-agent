from typing import TypedDict, List


class ResearchState(TypedDict):
    task: dict
    toolkits: List[str]  # 选择的查询工具
    tool_select_context: str  # 工具选择上下文
    answer: str  # 问题答案
    iferror: bool  # 是否发生错误
    errorinfo: str
    reselect_num: int
    review: bool  # 答案检查结果
    review_reason: str  # 理由
