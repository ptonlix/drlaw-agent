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
        print(drlaw_state)

        task = research_state.get("task")
        # errlog = task.get("errlog")
        # result_output_dir = task.get("result_output_dir")
        # answer = research_state.get("answer")
        # toolkits = research_state.get("toolkits")
        # print_agent_output(
        #     output=f"Publishing final question answer:\n{answer}\n",
        #     agent="PUBLISHER",
        # )

        # content = {
        #     "id": task.get("index"),
        #     "question": task.get("query"),
        #     "answer": answer,
        #     "toolkits": toolkits,
        # }
        # with jsonlines.open(result_output_dir + "/result.json", "a") as json_file:
        #     json_file.write(content)

        # if research_state.get("iferror"):
        #     content["error"] = research_state.get("errorinfo")
        #     print(errlog + "/answer_error.jsonl")
        #     with jsonlines.open(errlog + "/answer_error.jsonl", "a") as json_file:
        #         json_file.write(content)
