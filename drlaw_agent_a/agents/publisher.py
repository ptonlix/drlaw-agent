from drlaw_agent.agents.utils.views import print_agent_output
import jsonlines


class PublisherAgent:

    def __init__(self):
        pass

    async def run(self, research_state: dict):
        task = research_state.get("task")
        errlog = task.get("errlog")
        result_output_dir = task.get("result_output_dir")
        answer = research_state.get("answer")
        toolkits = research_state.get("toolkits")
        print_agent_output(
            output=f"Publishing final question answer:\n{answer}\n",
            agent="PUBLISHER",
        )

        content = {
            "id": task.get("index"),
            "question": task.get("query"),
            "answer": answer,
            "toolkits": toolkits,
        }
        with jsonlines.open(result_output_dir + "/result.json", "a") as json_file:
            json_file.write(content)

        if research_state.get("iferror"):
            content["error"] = research_state.get("errorinfo")
            print(errlog + "/answer_error.jsonl")
            with jsonlines.open(errlog + "/answer_error.jsonl", "a") as json_file:
                json_file.write(content)
