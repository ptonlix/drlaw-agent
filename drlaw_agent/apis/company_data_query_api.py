from typing import List, Dict
import requests
from drlaw_agent.apis.base import DOMAIN, headers, record_call, CallLogger


@record_call
def get_company_info(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据上市公司名称、简称或代码查找上市公司信息
    例如：
        输入：
        {
            "query_conds": {
                "公司名称": "上海妙可蓝多食品科技股份有限公司"
            },
            "need_fields": []
        }
        输出:
        [{
            "公司名称": "上海妙可蓝多食品科技股份有限公司",
            "公司简称": "妙可蓝多",
            "英文名称": "Shanghai Milkground Food Tech Co., Ltd.",
            "关联证券": "",
            "公司代码": "600882",
            "曾用简称": "大成股份>> *ST大成>> 华联矿业>> 广泽股份",
            "所属市场": "上交所",
            "所属行业": "食品制造业",
            "成立日期": "1988-11-29",
            "上市日期": "1995-12-06",
            "法人代表": "柴琇",
            "总经理": "柴琇",
            "董秘": "谢毅",
            "邮政编码": "200136",
            "注册地址": "上海市奉贤区工业路899号8幢",
            "办公地址": "上海市浦东新区金桥路1398号金台大厦10楼",
            "联系电话": "021-50188700",
            "传真": "021-50188918",
            "官方网址": "www.milkground.cn",
            "电子邮箱": "ir@milkland.com.cn",
            "入选指数": "国证Ａ指,巨潮小盘",
            "主营业务": "以奶酪、液态奶为核心的特色乳制品的研发、生产和销售，同时公司也从事以奶粉、黄油为主的乳制品贸易业务。",
            "经营范围": "许可项目：食品经营；食品互联网销售；互联网直播服务（不含新闻信息服务、网络表演、网络视听节目）；互联网信息服务；进出口代理。（依法须经批准的项目，经相关部门批准后方可开展经营活动，具体经营项目以相关部门批准文件或许可证件为准）。一般项目：乳制品生产技术领域内的技术开发、技术咨询、技术服务、技术转让；互联网销售（除销售需要许可的商品）；互联网数据服务；信息系统集成服务；软件开发；玩具销售。（除依法须经批准的项目外，凭营业执照依法自主开展经营活动）",
            "机构简介": "公司是1988年11月10日经山东省体改委鲁体改生字(1988)第56号文批准，由山东农药厂发起，采取社会募集方式组建的以公有股份为主体的股份制企业。1988年12月15日,经中国人民银行淄博市分行以淄银字(1988)230号文批准，公开发行股票。 1988年12月经淄博市工商行政管理局批准正式成立山东农药工业股份有限公司(营业执照:16410234)。",
            "每股面值": "1.0",
            "首发价格": "1.0",
            "首发募资净额": "4950.0",
            "首发主承销商": ""
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_company_info"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_company_register(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据公司名称，查询工商信息

    例如：
        输入：
        {
            "query_conds": {
                "公司名称": "天能电池集团股份有限公司"
            },
            "need_fields": []
        }
        输出：
       [{
            "公司名称": "天能电池集团股份有限公司",
            "登记状态": "存续",
            "统一社会信用代码": "913305007490121183",
            "法定代表人": "杨建芬",
            "注册资本": "97210",
            "成立日期": "2003-03-13",
            "企业地址": "浙江省长兴县煤山镇工业园区",
            "联系电话": "0572-6029388",
            "联系邮箱": "dshbgs@tiannenggroup.com",
            "注册号": "330500400001780",
            "组织机构代码": "74901211-8",
            "参保人数": "709",
            "行业一级": "制造业",
            "行业二级": "电气机械和器材制造业",
            "行业三级": "电池制造",
            "曾用名": "天能电池集团有限公司,\n浙江天能电池有限公司",
            "企业简介": "天能集团成立于1986年，地处长三角腹地—— “中国绿色动力能源中心”浙江长兴，主要以电动车环保动力电池制造为主，集新能源镍氢、锂离子电池，风能、太阳能储能电池以及再生铅资源回收、循环利用等新能源的研发、生产、销售为一体，是目前国内首屈一指的绿色动力能源制造商。集团实力雄厚，管理科学，行业地位优势明显，于2007年6月11日，以中国动力电池第一股，在香港主板成功上市（00819.HK）。目前，集团已发展成为拥有25家国内全资子公司，3家境外公司，2013年销售收入达500亿，员工20000余名的大型国际化集团公司。集团拥有浙江长兴、江苏沭阳、安徽芜湖、安徽界首、河南濮阳五大生产基地，总资产近70亿元。公司主导产品电动车动力电池的产销量连续十五年位居全国同行业首位。集团是国家重点扶持技术企业、国家火炬计划重点技术企业，全国轻工行业先进集体、浙江省工业行业龙头骨干企业、国家蓄电池标准化委员会副主任委员单位。集团经营规模位居中国制造业企业500强、中国民营企业500强、中国电池行业十强、浙江省百强企业、浙江省民营企业100强。拥有国家级博士后工作站、院士专家工作站、省级企业技术中心、省级高新技术研究开发中心。近年来，先后开发国家级重点新产品10项，创新国家专利近600余项、省级新产品和高新技术产品100余项，同时承担国家火炬计划和星火计划项目10余项。集团“天能”牌电池先后被评为国家重点新产品、浙江省名牌产品、浙江省高新技术产品；“天能”商标先后荣获驰名商标、浙江省着名商标；天能品牌荣获2008中国动力电池最佳品牌、中国最具价值品牌500强、亚洲品牌500强，天能电池荣获2009年度最值得消费者信赖的电动车电池品牌，天能集团荣获中国电动车行业发展突出贡献奖。为响应国家大力发展循环经济的号召，天能集团将积极致力于新能源产业的发展，努力创新创业，实现“矢志成为全球领先的绿色能源供应商”的战略目标，争取为改善民生发展、践行产业报国、构建和谐社会作出更大的贡献。",
            "经营范围": "高性能电池的研发、生产、销售；锂离子电池、燃料电池及其他储能环保电池、新型电极材料的研究开发、生产、销售；货物进出口和技术进出口（国家限定公司经营或禁止进出口的商品和技术除外）。（依法须经批准的项目，经相关部门批准后方可开展经营活动）"
        }]
    """
    url = f"https://{DOMAIN}/law_api/s1_b/get_company_register"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_company_register_name(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据统一社会信用代码查询公司名称

    例如：
        输入：
        {
            "query_conds": {
                "统一社会信用代码": "91310000677833266F"
            },
            "need_fields": []
        }
        输出：
        [{
            "公司名称": "上海晨光文具股份有限公司"
        }]
    """
    url = f"https://{DOMAIN}/law_api/s1_b/get_company_register_name"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_sub_company_info(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据被投资的子公司名称获得投资该公司的上市公司、投资比例、投资金额等信息

    例如：
        输入：
        {
            {
                "query_conds": {
                    "公司名称": "上海爱斯达克汽车空调系统有限公司"
                },
                "need_fields": []
            }
        }
        输出：
        [{
            "关联上市公司全称": "上海航天汽车机电股份有限公司",
            "上市公司关系": "子公司",
            "上市公司参股比例": "87.5",
            "上市公司投资金额": "8.54亿",
            "公司名称": "上海爱斯达克汽车空调系统有限公司"
        }]
    """
    url = f"https://{DOMAIN}/law_api/s1_b/get_sub_company_info"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_sub_company_info_list(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据上市公司（母公司）的名称查询该公司投资的所有子公司信息列表

    例如：
        输入：
        {
            {
                "query_conds": {
                    "关联上市公司全称": "上海航天汽车机电股份有限公司"
                },
                "need_fields": []
            }
        }
        输出：
        [{
            "关联上市公司全称": "上海航天汽车机电股份有限公司",
            "上市公司关系": "子公司",
            "上市公司参股比例": "100.0",
            "上市公司投资金额": "8800.00万",
            "公司名称": "甘肃神舟光伏电力有限公司"
        }]
    """
    url = f"https://{DOMAIN}/law_api/s1_b/get_sub_company_info_list"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


if __name__ == "__main__":
    # print(
    #     get_company_info(
    #         query_conds={"公司名称": "上海妙可蓝多食品科技股份有限公司"},
    #         need_fields=[],
    #     )
    # )
    # print(
    #     get_company_register(
    #         query_conds={"公司名称": "天能电池集团股份有限公司"},
    #         need_fields=[],
    #     )
    # )
    print(
        get_company_register_name(
            query_conds={"统一社会信用代码": "91310000677833266F"},
            need_fields=[],
        )
    )
    print(
        get_sub_company_info(
            query_conds={"公司名称": "上海爱斯达克汽车空调系统有限公司"},
            need_fields=[],
        )
    )
    print(
        get_sub_company_info_list(
            query_conds={"关联上市公司全称": "上海航天汽车机电股份有限公司"},
            need_fields=["公司名称", "上市公司投资金额"],
        )
    )
    print(
        get_sub_company_info_list(
            query_conds={"关联上市公司全称": "上海航天汽车机电股份有限公司"},
            need_fields=["公司名称", "上市公司投资金额"],
        )
    )

    logger = CallLogger()
    print("Call Sequence:", logger.get_call_sequence())
    print("Call Count:", logger.get_call_count())
    print("Total Calls:", logger.get_total_calls())
    print("Call Type:", logger.get_call_types())
