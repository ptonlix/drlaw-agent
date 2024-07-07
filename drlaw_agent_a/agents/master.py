from langgraph.graph import StateGraph, END
from drlaw_agent.agents import publisher
from drlaw_agent.agents.utils.views import print_agent_output
from drlaw_agent.memory.research import ResearchState

# Import agent classes
from drlaw_agent.agents.executor import (
    ExecutorAgent,
)

from drlaw_agent.agents.toolselect import (
    ToolSelectAgent,
)
from drlaw_agent.agents.publisher import (
    PublisherAgent,
)
from drlaw_agent.agents.answer import AnswerAgent
from drlaw_agent.agents.reviewer import ReviewerAgent


def check_execution_effect(research_state: dict):
    iferror = research_state.get("iferror")

    if iferror:
        return "answerer"
    else:
        return "reviewer"


def check_tool_select(research_state: dict):
    toolkits = research_state.get("toolkits")
    # 输入的答案包含函数调用,则重新执行
    if len(toolkits) == 0:
        return "answerer"
    else:
        return "executor"


def check_review_effect(research_state: dict):

    review = research_state.get("review")

    if review:
        return "publish"
    else:
        return "reselect"


class DrlawAgent:
    def __init__(self, task: dict):
        self.task = task

    def init_research_team(self):
        # Initialize agents

        exec_agent = ExecutorAgent()
        producer_agent = ToolSelectAgent()
        publisher_agent = PublisherAgent()
        answer_agent = AnswerAgent()
        reviewer_agent = ReviewerAgent()

        # Define a Langchain StateGraph with the ResearchState
        workflow = StateGraph(ResearchState)

        # Add nodes for each agent
        workflow.add_node("toolselect", producer_agent.tool_select)
        workflow.add_node("executor", exec_agent.produce_assistant)
        workflow.add_node("publisher", publisher_agent.run)
        workflow.add_node("answerer", answer_agent.run)
        workflow.add_node("reviewer", reviewer_agent.answer_review)

        workflow.set_entry_point("toolselect")

        workflow.add_conditional_edges(
            "toolselect",
            check_tool_select,
            {"answerer": "answerer", "executor": "executor"},
        )

        workflow.add_conditional_edges(
            "executor",
            check_execution_effect,
            {"answerer": "answerer", "reviewer": "reviewer"},
        )

        workflow.add_edge("answerer", "reviewer")

        workflow.add_conditional_edges(
            "reviewer",
            check_review_effect,
            {"publish": "publisher", "reselect": "toolselect"},
        )

        # set up start and end nodes
        workflow.add_edge("publisher", END)

        return workflow

    async def run_research_task(self):
        research_team = self.init_research_team()

        # compile the graph
        chain = research_team.compile()

        print_agent_output(
            f"Starting the research process for query '{self.task.get('query')}'...",
            "MASTER",
        )
        result = await chain.ainvoke({"task": self.task})

        return result
