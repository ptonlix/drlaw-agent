from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from drlaw_agent_a.services.company_info_service import (
    get_company_info_service,
    count_company_by_industry_service,
    search_company_name_by_info_service,
)


class CompanyNameInput(BaseModel):
    company_name: str = Field(description="公司名称")


class IndustryNameInput(BaseModel):
    industry_name: str = Field(description="行业名称")


class KeyValueInput(BaseModel):
    key: str = Field(description="键")
    value: str = Field(description="值")


get_company_info_by_service = StructuredTool.from_function(
    func=get_company_info_service,
    name="get_company_info_by_service",
    args_schema=CompanyNameInput,
)

get_company_counter_by_industry = StructuredTool.from_function(
    func=count_company_by_industry_service,
    name="get_company_counter_by_industry",
    args_schema=IndustryNameInput,
)

get_company_name_retriever_by_info = StructuredTool.from_function(
    func=search_company_name_by_info_service,
    name="get_company_name_retriever_by_info",
    args_schema=KeyValueInput,
)

com_info_tools = [
    get_company_info_by_service,
    get_company_counter_by_industry,
    get_company_name_retriever_by_info,
]
