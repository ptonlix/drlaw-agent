from typing import TypedDict, List


class ReportState(TypedDict):
    task: dict
    company_info: List[dict]
    sub_company_info: List[dict]
    legal_info: List[dict]
    xzgxf_info: List[dict]
