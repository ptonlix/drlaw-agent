from drlaw_agent_a.apis import search_company_name_by_info, get_company_info
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

SYSTEM_MESSAGE = """
当前日期：{current_date}

你是一个公司名称检索大师，你熟悉中国公司名称构成,请根据用户提供的公司名称给出这个公司简称。
输出格式为 {{"company_name":"公司简称"}}

注意:公司简称为四个中文汉字,只需要输出一个,不要输出多个
"""


def get_company_bref_name(company_name: str) -> str:
    SYSTEM_MESSAGE
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_MESSAGE),
            ("human", "{query}"),
        ]
    ).partial(
        current_date=datetime.now().isoformat(),
    )

    get_company_name = (
        prompt | ChatOpenAI(model="glm-4", temperature=0.1) | JsonOutputParser()
    )

    return get_company_name.invoke(company_name)


def _get_full_name(company_name: str) -> str:
    """根据公司名称、公司简称或英文名称，获取该公司的全称。"""
    company_info_json = search_company_name_by_info(key="公司简称", value=company_name)
    if "公司名称" in company_info_json:
        company_name = company_info_json["公司名称"]
        return company_name
    company_info_json = search_company_name_by_info(key="英文名称", value=company_name)
    if "公司名称" in company_info_json:
        company_name = company_info_json["公司名称"]
        return company_name
    company_info_json = search_company_name_by_info(key="曾用简称", value=company_name)
    if "公司名称" in company_info_json:
        company_name = company_info_json["公司名称"]
        return company_name

    return company_name


def re_get_full_name(company_name: str) -> str:
    try:
        # 名字输错的情况
        new_name = get_company_bref_name(company_name)
        print(f"LLM生成公司简称:{new_name}")
        full_company_name = _get_full_name(**new_name)

        if new_name.get("company_name") == full_company_name:
            # 说明生成的公司简称没有效果
            print(
                f"通过LLM生成的公司简称获取公司全称没有效果，执行规则策略: {full_company_name}"
            )
            # 1.排除中文括号匹配的问题
            if "(" in company_name and ")" in company_name:
                full_company_name = company_name.replace("(", "（").replace(")", "）")
            elif "（" in company_name and "）" in company_name:
                full_company_name = company_name.replace("（", "(").replace("）", ")")

        print(f"最终获取到公司全称: {full_company_name}")
        return full_company_name

    except Exception as e:
        print(e)
        return company_name


# def augment_company_name(company_name: str | List[str]):
#     company_name = company_name if isinstance(company_name, list) else [company_name]
#     for c in company_name[:]:
#         company_name += search_company_name_by_company_abbreviation(c)
#         company_name += search_company_name_by_english_name(c)
#         company_name += [c.replace("(", "（").replace(")", "）")]
#         company_name += [c.replace("（", "(").replace("）", ")")]

#     return list(set(company_name))


if __name__ == "__main__":
    # name = re_get_full_name("广汇能源股份有限公司")
    # print(name)

    print(_get_full_name("广汇能源"))
