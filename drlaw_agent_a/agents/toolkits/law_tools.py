from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from drlaw_agent_a.services.law_service import (
    get_amount_involved_by_case_num_service,
    get_legal_document_service,
    count_case_number_by_cause_service,
    search_case_num_by_legal_document_service,
    count_plaintiff_lawyer_service,
    count_defendant_lawyer_service,
    get_legal_basis_by_case_num_service,
    compare_amount_involved_by_two_case_num_service,
)


class CaseNumInput(BaseModel):
    case_num: str = Field(description="案号")


class CaseCompareAmountInput(BaseModel):
    case_num_one: str = Field(description="案号一")
    case_num_two: str = Field(description="案号二")


class CauseOfActionInput(BaseModel):
    cause_of_action: str = Field(description="案由")


class PlaintiffInput(BaseModel):
    plaintiff: str = Field(description="原告")


class DefendantInput(BaseModel):
    defendant: str = Field(description="被告")


class KeyValueInput(BaseModel):
    key: str = Field(description="键")
    value: str = Field(description="值")


get_amount_by_case = StructuredTool.from_function(
    func=get_amount_involved_by_case_num_service,
    name="get_amount_by_case",
    args_schema=CaseNumInput,
)

get_legal_document_getter = StructuredTool.from_function(
    func=get_legal_document_service,
    name="get_legal_document_getter",
    description="""
    根据案号获得该案所有基本信息，包括'判决结果','原告','原告律师','审理法条依据',
    '文书类型','文件名','标题','案由','涉案金额','胜诉方','被告','被告律师'。
    """,
    args_schema=CaseNumInput,
)

get_case_number_counter_by_cause = StructuredTool.from_function(
    func=count_case_number_by_cause_service,
    name="get_case_number_counter_by_cause",
    args_schema=CauseOfActionInput,
)

get_case_num_retriever_by_legal_document = StructuredTool.from_function(
    func=search_case_num_by_legal_document_service,
    name="get_case_num_retriever_by_legal_document",
    args_schema=KeyValueInput,
)

get_plaintiff_lawyer_counter = StructuredTool.from_function(
    func=count_plaintiff_lawyer_service,
    name="get_plaintiff_lawyer_counter",
    args_schema=PlaintiffInput,
)

get_defendant_lawyer_counter = StructuredTool.from_function(
    func=count_defendant_lawyer_service,
    name="get_defendant_lawyer_counter",
    args_schema=DefendantInput,
)

get_legal_basis_by_case_num = StructuredTool.from_function(
    func=get_legal_basis_by_case_num_service,
    name="get_legal_basis_by_case_num",
    args_schema=CaseNumInput,
)

compare_amount_involved_by_two_case_num = StructuredTool.from_function(
    func=compare_amount_involved_by_two_case_num_service,
    name="compare_amount_involved_by_two_case_num",
    args_schema=CaseCompareAmountInput,
)

company_law_tools = [
    get_amount_by_case,
    get_legal_document_getter,
    get_case_number_counter_by_cause,
    get_case_num_retriever_by_legal_document,
    get_plaintiff_lawyer_counter,
    get_defendant_lawyer_counter,
    get_legal_basis_by_case_num,
    compare_amount_involved_by_two_case_num,
]
