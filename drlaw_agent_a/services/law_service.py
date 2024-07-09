import json
from drlaw_agent_a.apis import (
    get_legal_document,
    search_case_num_by_legal_document,
)


def get_amount_involved_by_case_num_service(case_num: str) -> str:
    """
    根据案号获得该案的涉案金额
    注意:涉及到两个案件涉案金额大小比较，推荐使用 compare_amount_involved_by_two_case_num
    输入参数：案号
    例如：(2020)赣0191民初1045号
    """
    rsp = get_legal_document(case_num)
    ret = {}
    if "案号" in rsp:
        ret["案号"] = rsp["案号"]
    if "涉案金额" in rsp:
        ret["涉案金额"] = rsp["涉案金额"]
    json_str = json.dumps(ret, ensure_ascii=False)
    return json_str


def compare_amount_involved_by_two_case_num_service(
    case_num_one: str,
    case_num_two: str,
) -> str:
    """
    根据两个案号获得该案的涉案金额，并且比较涉案金额大小
    输入参数：case_num_one:案号一 case_num_two:案号二
    例如：(2019)冀0203民初5480号 和 (2020)苏0412民初6970号
    """
    case_num_one_rsp = get_amount_involved_by_case_num_service(case_num_one)
    case_num_two_rsp = get_amount_involved_by_case_num_service(case_num_two)

    return case_num_one_rsp + "\n" + case_num_two_rsp


def get_legal_basis_by_case_num_service(case_num: str) -> str:
    """
    根据案号获得审理该案的法律条文依据
    输入参数：案号
    例如：(2020)赣0191民初1045号
    """
    rsp = get_legal_document(case_num)
    ret = {}
    if "案号" in rsp:
        ret["案号"] = rsp["案号"]
    if "涉案金额" in rsp:
        ret["审理法条依据"] = rsp["审理法条依据"]
    json_str = json.dumps(ret, ensure_ascii=False)
    return json_str


def get_legal_document_service(case_num: str) -> str:
    """
    根据案号获得该案所有基本信息，包括'判决结果','原告','原告律师','审理法条依据',
    '文书类型','文件名','标题','案由','涉案金额','胜诉方','被告','被告律师'。

    例如：
        输入：
        {'case_num': '案号1'}
        或者
        {'case_num': ['案号1', '案号2', '案号3']}
        或者
        {'case_num': {'Items': ['案号1', '案号2']}}
        输出：
        {'判决结果': '一、南昌绿地申新置业有限公司于本判决生效之日起十五日内向上海澳辉照明电器有限公司支付本金1179104元。\n'
             '二、南昌绿地申新置业有限公司于本判决生效之日起十五日内向上海澳辉电器有限公司支付利息(以质保金1179104元为基数,按年利率6%,从2019年6月7日起计算至1179104元实际付清之日止)。\n'
             '三、驳回上海澳辉电器有限公司的其他诉讼请求。',
         '原告': '上海澳辉照明电器有限公司',
         '原告律师': '刘某某,北京大成(南昌)律师事务所律师\n罗某某,北京大成(南昌)律师事务所律师',
         '审理法条依据': '无',
         '文书类型': '民事判决书',
         '文件名': '（2020）赣0191民初1045号.txt',
         '标题': '上海澳辉照明电器有限公司与上海建工集团股份有限公司、南昌绿地申新置业有限公司合同纠纷一审民事判决书',
         '案号': '(2020)赣0191民初1045号',
         '案由': '合同纠纷',
         '涉案金额': '1179104',
         '胜诉方': '原告',
         '被告': '上海建工集团股份有限公司\n南昌绿地申新置业有限公司',
         '被告律师': '罗丽萍,公司员工\n李某某,江西豫章律师事务所律师\n蔡某某,江西豫章律师事务所实习律师'}
    """
    rsp = get_legal_document(case_num)
    json_str = json.dumps(rsp, ensure_ascii=False)
    return json_str


def count_case_number_by_cause_service(cause_of_action: str) -> str:
    """
    根据案由获得涉及该案由的案件数量。
    """
    rsp = search_case_num_by_legal_document("案由", cause_of_action)
    if isinstance(rsp, dict):
        case_number = 1
    elif isinstance(rsp, list):
        case_number = len(rsp)
    else:
        case_number = 0
    ret = {f"案由为{cause_of_action}的案件数量": case_number}
    json_str = json.dumps(ret, ensure_ascii=False)
    return json_str


def search_case_num_by_legal_document_service(key: str, value: str) -> str:
    """
    根据法律文书某个 key 是某个 value 来查询具体的案号。这个函数只能用来查询案号。
    可以输入的 key 有['判决结果','原告','原告律师','审理法条依据',
    '文书类型','文件名','标题','案由','涉案金额','胜诉方','被告','被告律师',]

    例如：
        输入：
        {"key": "原告",
         "value": "光明乳业股份有限公司"}
        输出：
        [{'案号': '(2020)苏06民初861号'},
         {'案号': '(2021)沪0104民初6181号'},
         {'案号': '(2021)沪0104民初17782号'},
         {'案号': '(2019)湘0111民初3091号'}]
    """
    rsp = search_case_num_by_legal_document(key, value)
    json_str = json.dumps(rsp, ensure_ascii=False)
    return json_str


def count_plaintiff_lawyer_service(plaintiff: str) -> str:
    """
    发起诉讼担任原告时，统计公司聘请的不同原告律师的频次。
    """
    case_num_json_list = search_case_num_by_legal_document("原告", plaintiff)
    if isinstance(case_num_json_list, dict):
        case_num_json_list = [case_num_json_list]
    case_num_list = [item["案号"] for item in case_num_json_list]
    legal_document_list = get_legal_document(case_num_list)
    if isinstance(legal_document_list, dict):
        legal_document_list = [legal_document_list]
    # 统计原告律师的频次
    plaintiff_lawyer_counter = {}
    for item in legal_document_list:
        if "原告律师" in item and item["原告律师"]:
            if item["原告律师"] in plaintiff_lawyer_counter:
                plaintiff_lawyer_counter[item["原告律师"]] += 1
            else:
                plaintiff_lawyer_counter[item["原告律师"]] = 1
    ret = {"原告律师频次": plaintiff_lawyer_counter}
    json_str = json.dumps(ret, ensure_ascii=False)
    return json_str


def count_defendant_lawyer_service(defendant: str) -> str:
    """
    面临诉讼担任被告时，统计公司聘请的不同被告律师的频次。
    """
    case_num_json_list = search_case_num_by_legal_document("被告", defendant)
    if isinstance(case_num_json_list, dict):
        case_num_json_list = [case_num_json_list]
    case_num_list = [item["案号"] for item in case_num_json_list]
    legal_document_list = get_legal_document(case_num_list)
    if isinstance(legal_document_list, dict):
        legal_document_list = [legal_document_list]
    # 统计被告律师的频次
    defendant_lawyer_counter = {}
    for item in legal_document_list:
        if "被告律师" in item and item["被告律师"]:
            if item["被告律师"] in defendant_lawyer_counter:
                defendant_lawyer_counter[item["被告律师"]] += 1
            else:
                defendant_lawyer_counter[item["被告律师"]] = 1
    ret = {"被告律师频次": defendant_lawyer_counter}
    json_str = json.dumps(ret, ensure_ascii=False)
    return json_str


if __name__ == "__main__":

    # print(get_amount_involved_by_case_num_service("(2020)沪0104民初14148号案件"))
    # print(get_legal_basis_by_case_num_service("(2019)鄂0103民初12292号"))
    # print(
    #     compare_amount_involved_by_two_case_num_service(
    #         "(2020)赣0191民初1045号", "(2020)桂0103民初6133号"
    #     )
    # )

    # print(get_legal_document_service("(2019)鄂01民初4724号"))
    # print(count_defendant_lawyer_service("新城控股集团股份有限公司"))
    # print(count_plaintiff_lawyer_service("光明乳业股份有限公司"))
    print(count_case_number_by_cause_service("不正当竞争纠纷"))
