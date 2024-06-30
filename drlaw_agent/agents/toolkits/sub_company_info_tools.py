from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from drlaw_agent.services.sub_company_info_service import (
    get_parent_company_info_service,
    get_sub_company_name_service,
    count_sub_company_service,
    # search_company_name_by_super_info_service,
    query_total_amount_invested_in_subsidiaries,
    search_company_name_by_stock_bref,
    get_company_investment_information,
    get_multiple_parent_company_info_service,
    get_sub_company_info_service,
    get_sub_company_of_largest_holding_ratio,
    get_holding_sub_company,
)


class CompanyNameInput(BaseModel):
    company_name: str = Field(description="公司名称")


class CompanyInvestment(BaseModel):
    company_name: str = Field(description="公司名称")
    holding_ratio: str = Field(default="0", description="公司的控股比例")
    investment_amount: str = Field(default="0万", description="投资金额")


class CompanyMultipleNameInput(BaseModel):
    company_name_list: list[str] | dict = Field(description="多个公司名称列表")


class KeyValueInput(BaseModel):
    key: str = Field(description="键")
    value: str = Field(description="值")


get_parent_company_info_getter = StructuredTool.from_function(
    func=get_parent_company_info_service,
    name="get_parent_company_info_getter",
    args_schema=CompanyNameInput,
)

get_sub_company_name_getter = StructuredTool.from_function(
    func=get_sub_company_name_service,
    name="get_sub_company_name_getter",
    args_schema=CompanyNameInput,
)

get_sub_company_info_getter = StructuredTool.from_function(
    func=get_sub_company_info_service,
    name="get_sub_company_info_getter",
    args_schema=CompanyNameInput,
)

get_all_sub_company_counter = StructuredTool.from_function(
    func=count_sub_company_service,
    name="get_all_sub_company_counter",
    args_schema=CompanyInvestment,
)

# get_company_name_retriever_by_super_info = StructuredTool.from_function(
#     func=search_company_name_by_super_info_service,
#     name="get_company_name_retriever_by_super_info",
#     args_schema=KeyValueInput,
# )

get_total_amount_invested_in_subsidiaries_getter = StructuredTool.from_function(
    func=query_total_amount_invested_in_subsidiaries,
    name="get_total_amount_invested_in_subsidiaries_getter",
    args_schema=CompanyNameInput,
)
search_company_name_by_stock_bref_getter = StructuredTool.from_function(
    func=search_company_name_by_stock_bref,
    name="search_company_name_by_stock_bref_getter",
    args_schema=CompanyNameInput,
)

get_company_investment_information_getter = StructuredTool.from_function(
    func=get_company_investment_information,
    name="get_company_investment_information_getter",
    args_schema=CompanyInvestment,
)

get_multiple_parent_company_info_getter = StructuredTool.from_function(
    func=get_multiple_parent_company_info_service,
    name="get_multiple_parent_company_info_getter",
    args_schema=CompanyMultipleNameInput,
)

get_sub_company_of_largest_holding_ratio_getter = StructuredTool.from_function(
    func=get_sub_company_of_largest_holding_ratio,
    name="get_sub_company_of_largest_holding_ratio_getter",
    args_schema=CompanyNameInput,
)

get_holding_sub_company_getter = StructuredTool.from_function(
    func=get_holding_sub_company,
    name="get_holding_sub_company_getter",
    args_schema=CompanyNameInput,
)


sub_com_info_tools = [
    get_parent_company_info_getter,
    get_multiple_parent_company_info_getter,
    get_sub_company_name_getter,
    get_sub_company_info_getter,
    get_all_sub_company_counter,
    # get_company_name_retriever_by_super_info,
    get_total_amount_invested_in_subsidiaries_getter,
    search_company_name_by_stock_bref_getter,
    get_company_investment_information_getter,
    get_sub_company_of_largest_holding_ratio_getter,
    get_holding_sub_company_getter,
]
