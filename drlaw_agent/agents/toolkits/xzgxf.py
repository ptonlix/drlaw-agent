from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from drlaw_agent.services.xzgxf_service import (
    get_xzgxf_info_service,
    get_xzgxf_info_list_service,
)


class LegalNameInput(BaseModel):
    legal_name: str = Field(description="案号名称")


class CompanyNameInput(BaseModel):
    company_name: str = Field(description="公司名称")


get_xzgxf_info_service_tool = StructuredTool.from_function(
    func=get_xzgxf_info_service,
    name="get_xzgxf_info_service_tool",
    args_schema=LegalNameInput,
)


get_xzgxf_info_list_service_tool = StructuredTool.from_function(
    func=get_xzgxf_info_list_service,
    name="get_xzgxf_info_list_service_tool",
    args_schema=CompanyNameInput,
)

xzgxf_info_tools = [
    get_xzgxf_info_service_tool,
    get_xzgxf_info_list_service_tool,
]
