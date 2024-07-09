from drlaw_agent.agents.utils.views import print_agent_output
import jsonlines


class PublisherAgent:
    """
    客户:将问题答案答复客户
    """

    def __init__(self):
        pass

    async def run(self, drlaw_state: dict):
        print_agent_output("客服助理正在将问题答案答复客户", agent="PUBLISHER")

        task = drlaw_state.get("task")
        result_output_dir = task.get("result_output_dir")
        answer = drlaw_state.get("answer")
        call_agents = drlaw_state.get("call_agents")

        content = {
            "id": task.get("index"),
            "question": task.get("query"),
            "answer": answer,
            "call_agents": call_agents,
        }
        with jsonlines.open(result_output_dir + "/result.json", "a") as json_file:
            json_file.write(content)
