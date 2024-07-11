from drlaw_agent.agents.utils.views import print_agent_output
from drlaw_agent.services.write_service import (
    get_citizens_sue_citizens_service,
    get_citizens_sue_company_service,
    get_company_sue_citizens_service,
    get_company_sue_company_service,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
import json
from json.decoder import JSONDecodeError
import re
from datetime import datetime
from colorama import Fore, Style

SYSTEM_MESSAGE = """你是一个法律专家，专门帮助客户来拟起诉状。你需要从遵从以下工作流程
1. 从用户的请求中判断要草拟的起诉状是如下四种 `公司法人起诉公司法人、公司法人起诉公司、公司起诉公司法人、公司起诉公司` 中的哪一种
2. 从用户请求中提取如下关键信息: `原告公司名称、被告公司名称、原告诉讼律师、被告诉讼律师、诉讼请求、诉讼法院和起诉时间`
3. 从用户请求的信息中构造生成如下关键信息: `诉讼的事实理由、诉讼证据`

注意: 如果是用户请求的形式为，公司与公司的法人发送纠纷,应该是公司起诉公司法人类型

起诉状类型记为:indictment_type
原告公司名称记为plaintiff_company、被告公司名称记为accuser_company、原告诉讼律师记为plaintiff_lawyer
被告诉讼律师记为accuser_lawyer、诉讼请求记为claim、诉讼法院记为court、起诉时间记为time
诉讼的事实理由记为reason、诉讼证据记为proof
结果输出: 将以上关键信息整理成JSON格式,如以下格式:
```json
{{
    "indictment_type": "string",
    "plaintiff_company": "string",
    "accuser_company": "string",
    "plaintiff_lawyer": "string",
    "accuser_lawyer": "string",
    "claim": "string",
    "reason": "string",
    "proof": "string",
    "court": "string",
    "time": "string"
}}
```
输出例子:
```json
{{
    "indictment_type":"公司法人起诉公司法人",
    "plaintiff_company": "北京碧水源科技股份有限公司",
    "accuser_company": "江苏金迪克生物技术股份有限公司",
    "plaintiff_lawyer": "北京国旺律师事务所",
    "accuser_lawyer": "北京浩云律师事务所",
    "claim":"民事纠纷",
    "reason":"上诉",
    "proof":"证据",
    "court": "天津市蓟州区人民法院",
    "time": "2024-02-01"
}}
```

当前日期：{current_date}
"""


class IndictmenterAgent:
    """
    起诉状信息收集与写作助理:
    能根据针对公司法人起诉公司法人、公司法人起诉公司、公司起诉公司法人、公司起诉公司这四种起诉场景收集相关信息并写作起诉状。用户要求写起诉状，直接询问他即可。
    """

    def __init__(self):
        self.indictment_dict = {
            "公司法人起诉公司法人": get_citizens_sue_citizens_service,
            "公司法人起诉公司": get_citizens_sue_company_service,
            "公司起诉公司法人": get_company_sue_citizens_service,
            "公司起诉公司": get_company_sue_company_service,
        }

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

    async def call_indictment(self, drlaw_state: dict) -> str:
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

        need_indictment = (
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
        print_agent_output("起诉状写作助理正在收集关键信息", agent="INDICTMENTER")
        ret = need_indictment.invoke(
            {
                "query": query,
            }
        )
        print_agent_output(f"模型推断的关键信息如下{ret}", agent="INDICTMENTER")
        gptresponse = self.zhipu_output_handle(ret)
        return gptresponse

    async def run(self, drlaw_state: dict):
        print_agent_output("起诉状写作助理正在编写起诉状", agent="INDICTMENTER")
        task = drlaw_state.get("task")
        query = task.get("query")
        # 提取问题中关键信息
        try:
            info = await self.call_indictment(drlaw_state)
            print_agent_output(f"提取的关键信息如下{info}", agent="INDICTMENTER")
            # 调用工具获取信息
            tool = self.indictment_dict[info["indictment_type"]]

            info.pop("indictment_type")  # 忽略该字段
            indict_info = tool(**info)
            # 返回起诉状字符串
            return {
                "messages": [("human", f"起诉状信息如下:{indict_info}")],
                "agent_type": "客服助理",
            }
        except Exception as e:
            print(f"{Fore.RED}Error in answer question {query}: {e}{Style.RESET_ALL}")
            agent_info = f"{self.__class__.__name__}出错:\n {query}: {e}"
            return {
                "messages": [("human", agent_info)],
                "agent_type": "错误信息助理",
            }


if __name__ == "__main__":
    import asyncio

    indict = IndictmenterAgent()

    asyncio.run(
        indict.run(
            {
                "task": {
                    "query": "深圳市佳士科技股份有限公司的法人与天津凯发电气股份有限公司的法人发生了产品生产者责任纠纷，深圳市佳士科技股份有限公司委托给了山东崇义律师事务所，天津凯发电气股份有限公司委托给了山东海金州律师事务所，请写一份民事起诉状给辽宁省沈阳市中级人民法院时间是2024-04-02，注：法人的地址电话可用公司的代替。"
                },
            }
        )
    )
