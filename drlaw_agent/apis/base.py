import os
import functools
from typing import Callable, Any, List, Dict

DOMAIN = "comm.chatglm.cn"
TEAM_TOKEN = os.environ.get("TEAM_TOKEN")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {TEAM_TOKEN}"}

# 调用情况变量
global_call_data = {"call_sequence": [], "call_count": {}}


def record_call(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Record the function name in the call sequence
        global_call_data["call_sequence"].append(func.__name__)

        # Increment the function call count
        if func.__name__ in global_call_data["call_count"]:
            global_call_data["call_count"][func.__name__] += 1
        else:
            global_call_data["call_count"][func.__name__] = 1

        return func(*args, **kwargs)

    return wrapper


class CallLogger:

    def reset(self):
        global global_call_data
        global_call_data = {"call_sequence": [], "call_count": {}}

    def get_call_sequence(self) -> List[str]:
        return global_call_data["call_sequence"]

    def get_call_count(self) -> Dict[str, int]:
        return global_call_data["call_count"]

    def get_total_calls(self) -> int:
        return sum(global_call_data["call_count"].values())

    def get_call_types(self) -> List[str]:
        call_types = []
        for func_name in global_call_data["call_sequence"]:
            if func_name not in call_types:
                call_types.append(func_name)
        return call_types
