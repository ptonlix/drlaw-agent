DATABASE_TABLE_INFO = """
1.公司计划表:
字段信息如下：
公司名称 = Column(Text, primary_key=True)
公司简称 = Column(Text)
英文名称 = Column(Text)
关联证券 = Column(Text)
公司代码 = Column(Text)
曾用简称 = Column(Text)
所属市场 = Column(Text)
所属行业 = Column(Text)
上市日期 = Column(Text)
法人代表 = Column(Text)
总经理 = Column(Text)
董秘 = Column(Text)
邮政编码 = Column(Text)
注册地址 = Column(Text)
办公地址 = Column(Text)
联系电话 = Column(Text)
传真 = Column(Text)
官方网址 = Column(Text)
电子邮箱 = Column(Text)
入选指数 = Column(Text)
主营业务 = Column(Text)
经营范围 = Column(Text)
机构简介 = Column(Text)
每股面值 = Column(Text)
首发价格 = Column(Text)
首发募资净额 = Column(Text)
首发主承销商 = Column(Text)

2.公司注册表
字段信息如下：：
公司名称 = Column(Text, primary_key=True, default='')
登记状态 = Column(Text, default='')
统一社会信用代码 = Column(Text, default='')
注册资本 = Column(Text, default='') # 单位：万元
成立日期 = Column(Text, default='')
省份 = Column(Text, default='')
城市 = Column(Text, default='')
区县 = Column(Text, default='')
注册号 = Column(Text, default='')
组织机构代码 = Column(Text, default='')
参保人数 = Column(Text, default='')
企业类型 = Column(Text, default='')
曾用名 = Column(Text, default='')

3.关联子公司信息表:
字段信息如下:
关联上市公司股票代码 = Column(Text, default='')
关联上市公司股票简称 = Column(Text, default='')
关联上市公司全称 = Column(Text, default='')
上市公司关系 = Column(Text, default='')
上市公司参股比例 = Column(Text, default='')
上市公司投资金额 = Column(Text, default='')
公司名称 = Column(Text, primary_key=True, default='')

4.法律文书信息表:
字段信息如下:
标题 = Column(Text, default='')
案号 = Column(Text, default='', primary_key=True)
文书类型 = Column(Text, default='')
原告 = Column(Text, default='')
被告 = Column(Text, default='')
原告律师 = Column(Text, default='')
被告律师 = Column(Text, default='')
案由 = Column(Text, default='')
审理法条依据 = Column(Text, default='')
涉案金额 = Column(Text, default='')
判决结果 = Column(Text, default='')
胜诉方 = Column(Text, default='')
文件名 = Column(Text, default='')
"""


DATABASE_API_INFO = """
API1:
基本描述：根据公司基本信息某个字段是某个值来查询具体的公司名称
输入参数: 公司基本信息字段:输入信息
返回值: 符合条件的公司名称列表
API2：
基本描述：根据公司名称获得该公司所有基本信息
输入参数: 公司名称
返回值: 公司详细信息
API3:
基本描述：根据公司注册信息某个字段是某个值来查询具体的公司名称
输入参数: 公司注册信息字段：输入信息
返回值: 符合条件的公司名称列表
API3:
基本描述：根据公司注册信息某个字段是某个值来查询具体的公司名称
输入参数: 公司注册信息字段：输入信息
返回值: 符合条件的公司名称列表
"""
