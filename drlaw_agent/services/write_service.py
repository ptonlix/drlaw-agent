from drlaw_agent.apis.write_data_api import (
    save_dict_list_to_word,
    get_citizens_sue_citizens,
    get_citizens_sue_company,
    get_company_sue_citizens,
    get_company_sue_company,
)
from drlaw_agent.services.company_service import get_company_register_service
from drlaw_agent.services.lawfirm_service import get_lawfirm_info_service
from drlaw_agent.services.court_service import get_court_info_service
import json


def save_dict_list_to_word_service(
    company_name: str,
    company_info: list,
    sub_company_info: list,
    legal_info: list,
    xzgxf_info: list,
) -> str:
    """
    通过传入公司名称、公司工商信息、子公司信息、裁判文书信息、限制高消费信息，制作生成公司数据报告
    例子：
        输入：
        {
        "company_name": "北京碧水源科技股份有限公司",
        }
        返回：报告字符串
    """
    word_dict = {
        "工商信息": company_info,
        "子公司信息": sub_company_info,
        "裁判文书": legal_info,
        "限制高消费": xzgxf_info,
    }
    # word_dict_str = json.dumps(word_dict, ensure_ascii=False)
    try:
        result = save_dict_list_to_word(company_name, str(word_dict))
        return result
    except Exception:
        return "生成公司数据报告失败,请重试"


def get_citizens_sue_citizens_service(
    plaintiff_company: str,
    accuser_company: str,
    plaintiff_lawyer: str,
    accuser_lawyer: str,
    claim: str,
    reason: str,
    proof: str,
    court: str,
    time: str,
):
    """
    公民起诉公民的诉讼状生成接口
    通过传入原告法人的公司名称、被告法人的公司名称、原告诉讼律师、被告诉讼律师、诉讼法院和宿舍时间，生成民事起诉状。
    例子：
        输入：
        {
        plaintiff_company: "北京碧水源科技股份有限公司",
        accuser_company: "江苏金迪克生物技术股份有限公司",
        plaintiff_lawyer: "北京国旺律师事务所",
        accuser_lawyer: "北京浩云律师事务所",
        claim:"民事纠纷",
        reason:"上诉",
        proof:"证据",
        court: "天津市蓟州区人民法院",
        time: "2024-02-01",
        }
        返回：起诉状字符串
    """
    try:
        # 获取原告法人信息
        plaintiff_company_info = json.loads(
            get_company_register_service(plaintiff_company)
        )[0]
        accuser_company_info = json.loads(
            get_company_register_service(accuser_company)
        )[0]
        plaintiff_lawyer_info = json.loads(get_lawfirm_info_service(plaintiff_lawyer))[
            0
        ]
        accuser_lawyer_info = json.loads(get_lawfirm_info_service(accuser_lawyer))[0]
        court_info = json.loads(get_court_info_service(court))[0]
        time_info = time

        palyload = {
            "原告": plaintiff_company_info.get("法定代表人"),
            "原告性别": "男",
            "原告生日": "1976-10-2",
            "原告民族": "汉",
            "原告工作单位": plaintiff_company_info.get("公司名称"),
            "原告地址": plaintiff_company_info.get("企业地址"),
            "原告联系方式": plaintiff_company_info.get("联系电话"),
            "原告委托诉讼代理人": plaintiff_lawyer_info.get("律师事务所名称"),
            "原告委托诉讼代理人联系方式": plaintiff_lawyer_info.get("通讯电话"),
            "被告": accuser_company_info.get("法定代表人"),
            "被告性别": "女",
            "被告生日": "1975-02-12",
            "被告民族": "汉",
            "被告工作单位": accuser_company_info.get("公司名称"),
            "被告地址": accuser_company_info.get("企业地址"),
            "被告联系方式": accuser_company_info.get("联系电话"),
            "被告委托诉讼代理人": accuser_lawyer_info.get("律师事务所名称"),
            "被告委托诉讼代理人联系方式": accuser_lawyer_info.get("通讯电话"),
            "诉讼请求": claim,
            "事实和理由": reason,
            "证据": proof,
            "法院名称": court_info.get("法院名称"),
            "起诉日期": time_info,
        }

        result = get_citizens_sue_citizens(palyload)
        return result

    except Exception:
        return ""


def get_citizens_sue_company_service(
    plaintiff_company: str,
    accuser_company: str,
    plaintiff_lawyer: str,
    accuser_lawyer: str,
    claim: str,
    reason: str,
    proof: str,
    court: str,
    time: str,
):
    """
    公民起诉公司的诉讼状生成接口
    通过传入原告法人的公司名称、被告的公司名称、原告诉讼律师、被告诉讼律师、诉讼法院和宿舍时间，生成民事起诉状。
    例子：
        输入：
        {
        plaintiff_company: "北京碧水源科技股份有限公司",
        accuser_company: "江苏金迪克生物技术股份有限公司",
        plaintiff_lawyer: "北京国旺律师事务所",
        accuser_lawyer: "北京浩云律师事务所",
        claim:"民事纠纷",
        reason:"上诉",
        proof:"证据",
        court: "天津市蓟州区人民法院",
        time: "2024-02-01",
        }
        返回：起诉状字符串
    """
    try:
        # 获取原告法人信息
        plaintiff_company_info = json.loads(
            get_company_register_service(plaintiff_company)
        )[0]
        accuser_company_info = json.loads(
            get_company_register_service(accuser_company)
        )[0]
        plaintiff_lawyer_info = json.loads(get_lawfirm_info_service(plaintiff_lawyer))[
            0
        ]
        accuser_lawyer_info = json.loads(get_lawfirm_info_service(accuser_lawyer))[0]
        court_info = json.loads(get_court_info_service(court))[0]
        time_info = time
        palyload = {
            "原告": plaintiff_company_info.get("法定代表人"),
            "原告性别": "男",
            "原告生日": "1976-10-2",
            "原告民族": "汉",
            "原告工作单位": plaintiff_company_info.get("公司名称"),
            "原告地址": plaintiff_company_info.get("企业地址"),
            "原告联系方式": plaintiff_company_info.get("联系电话"),
            "原告委托诉讼代理人": plaintiff_lawyer_info.get("律师事务所名称"),
            "原告委托诉讼代理人联系方式": plaintiff_lawyer_info.get("通讯电话"),
            "被告": accuser_company_info.get("公司名称"),
            "被告地址": accuser_company_info.get("企业地址"),
            "被告法定代表人": accuser_company_info.get("法定代表人"),
            "被告联系方式": accuser_company_info.get("联系电话"),
            "被告委托诉讼代理人": accuser_lawyer_info.get("律师事务所名称"),
            "被告委托诉讼代理人联系方式": accuser_lawyer_info.get("通讯电话"),
            "诉讼请求": claim,
            "事实和理由": reason,
            "证据": proof,
            "法院名称": court_info.get("法院名称"),
            "起诉日期": time_info,
        }

        result = get_citizens_sue_company(palyload)
        return result

    except Exception:
        return ""


def get_company_sue_citizens_service(
    plaintiff_company: str,
    accuser_company: str,
    plaintiff_lawyer: str,
    accuser_lawyer: str,
    claim: str,
    reason: str,
    proof: str,
    court: str,
    time: str,
):
    """
    公民起诉公司的诉讼状生成接口
    通过传入原告公司名称、被告法人的公司名称、原告诉讼律师、被告诉讼律师、诉讼法院和宿舍时间，生成民事起诉状。
    例子：
        输入：
        {
        plaintiff_company: "北京碧水源科技股份有限公司",
        accuser_company: "江苏金迪克生物技术股份有限公司",
        plaintiff_lawyer: "北京国旺律师事务所",
        accuser_lawyer: "北京浩云律师事务所",
        claim:"民事纠纷",
        reason:"上诉",
        proof:"证据",
        court: "天津市蓟州区人民法院",
        time: "2024-02-01",
        }
        返回：起诉状字符串
    """
    try:
        # 获取原告法人信息
        plaintiff_company_info = json.loads(
            get_company_register_service(plaintiff_company)
        )[0]
        accuser_company_info = json.loads(
            get_company_register_service(accuser_company)
        )[0]
        plaintiff_lawyer_info = json.loads(get_lawfirm_info_service(plaintiff_lawyer))[
            0
        ]
        accuser_lawyer_info = json.loads(get_lawfirm_info_service(accuser_lawyer))[0]
        court_info = json.loads(get_court_info_service(court))[0]
        time_info = time
        """
        {
   ≈
    "诉讼请求": "AA纠纷",
    "事实和理由": "上诉",
    "证据": "PPPPP",
    "法院名称": "最高法",
    "起诉日期": "2012-09-08"
}
        """
        palyload = {
            "原告": plaintiff_company_info.get("公司名称"),
            "原告地址": plaintiff_company_info.get("企业地址"),
            "原告法定代表人": plaintiff_company_info.get("法定代表人"),
            "原告联系方式": plaintiff_company_info.get("联系电话"),
            "原告委托诉讼代理人": plaintiff_lawyer_info.get("律师事务所名称"),
            "原告委托诉讼代理人联系方式": plaintiff_lawyer_info.get("通讯电话"),
            "被告": accuser_company_info.get("法定代表人"),
            "被告性别": "女",
            "被告生日": "1975-02-12",
            "被告民族": "汉",
            "被告工作单位": accuser_company_info.get("公司名称"),
            "被告地址": accuser_company_info.get("企业地址"),
            "被告联系方式": accuser_company_info.get("联系电话"),
            "被告委托诉讼代理人": accuser_lawyer_info.get("律师事务所名称"),
            "被告委托诉讼代理人联系方式": accuser_lawyer_info.get("通讯电话"),
            "诉讼请求": claim,
            "事实和理由": reason,
            "证据": proof,
            "法院名称": court_info.get("法院名称"),
            "起诉日期": time_info,
        }

        result = get_company_sue_citizens(palyload)
        return result

    except Exception:
        return ""


def get_company_sue_company_service(
    plaintiff_company: str,
    accuser_company: str,
    plaintiff_lawyer: str,
    accuser_lawyer: str,
    claim: str,
    reason: str,
    proof: str,
    court: str,
    time: str,
):
    """
    公民起诉公司的诉讼状生成接口
    通过传入原告公司名称、被告公司名称、原告诉讼律师、被告诉讼律师、诉讼法院和宿舍时间，生成民事起诉状。
    例子：
        输入：
        {
        plaintiff_company: "北京碧水源科技股份有限公司",
        accuser_company: "江苏金迪克生物技术股份有限公司",
        plaintiff_lawyer: "北京国旺律师事务所",
        accuser_lawyer: "北京浩云律师事务所",
        claim:"民事纠纷",
        reason:"上诉",
        proof:"证据",
        court: "天津市蓟州区人民法院",
        time: "2024-02-01",
        }
        返回：起诉状字符串
    """
    try:
        # 获取原告法人信息
        plaintiff_company_info = json.loads(
            get_company_register_service(plaintiff_company)
        )[0]
        accuser_company_info = json.loads(
            get_company_register_service(accuser_company)
        )[0]
        plaintiff_lawyer_info = json.loads(get_lawfirm_info_service(plaintiff_lawyer))[
            0
        ]
        accuser_lawyer_info = json.loads(get_lawfirm_info_service(accuser_lawyer))[0]
        court_info = json.loads(get_court_info_service(court))[0]
        time_info = time
        """
        {
   ≈
    "诉讼请求": "AA纠纷",
    "事实和理由": "上诉",
    "证据": "PPPPP",
    "法院名称": "最高法",
    "起诉日期": "2012-09-08"
}
        """
        palyload = {
            "原告": plaintiff_company_info.get("公司名称"),
            "原告地址": plaintiff_company_info.get("企业地址"),
            "原告法定代表人": plaintiff_company_info.get("法定代表人"),
            "原告联系方式": plaintiff_company_info.get("联系电话"),
            "原告委托诉讼代理人": plaintiff_lawyer_info.get("律师事务所名称"),
            "原告委托诉讼代理人联系方式": plaintiff_lawyer_info.get("通讯电话"),
            "被告": accuser_company_info.get("公司名称"),
            "被告地址": accuser_company_info.get("企业地址"),
            "被告法定代表人": accuser_company_info.get("法定代表人"),
            "被告联系方式": accuser_company_info.get("联系电话"),
            "被告委托诉讼代理人": accuser_lawyer_info.get("律师事务所名称"),
            "被告委托诉讼代理人联系方式": accuser_lawyer_info.get("通讯电话"),
            "诉讼请求": claim,
            "事实和理由": reason,
            "证据": proof,
            "法院名称": court_info.get("法院名称"),
            "起诉日期": time_info,
        }

        result = get_company_sue_company(palyload)
        return result

    except Exception:
        return ""


if __name__ == "__main__":

    # print(
    #     get_citizens_sue_citizens_service(
    #         "北京碧水源科技股份有限公司",
    #         "南京仙林碧水源污水处理有限公司",
    #         "北京市金杜律师事务所",
    #         "爱德律师事务所",
    #         "民事纠纷",
    #         "上诉",
    #         "证据",
    #         "天津市蓟州区人民法院",
    #         "2024-02-01",
    #     )
    # )
    # print(
    #     get_citizens_sue_company_service(
    #         "北京碧水源科技股份有限公司",
    #         "南京仙林碧水源污水处理有限公司",
    #         "北京市金杜律师事务所",
    #         "爱德律师事务所",
    #         "民事纠纷",
    #         "上诉",
    #         "证据",
    #         "天津市蓟州区人民法院",
    #         "2024-02-01",
    #     )
    # )
    # print(
    #     get_company_sue_citizens_service(
    #         "北京碧水源科技股份有限公司",
    #         "南京仙林碧水源污水处理有限公司",
    #         "北京市金杜律师事务所",
    #         "爱德律师事务所",
    #         "民事纠纷",
    #         "上诉",
    #         "证据",
    #         "天津市蓟州区人民法院",
    #         "2024-02-01",
    #     )
    # )
    print(
        get_company_sue_company_service(
            "北京碧水源科技股份有限公司",
            "南京仙林碧水源污水处理有限公司",
            "北京市金杜律师事务所",
            "爱德律师事务所",
            "民事纠纷",
            "上诉",
            "证据",
            "天津市蓟州区人民法院",
            "2024-02-01",
        )
    )
    # print(
    #     save_dict_list_to_word_service(
    #         "北京碧水源科技股份有限公司",
    #         [
    #             {
    #                 "公司名称": "北京碧水源科技股份有限公司",
    #                 "登记状态": "存续",
    #                 "统一社会信用代码": "91110000802115985Y",
    #                 "参保人数": "351",
    #                 "行业一级": "科学研究和技术服务业",
    #                 "行业二级": "科技推广和应用服务业",
    #                 "行业三级": "其他科技推广服务业",
    #             }
    #         ],
    #         [
    #             {
    #                 "关联上市公司全称": "北京碧水源科技股份有限公司",
    #                 "上市公司关系": "子公司",
    #                 "上市公司参股比例": 100.0,
    #                 "上市公司投资金额": "1.06亿",
    #                 "公司名称": "北京碧海环境科技有限公司",
    #             }
    #         ],
    #         [
    #             {
    #                 "关联公司": "北京碧水源科技股份有限公司",
    #                 "原告": "四川帝宇水利水电工程有限公司",
    #                 "被告": "成都碧水源江环保科技有限公司,北京碧水源科技股份有限公司",
    #                 "案由": "建设工程施工合同纠纷",
    #                 "涉案金额": 0.0,
    #                 "日期": "2019-07-23 00:00:00",
    #             }
    #         ],
    #         [
    #             {
    #                 "限制高消费企业名称": "南京仙林碧水源污水处理有限公司",
    #                 "案号": "（2024）苏0113执1601号",
    #                 "申请人": "苏华建设集团有限公司",
    #                 "涉案金额": "-",
    #                 "立案日期": "2024-04-07 00:00:00",
    #                 "限高发布日期": "2024-06-24 00:00:00",
    #             }
    #         ],
    #     )
    # )
