from drlaw_agent.apis.base import CallLogger


def get_api_info_service() -> str:
    """
    查询API种类(个数)信息、调用次数、串行调用API种类(个数)、最小调用次数、最优串行次数等信息
    """
    call_log = CallLogger()
    # seq = call_log.get_call_sequence()
    # call_count = call_log.get_call_count()
    total_calls = call_log.get_total_calls()
    call_type = call_log.get_call_types()

    # 定义一个查询条件的列表，包含所有可能的查询条件
    # 如果没有找到任何信息，返回错误消息
    return f"本轮API调用信息如下:\n1.调用API种类(个数):{len(call_type)}个,分别是{call_type}\
2.本轮共调用API{total_calls}次\n3.最小调用次数为:{len(call_type)}次\n4.串行调用API种类(个数)为{len(call_type)}个5.最优串行次数为{len(call_type)}次"
