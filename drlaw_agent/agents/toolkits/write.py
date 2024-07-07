from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from drlaw_agent.services.write_service import (
    save_dict_list_to_word_service,
    get_company_sue_company_service,
    get_citizens_sue_citizens_service,
    get_company_sue_citizens_service,
    get_citizens_sue_company_service,
)


save_dict_list_to_word_service_tool = StructuredTool.from_function(
    func=save_dict_list_to_word_service,
    name="save_dict_list_to_word_service_tool",
    args_schema=CompanyNameInput,
)
