from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from drlaw_agent.services.company_service import (
    get_company_register_name_service,
    get_company_info_service,
    get_parent_company_info_service,
    get_sub_company_info_list_service,
)


class CompanyNameInput(BaseModel):
    company_name: str = Field(description="公司名称")


class CompanySocialCodeInput(BaseModel):
    company_social_code: str = Field(description="公司统一信用代码")


get_company_register_name_service_tool = StructuredTool.from_function(
    func=get_company_register_name_service,
    name="get_company_register_name_service_tool",
    args_schema=CompanySocialCodeInput,
)


get_company_info_service_tool = StructuredTool.from_function(
    func=get_company_info_service,
    name="get_company_info_service_tool",
    args_schema=CompanyNameInput,
)


get_parent_company_info_service_tool = StructuredTool.from_function(
    func=get_parent_company_info_service,
    name="get_parent_company_info_service_tool",
    args_schema=CompanyNameInput,
)

get_sub_company_info_list_service_tool = StructuredTool.from_function(
    func=get_sub_company_info_list_service,
    name="get_sub_company_info_list_service_tool",
    args_schema=CompanyNameInput,
)

com_info_tools = [
    get_company_register_name_service_tool,
    get_company_info_service_tool,
    get_parent_company_info_service_tool,
    get_sub_company_info_list_service_tool,
]
