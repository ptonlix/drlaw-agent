from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from drlaw_agent.services.lawfirm_service import (
    get_lawfirm_info_service,
    get_lawfirm_log_service,
)


class LawfirmNameInput(BaseModel):
    lawfirm_name: str = Field(description="律师事务所名称")


get_lawfirm_info_service_tool = StructuredTool.from_function(
    func=get_lawfirm_info_service,
    name="get_lawfirm_info_service_tool",
    args_schema=LawfirmNameInput,
)


get_lawfirm_log_service_tool = StructuredTool.from_function(
    func=get_lawfirm_log_service,
    name="get_lawfirm_log_service_tool",
    args_schema=LawfirmNameInput,
)

court_info_tools = [
    get_lawfirm_info_service_tool,
    get_lawfirm_log_service_tool,
]
