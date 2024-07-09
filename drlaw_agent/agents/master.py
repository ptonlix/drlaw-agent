from langgraph.graph import StateGraph, END
from drlaw_agent.agents.publisher import PublisherAgent
from drlaw_agent.agents.assistanter import AssistanterAgent
from drlaw_agent.agents.companyer import CompanyerAgent
from drlaw_agent.agents.legaler import LegalerAgent
from drlaw_agent.agents.courter import CourterAgent
from drlaw_agent.agents.lawfirmer import LawfirmerAgent
from drlaw_agent.agents.xzgxfer import XzgxferAgent
from drlaw_agent.agents.addresser import AddresserAgent
from drlaw_agent.agents.reporter import ReporterAgent
from drlaw_agent.agents.indictmenter import IndictmenterAgent
from drlaw_agent.agents.errorer import ErrorerAgent
from drlaw_agent.agents.utils.views import print_agent_output
from drlaw_agent.agents.utils.model import AgentTypeService
from drlaw_agent.memory.drlaw import DrlawState
from langgraph.checkpoint.memory import MemorySaver


def check_assistant(state: dict) -> str:
    return state["agent_type"]


class DrlawAgent:
    def __init__(self, task: dict):
        self.task = task

    def init_drlaw_team(self):
        # Initialize agents

        assistanter_agent = AssistanterAgent()
        companyer_agent = CompanyerAgent()
        legaler_agent = LegalerAgent()
        courter_agent = CourterAgent()
        lawfirmer_agent = LawfirmerAgent()
        xzgxfer_agent = XzgxferAgent()
        addresser_agent = AddresserAgent()
        reporter_agent = ReporterAgent()
        indictmenter_agent = IndictmenterAgent()
        errorer_agent = ErrorerAgent()

        publisher_agent = PublisherAgent()
        # Define a Langchain StateGraph with the ResearchState
        workflow = StateGraph(DrlawState)

        # Add nodes for each agent
        workflow.add_node("assistanter", assistanter_agent.run)
        workflow.add_node("companyer", companyer_agent.run)
        workflow.add_node("legaler", legaler_agent.run)
        workflow.add_node("courter", courter_agent.run)
        workflow.add_node("lawfirmer", lawfirmer_agent.run)
        workflow.add_node("xzgxfer", xzgxfer_agent.run)
        workflow.add_node("addresser", addresser_agent.run)
        workflow.add_node("reporter", reporter_agent.run)
        workflow.add_node("indictmenter", indictmenter_agent.run)
        workflow.add_node("errorer", errorer_agent.run)
        workflow.add_node("publisher", publisher_agent.run)

        workflow.set_entry_point("assistanter")

        workflow.add_conditional_edges(
            "assistanter",
            check_assistant,
            AgentTypeService,
        )

        workflow.add_edge("companyer", "assistanter")
        workflow.add_edge("legaler", "assistanter")
        workflow.add_edge("courter", "assistanter")
        workflow.add_edge("lawfirmer", "assistanter")
        workflow.add_edge("xzgxfer", "assistanter")
        workflow.add_edge("addresser", "assistanter")
        workflow.add_edge("reporter", "assistanter")
        workflow.add_edge("indictmenter", "assistanter")

        # set up start and end nodes
        workflow.add_edge("publisher", END)
        workflow.add_edge("errorer", END)

        return workflow

    async def run_drlaw_task(self, thread_id: int):
        research_team = self.init_drlaw_team()

        # compile the graph
        memory = MemorySaver()
        chain = research_team.compile(checkpointer=memory)

        print_agent_output(
            f"Starting the research process for query '{self.task.get('query')}'...",
            "MASTER",
        )
        result = await chain.ainvoke(
            input={"task": self.task}, config={"configurable": {"thread_id": thread_id}}
        )
        return result
