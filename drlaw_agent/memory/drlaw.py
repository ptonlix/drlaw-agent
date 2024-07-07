from typing import TypedDict, List


class DrlawState(TypedDict):
    task: dict
    agent_type: str  # 选择哪个助手
    answer: str  # 问题答案
    iferror: bool  # 是否发生错误
    errorinfo: str
    reselect_num: int
    review: bool  # 答案检查结果
    review_reason: str  # 理由
