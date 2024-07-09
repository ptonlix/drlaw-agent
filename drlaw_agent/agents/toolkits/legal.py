from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from drlaw_agent.services.legal_service import (
    get_legal_document_service,
    get_legal_document_about_company_service,
    get_legal_document_about_accused_service,
    get_legal_document_about_amount_service,
)


class CompanyNameInput(BaseModel):
    company_name: str = Field(description="公司名称")


class LegalNameInput(BaseModel):
    legal_name: str = Field(description="案号名称")


class LegalAccusedInput(BaseModel):
    company_name: str = Field(description="公司名称")
    prosecute_year: str = Field(default="", description="起诉(立案)年份")


class LegalAmountInput(BaseModel):
    company_name: str = Field(description="公司名称")
    maximum: str = Field(default="-1", description="涉案金额过滤最大值")
    minimum: str = Field(default="-1", description="涉案金额过滤最小值")


get_legal_document_service_tool = StructuredTool.from_function(
    func=get_legal_document_service,
    name="get_legal_document_service_tool",
    args_schema=LegalNameInput,
)


get_legal_document_about_company_service_tool = StructuredTool.from_function(
    func=get_legal_document_about_company_service,
    name="get_legal_document_about_company_service_tool",
    args_schema=CompanyNameInput,
)

get_legal_document_about_accused_service_tool = StructuredTool.from_function(
    func=get_legal_document_about_accused_service,
    name="get_legal_document_about_accused_service_tool",
    args_schema=LegalAccusedInput,
)

get_legal_document_about_amount_service_tool = StructuredTool.from_function(
    func=get_legal_document_about_amount_service,
    name="get_legal_document_about_amount_service_tool",
    args_schema=LegalAmountInput,
)

legal_info_tools = [
    get_legal_document_service_tool,
    get_legal_document_about_company_service_tool,
    get_legal_document_about_accused_service_tool,
    get_legal_document_about_amount_service_tool,
]
