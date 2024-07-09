from langchain_core.tools import StructuredTool

from drlaw_agent.services.api_service import (
    get_api_info_service,
)

get_api_info_service_tool = StructuredTool.from_function(
    func=get_api_info_service,
    name="get_address_info_service_tool",
)

api_info_tools = [
    get_api_info_service_tool,
]
