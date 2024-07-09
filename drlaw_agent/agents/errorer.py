from drlaw_agent.agents.utils.views import print_agent_output
import jsonlines


class ErrorerAgent:
    """
    错误信息助理:
    记录各类异常信息
    """

    def __init__(self):
        pass

    async def run(self, drlaw_state: dict):
        print_agent_output("错误信息助理正在输出错误信息", agent="ERRORER")

        task = drlaw_state.get("task")
        errormsg = drlaw_state.get("messages")
        errlog = task.get("errlog")
        call_agents = drlaw_state.get("call_agents")

        content = {
            "id": task.get("index"),
            "question": task.get("query"),
            "answer": errormsg,
            "call_agents": call_agents,
        }

        with jsonlines.open(errlog + "/answer_error.jsonl", "a") as json_file:
            json_file.write(content)
