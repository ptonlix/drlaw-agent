from dotenv import load_dotenv
from drlaw_agent.agents.master import DrlawAgent
from drlaw_agent.utils import read_jsonl
from tqdm import tqdm
import asyncio
import json

from pathlib import Path

PROJECT_ROOT_PATH: Path = Path(__file__).parents[1]

load_dotenv()


def open_task():
    with open(PROJECT_ROOT_PATH / "task.json", "r") as f:
        task = json.load(f)

    if not task:
        raise Exception(
            "No task provided. Please include a task.json file in the root directory."
        )

    return task


async def main():
    task = open_task()

    question_file = task.get("question_file")
    if question_file:
        queries = read_jsonl(question_file)
        for query in tqdm(queries):
            # 如果中断，可以从这里开始
            if query["id"] < 211:
                continue
            task["index"] = query["id"]
            task["query"] = query["question"]
            drlaw = DrlawAgent(task)
            await drlaw.run_drlaw_task()
            task = open_task()  # 状态初始化
    else:
        drlaw = DrlawAgent(task)
        await drlaw.run_drlaw_task(thread_id=task["index"])


if __name__ == "__main__":
    asyncio.run(main())
