from drlaw_agent.agents.utils.views import print_agent_output
from drlaw_agent.services.write_service import save_dict_list_to_word_service
from drlaw_agent.utils import convert_to_float
from drlaw_agent.services.company_service import (
    get_company_register_service,
    get_sub_company_info_list_service_for_report,
)
from drlaw_agent.services.legal_service import (
    get_legal_document_list_service,
    extract_year_and_code,
)
from drlaw_agent.services.xzgxf_service import get_xzgxf_info_service_for_report
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
import json
from json.decoder import JSONDecodeError
import re
from datetime import datetime
from colorama import Fore, Style
from typing import List
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)

SYSTEM_MESSAGE = """你是一个企业数据报告生成专家，专门帮助客户收集企业数据并生成企业报告。你需要从遵从以下工作流程
1. 用户请求提取出如下关键信息: 公司名称、是否需要工商信息、是否需要公司简介、用于筛选子公司的投资金额、是否是全资子公司、案件审理年份、案件立案年份、用户筛选案件的涉案金额、是否需要限制高消费信息、

公司名称记为:company_name、是否需要工商信息记为ifcommerce、是否需要公司简介记为ifintro、
用于筛选子公司的投资金额记为over_investment、是否是全资子公司记为wholly_owned、 案件审理年份记为hear_year、案件立案年份记为prosecute_year、用户筛选案件的涉案金额记为over_legal_money
是否需要限制高消费信息记为ifxzgxf
注意: 1.相关关键信息在用户输入中未提及,则标记为空字符串 2.over_investment 和 over_legal_money 只需要填写金额即可，本身他们就是大于的意思，比如过亿就是1亿,大于10万就是10万

结果输出: 将以上关键信息整理成JSON格式,如以下格式:
```json
{{
    "company_name": "string",
    "ifcommerce":"string",
    "ifintro":"string",
    "over_investment": "string",
    "wholly_owned": "string",
    "hear_year":"string",
    "prosecute_year": "string",
    "over_legal_money": "string",
    "ifxzgxf":string
}}

例如: 用户请求: 报告龙建路桥股份有限公司关于工商信息（不包括公司简介）及投资金额过亿的全资子公司，母公司及子公司的立案时间在2019年涉案金额不为0的裁判文书（不需要判决结果）整合。
输出关键信息为:
```json
{{
    "company_name": "龙建路桥股份有限公司",
    "ifcommerce":"是",
    "ifintro":"否",
    "over_investment":"1亿",
    "wholly_owned":"是",
    "hear_year":"",
    "prosecute_year":"2019年"
    "over_legal_money":"0元"
    "ifxzgxf":""
}}
```
"""


class ReportModel:
    company_name: str
    ifcommerce: str
    ifintro: str
    over_investment: str
    wholly_owned: str
    prosecute_year: str
    over_legal_money: str


class ReporterAgent:
    """
    公司数据报告写作助理:
    能够根据要求收集公司的数据，写作这个公司数据整合报告
    """

    def __init__(self): ...

    def fix_json(self, json_str: str) -> dict:
        # 使用正则表达式替换掉重复的逗号
        fixed_json_str = re.sub(r",\s*}", "}", json_str)
        fixed_json_str = re.sub(r",\s*]", "]", fixed_json_str)

        # 尝试加载修复后的JSON字符串
        return json.loads(fixed_json_str)

    def zhipu_output_handle(self, output: str) -> dict:
        try:
            # 找到json子串并加载为字典
            start_index = output.find("{")
            end_index = output.rfind("}") + 1
            json_str = output[start_index:end_index]

            # 加载为字典
            return json.loads(json_str)
        except JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return self.fix_json(json_str)

    def get_company_info(self, company_name: str, ifintro: str) -> List[dict]:
        reg_info = get_company_register_service(company_name=company_name)
        reg_info = json.loads(reg_info)
        if ifintro == "否":  # 明确不带公司简介再去掉
            reg_list = [
                {k: v for k, v in d.items() if k != "企业简介"} for d in reg_info
            ]
        else:
            reg_list = reg_info
        return reg_list

    def get_subcompany_info(
        self, company_name: str, over_investment: str, wholly_owned: str
    ) -> List[dict]:
        subcompany_info = json.loads(
            get_sub_company_info_list_service_for_report(company_name)
        )
        wholly_owned_info = []
        over_investment_info = []
        intersection = []
        if wholly_owned == "是":
            wholly_owned_info = [
                sub_company
                for sub_company in subcompany_info
                if sub_company["上市公司参股比例"] == "100.0"
            ]

        if over_investment:
            over_investment_info = [
                sub_company
                for sub_company in subcompany_info
                if convert_to_float(sub_company["上市公司投资金额"]) > 1e8
            ]
        if wholly_owned_info and over_investment_info:
            # 将第二个列表转换为集合（每个元素是一个冻结的字典）
            set_dict = {frozenset(d.items()) for d in over_investment_info}

            # 找到交集
            intersection = [
                d for d in wholly_owned_info if frozenset(d.items()) in set_dict
            ]

            return intersection
        elif wholly_owned_info:
            return wholly_owned_info
        elif over_investment:
            return over_investment

        return subcompany_info

    def get_legal_info(
        self,
        parent_company_name: str,
        sub_company_list: List[dict],
        hear_year: str,
        prosecute_year: str,
        over_legal_money: str,
    ) -> List[dict]:
        company_names = []
        if sub_company_list:
            company_names = [c["公司名称"] for c in sub_company_list]
            company_names.append(sub_company_list[0]["关联上市公司全称"])
        else:
            company_names.append(parent_company_name)

        legal_info_list = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_index = {
                executor.submit(get_legal_document_list_service, company_name, []): i
                for i, company_name in enumerate(company_names)
            }

            for future in tqdm(
                as_completed(future_to_index),
                total=len(company_names),
                desc="Processing",
                unit="request",
            ):
                index = future_to_index[future]
                try:
                    result = future.result()
                    legal_info_list.extend(result)
                except Exception as e:
                    logger.error(
                        f"Failed to process get legal document at index {index}. Error: {e}"
                    )

        legal_info_list = [
            {k: v for k, v in d.items() if k != "判决结果"} for d in legal_info_list
        ]

        year_list = []
        over_legal_money_list = []
        if prosecute_year:  # 立案时间
            for info in legal_info_list:
                date_obj, _ = extract_year_and_code(info["案号"])  # 起诉时间
                if prosecute_year in date_obj:
                    year_list.append(info)
        elif hear_year:  # 审理时间
            for info in legal_info_list:
                # 将日期字符串转换为datetime对象
                date_obj = datetime.strptime(
                    info["日期"], "%Y-%m-%d %H:%M:%S"
                )  # 审理时间
                formatted_date = date_obj.strftime("%Y年%m月%d日")
                if hear_year in formatted_date:
                    year_list.append(info)

        if over_legal_money:
            over_legal_money_list = [
                i
                for i in legal_info_list
                if convert_to_float(i["涉案金额"]) > convert_to_float(over_legal_money)
            ]

        if (prosecute_year or hear_year) and over_legal_money:
            # 将第二个列表转换为集合（每个元素是一个冻结的字典）
            set_dict = {frozenset(d.items()) for d in over_legal_money_list}

            # 找到交集
            return [d for d in year_list if frozenset(d.items()) in set_dict]
        elif year_list:
            return year_list
        elif over_legal_money_list:
            return over_legal_money_list

        return legal_info_list

    def get_legal_xzgxf_info(self, legal_info: List[dict]) -> List[dict]:
        xzgxf_list = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_index = {
                executor.submit(get_xzgxf_info_service_for_report, legal["案号"]): i
                for i, legal in enumerate(legal_info)
            }

            for future in tqdm(
                as_completed(future_to_index),
                total=len(legal_info),
                desc="Processing",
                unit="request",
            ):
                index = future_to_index[future]
                try:
                    result = future.result()
                    xzgxf_list.extend(result)
                except Exception as e:
                    logger.error(
                        f"Failed to process get legal xzgxf at index {index}. Error: {e}"
                    )

        return xzgxf_list

    async def call_report(self, drlaw_state: dict) -> str:
        task = drlaw_state.get("task")
        query = task.get("query")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_MESSAGE),
                ("human", "{query}"),
            ]
        ).partial(
            current_date=datetime.now().isoformat(),
        )

        need_report = (
            prompt
            # | ChatOpenAI(model=task.get("model"), temperature=0.1)
            | ChatOpenAI(
                model="glm-4-0520",
                temperature=0.95,
                max_tokens=4095,
                model_kwargs={
                    "tools": [
                        {
                            "type": "web_search",
                            "web_search": {
                                "enable": False  # 禁用：False，启用：True，默认为 True。
                            },
                        }
                    ],
                },
            )
            | StrOutputParser()
        )
        print_agent_output("公司数据报告写作助正在收集关键信息", agent="REPORTER")
        ret = need_report.invoke(
            {
                "query": query,
            }
        )
        print_agent_output(f"模型推断的关键信息如下{ret}", agent="REPORTER")
        gptresponse = self.zhipu_output_handle(ret)
        return gptresponse

    async def run(self, drlaw_state: dict):
        print_agent_output("起诉状写作助理正在编写起诉状", agent="REPORTER")
        task = drlaw_state.get("task")
        query = task.get("query")
        # 提取问题中关键信息
        try:
            keyinfo = await self.call_report(drlaw_state)
            print_agent_output(f"提取的关键信息如下{keyinfo}", agent="REPORTER")
            # 调用工具获取信息
            # 1.获取公司信息
            if keyinfo.get("ifcommerce") == "是":
                company_info = self.get_company_info(
                    keyinfo.get("company_name"), keyinfo.get("ifintro")
                )
            else:
                company_info = [{}]
            # 2.获取子公司信息
            sub_company_info = self.get_subcompany_info(
                keyinfo.get("company_name"),
                keyinfo.get("over_investment"),
                keyinfo.get("wholly_owned"),
            )
            # 3.获取裁判文书信息
            legal_info = self.get_legal_info(
                keyinfo.get("company_name"),
                sub_company_info,
                keyinfo.get("hear_year"),
                keyinfo.get("prosecute_year"),
                keyinfo.get("over_legal_money"),
            )
            # 4.获取限制高消费信息
            if keyinfo.get("ifxzgxf") == "是":
                xzgxf_info = self.get_legal_xzgxf_info(legal_info)
            else:
                xzgxf_info = []

            # 返回起诉状字符串
            indict_info = save_dict_list_to_word_service(
                company_name=keyinfo.get("company_name"),
                company_info=company_info,
                sub_company_info=sub_company_info,
                legal_info=legal_info,
                xzgxf_info=xzgxf_info,
            )
            print(indict_info.replace("companyregister1_0", "companyregister0_0"))
            return {
                "messages": [
                    (
                        "human",
                        f"起诉状信息如下:{indict_info.replace('companyregister1_0','companyregister0_0')}",
                    )
                ],
                "agent_type": "客服助理",
            }
        except Exception as e:
            logger.exception(e)
            print(f"{Fore.RED}Error in answer question {query}: {e}{Style.RESET_ALL}")
            agent_info = f"{self.__class__.__name__}出错:\n {query}: {e}"
            return {"messages": [("human", agent_info)], "agent_type": "错误信息助理"}


if __name__ == "__main__":
    import asyncio

    reporter = ReporterAgent()

    asyncio.run(
        reporter.run(
            {
                "task": {
                    "query": "甘肃省敦煌种业集团股份有限公司关于工商信息及子公司信息，母公司及子公司的立案时间在2019年涉案金额不为0的裁判文书及限制高消费（不需要判决结果）整合报告。"
                },
            }
        )
    )
