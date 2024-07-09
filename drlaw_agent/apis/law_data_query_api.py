from typing import List, Dict
import requests
from drlaw_agent.apis.base import DOMAIN, headers, record_call


@record_call
def get_legal_document(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据案号查询裁判文书相关信息
    例如：
        输入：
        {
            {"query_conds": {"案号": "(2019)沪0115民初61975号"}, "need_fields": []}
        }
        输出:
        [{
            "关联公司": "上海爱斯达克汽车空调系统有限公司",
            "标题": "上海爱斯达克汽车空调系统有限公司与上海逸测检测技术服务有限公司服务合同纠纷一审民事判决书",
            "案号": "(2019)沪0115民初61975号",
            "文书类型": "民事判决书",
            "原告": "上海爱斯达克汽车空调系统有限公司",
            "被告": "上海逸测检测技术服务有限公司",
            "原告律师事务所": "",
            "被告律师事务所": "上海世韬律师事务所",
            "案由": "服务合同纠纷",
            "涉案金额": "1254802.58",
            "判决结果": "一、被告上海逸测检测技术服务有限公司应于本判决生效之日起十日内支付原告上海爱斯达克汽车空调系统有限公司测试费1,254,802.58元; \\n \\n二、被告上海逸测检测技术服务有限公司应于本判决生效之日起十日内支付原告上海爱斯达克汽车空调系统有限公司违约金71,399.68元 。  \\n \\n负有金钱给付义务的当事人如未按本判决指定的期间履行给付金钱义务,应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定,加倍支付迟延履行期间的债务利息 。  \\n \\n案件受理费16,736元,减半收取计8,368元,由被告上海逸测检测技术服务有限公司负担 。  \\n \\n如不服本判决,可在判决书送达之日起十五日内向本院递交上诉状,并按对方当事人的人数提出副本,上诉于上海市第一中级人民法院 。 ",
            "日期": "2019-12-09 00:00:00",
            "文件名": "（2019）沪0115民初61975号.txt"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_legal_document"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_legal_document_list(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据关联公司查询所有裁判文书相关信息列表
    例如：
        输入：
        {
           {"query_conds": {"关联公司": "上海爱斯达克汽车空调系统有限公司"}, "need_fields": []}
        }
        输出:
       [{
            "关联公司": "上海爱斯达克汽车空调系统有限公司",
            "标题": "上海爱斯达克汽车空调系统有限公司与上海逸测检测技术服务有限公司服务合同纠纷一审民事判决书",
            "案号": "(2019)沪0115民初61975号",
            "文书类型": "民事判决书",
            "原告": "上海爱斯达克汽车空调系统有限公司",
            "被告": "上海逸测检测技术服务有限公司",
            "原告律师事务所": "",
            "被告律师事务所": "上海世韬律师事务所",
            "案由": "服务合同纠纷",
            "涉案金额": "1254802.58",
            "判决结果": "一、被告上海逸测检测技术服务有限公司应于本判决生效之日起十日内支付原告上海爱斯达克汽车空调系统有限公司测试费1,254,802.58元; \\n \\n二、被告上海逸测检测技术服务有限公司应于本判决生效之日起十日内支付原告上海爱斯达克汽车空调系统有限公司违约金71,399.68元 。  \\n \\n负有金钱给付义务的当事人如未按本判决指定的期间履行给付金钱义务,应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定,加倍支付迟延履行期间的债务利息 。  \\n \\n案件受理费16,736元,减半收取计8,368元,由被告上海逸测检测技术服务有限公司负担 。  \\n \\n如不服本判决,可在判决书送达之日起十五日内向本院递交上诉状,并按对方当事人的人数提出副本,上诉于上海市第一中级人民法院 。 ",
            "日期": "2019-12-09 00:00:00",
            "文件名": "（2019）沪0115民初61975号.txt"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_legal_document_list"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_court_info(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据法院名称查询法院名录相关信息
    例如：
        输入：
        {
           {"query_conds": {"法院名称": "上海市浦东新区人民法院"}, "need_fields": []}
        }
        输出:
       [{
            "法院名称": "上海市浦东新区人民法院",
            "法院负责人": "朱丹",
            "成立日期": "2019-05-16",
            "法院地址": "上海市浦东新区丁香路611号",
            "法院联系电话": "-",
            "法院官网": "-"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_court_info"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_court_code(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据法院名称或者法院代字查询法院代字等相关数据

    例如：
        输入：
        {
           {"query_conds": {"法院名称": "上海市浦东新区人民法院"}, "need_fields": []}
        }
        输出:
       [{
            "法院名称": "上海市浦东新区人民法院",
            "行政级别": "市级",
            "法院级别": "基层法院",
            "法院代字": "沪0115",
            "区划代码": "310115",
            "级别": "1"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_court_code"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_lawfirm_info(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据律师事务所查询律师事务所名录

     例如：
         输入：
         {
            {"query_conds": {"律师事务所名称": "爱德律师事务所"}, "need_fields": []}
         }
         输出:
        [{
            "律师事务所名称": "爱德律师事务所",
            "律师事务所唯一编码": "31150000E370803331",
            "律师事务所负责人": "巴布",
            "事务所注册资本": "10万元人民币",
            "事务所成立日期": "1995-03-14",
            "律师事务所地址": "呼和浩特市赛罕区大学西街110号丰业大厦11楼",
            "通讯电话": "0471-3396155",
            "通讯邮箱": "kehufuwubu@ardlaw.cn",
            "律所登记机关": "内蒙古自治区呼和浩特市司法局"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_lawfirm_info"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_lawfirm_log(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据律师事务所查询律师事务所统计数据

     例如：
         输入：
         {
            {"query_conds": {"律师事务所名称": "北京市金杜律师事务所"}, "need_fields": []}
         }
         输出:
        [{
            "律师事务所名称": "北京市金杜律师事务所",
            "业务量排名": "2",
            "服务已上市公司": "68",
            "报告期间所服务上市公司违规事件": "23",
            "报告期所服务上市公司接受立案调查": "3"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_lawfirm_log"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_legal_abstract(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据案号查询文本摘要

     例如：
         输入：
         {
            {"query_conds": {"案号": "（2019）沪0115民初61975号"}, "need_fields": []}
         }
         输出:
        [{
            "文件名": "（2019）沪0115民初61975号.txt",
            "案号": "（2019）沪0115民初61975号",
            "文本摘要": "原告上海爱斯达克汽车空调系统有限公司与被告上海逸测检测技术服务有限公司因服务合同纠纷一案，原告请求被告支付检测费1,254,802.58元"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_legal_abstract"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_xzgxf_info(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据案号查询限制高消费相关信息

     例如：
         输入：
         {
            { "query_conds": {"案号": "（2018）鲁0403执1281号"}, "need_fields": [] }
         }
         输出:
        [{
            "限制高消费企业名称": "枣庄西能新远大天然气利用有限公司",
            "案号": "（2018）鲁0403执1281号",
            "法定代表人": "高士其",
            "申请人": "枣庄市人力资源和社会保障局",
            "涉案金额": "12000",
            "执行法院": "山东省枣庄市薛城区人民法院",
            "立案日期": "2018-11-16 00:00:00",
            "限高发布日期": "2019-02-13 00:00:00"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_xzgxf_info"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_xzgxf_info_list(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据企业名称查询所有限制高消费相关信息列表

     例如：
         输入：
         {
            { "query_conds": {"限制高消费企业名称": "欣水源生态环境科技有限公司"}, "need_fields": [] }
         }
         输出:
        [{
            "限制高消费企业名称": "欣水源生态环境科技有限公司",
            "案号": "（2023）黔2731执恢130号",
            "法定代表人": "刘福云",
            "申请人": "四川省裕锦建设工程有限公司惠水分公司",
            "涉案金额": "7500000",
            "执行法院": "贵州省黔南布依族苗族自治州惠水县人民法院",
            "立案日期": "2023-08-04 00:00:00",
            "限高发布日期": "2023-11-09 00:00:00"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_xzgxf_info_list"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


if __name__ == "__main__":
    import pprint

    # print(get_legal_document({"案号": "(2019)沪0115民初61975号"}, []))
    # pprint.pp(
    #     get_legal_document_list({"关联公司": "上海爱斯达克汽车空调系统有限公司"}, [])
    # )
    # pprint.pp(get_court_info({"法院名称": "上海市浦东新区人民法院"}, []))
    # pprint.pp(get_court_code({"法院名称": "上海市浦东新区人民法院"}, []))
    # pprint.pp(get_lawfirm_info({"律师事务所名称": "爱德律师事务所"}, []))
    # pprint.pp(get_lawfirm_log({"律师事务所名称": "北京市金杜律师事务所"}, []))
    # pprint.pp(get_legal_abstract({"案号": "（2019）沪0115民初61975号"}, []))
    # pprint.pp(get_xzgxf_info({"案号": "（2018）鲁0403执1281号"}, []))
    pprint.pp(
        get_xzgxf_info_list({"限制高消费企业名称": "欣水源生态环境科技有限公司"}, [])
    )
