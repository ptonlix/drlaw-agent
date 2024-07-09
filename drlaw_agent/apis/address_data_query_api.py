from typing import List, Dict
import requests
from drlaw_agent.apis.base import DOMAIN, headers, record_call


@record_call
def get_address_info(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据地址查该地址对应的省份城市区县
    例如：
        输入：
        {
            {"query_conds": {"地址": "西藏自治区那曲地区安多县帕那镇中路13号"}, "need_fields": []}
        }
        输出:
        [{
            "地址": "西藏自治区那曲地区安多县帕那镇中路13号",
            "省份": "西藏自治区",
            "城市": "那曲市",
            "区县": "安多县"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_address_info"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_address_code(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据省市区查询区划代码
    例如：
        输入：
        {
           {"query_conds": {"省份": "西藏自治区", "城市": "拉萨市", "区县": "城关区"}, "need_fields": []}
        }
        输出:
        [{
            "省份": "西藏自治区",
            "城市": "拉萨市",
            "城市区划代码": "540100000000",
            "区县": "城关区",
            "区县区划代码": "540102000000"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_address_code"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


@record_call
def get_temp_info(
    query_conds: Dict[str, str], need_fields: List[str] = []
) -> List[dict]:
    """
    根据省市区查询区划代码
    例如：
        输入：
        {
           {"query_conds": {"省份": "北京市", "城市": "北京市", "日期": "2020年1月1日"}, "need_fields": []}
        }
        输出:
        [{
            "日期": "2020年1月1日",
            "省份": "北京市",
            "城市": "北京市",
            "天气": "晴",
            "最高温度": "11",
            "最低温度": "1",
            "湿度": "55"
        }]
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_temp_info"

    data = {"query_conds": query_conds, "need_fields": need_fields}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


if __name__ == "__main__":
    import pprint

    # pprint.pp(get_address_info({"地址": "西藏自治区那曲地区安多县帕那镇中路13号"}, []))
    # pprint.pp(
    #     get_address_code({"省份": "西藏自治区", "城市": "拉萨市", "区县": "城关区"}, [])
    # )
    pprint.pp(
        get_temp_info({"省份": "北京市", "城市": "北京市", "日期": "2020年1月1日"}, [])
    )
