from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from drlaw_agent.services.court_service import (
    get_court_info_service,
    get_court_code_service,
)


class CourtNameInput(BaseModel):
    court_name: str = Field(description="法院名称")


get_court_info_service_tool = StructuredTool.from_function(
    func=get_court_info_service,
    name="get_court_info_service_tool",
    args_schema=CourtNameInput,
)


get_court_code_service_tool = StructuredTool.from_function(
    func=get_court_code_service,
    name="get_court_code_service_tool",
    args_schema=CourtNameInput,
)

court_info_tools = [
    get_court_info_service_tool,
    get_court_code_service_tool,
]
