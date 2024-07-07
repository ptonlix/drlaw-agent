from typing import List, Dict, Any
import requests
from drlaw_agent.apis.base import DOMAIN, headers


def get_sum(nums: List[str | float | int]) -> float:
    """
    求和方法，可以对传入的int、float、str数组进行求和，str数组只能转换字符串里的千万亿，如"1万"
    例如：
        输入：
        {
           [1, 2, 3, 4, 5]
        }
        输出: 15
    """

    url = f"https://{DOMAIN}/law_api/s1_b/get_sum"

    data = nums

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


def lawrank(keys: List[Any], values: List[float]) -> float:
    """
    排序接口，返回按照values排序的keys,此排序为升序排序
    例如：
        输入：
        {
        { "keys": ["a", "b", "c"], "values": [2, 5, 3] }
        }
        输出:
        {["a","c","b"]}
    """

    url = f"https://{DOMAIN}/law_api/s1_b/rank"

    data = {"keys": keys, "values": values}

    rsp = requests.post(url, json=data, headers=headers)
    rsp_obj = rsp.json()

    if isinstance(rsp_obj, dict):
        return [rsp_obj]
    return rsp_obj


if __name__ == "__main__":
    import pprint

    pprint.pp(get_sum([1, 2, 3, 4, 5]))
    pprint.pp(lawrank(keys=["a", "b", "c"], values=[2, 5, 3], is_desc=True))
