from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from datetime import datetime
from drlaw_agent_a.agents.utils.views import print_agent_output


class AnswerAgent:

    def __init__(self):
        pass

    def answer_without_tools(self, model: str, query: str) -> str:
        SYSTEM_MESSAGE = "你是一个擅长回答金融和法律有关的问题的专家，会利用自己能力来检索信息，通过一步一步拆解并分析问题，最终得出最准确的答案。\n当前日期:{current_date}"

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_MESSAGE),
                ("human", "{query}"),
            ]
        ).partial(
            current_date=datetime.now().isoformat(),
        )

        answer = prompt | ChatOpenAI(model=model, temperature=0.1) | StrOutputParser()

        return answer.invoke({"query": query})

    def run(self, research_state: dict):
        task = research_state.get("task")

        query = task.get("query")
        model_name = task.get("model")
        print_agent_output(
            f"Running answer_without_tools on the following query and tools:\n {query}",
            agent="ANSWERER",
        )

        return {
            "task": task,
            "answer": self.answer_without_tools(model_name, query=query),
            "iferror": False if not research_state.get("iferror") else True,
            "reselect_num": research_state.get("reselect_num"),
        }
