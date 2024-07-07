from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from drlaw_agent.services.address_service import (
    get_address_info_service,
    get_temp_info_service,
)


class AddressInput(BaseModel):
    address: str = Field(description="地理位置")


class QuestionInput(BaseModel):
    question: str = Field(description="提问的问题")


get_address_info_service_tool = StructuredTool.from_function(
    func=get_address_info_service,
    name="get_address_info_service_tool",
    args_schema=AddressInput,
)


get_temp_info_service_tool = StructuredTool.from_function(
    func=get_temp_info_service,
    name="get_temp_info_service_tool",
    args_schema=QuestionInput,
)

address_info_tools = [
    get_address_info_service_tool,
    get_temp_info_service_tool,
]
