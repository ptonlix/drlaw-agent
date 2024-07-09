from colorama import Fore, Style
from enum import Enum


class AgentColor(Enum):
    ASSISTANT = Fore.LIGHTBLUE_EX
    COMPANYER = Fore.YELLOW
    LEGALER = Fore.LIGHTGREEN_EX
    ADDRESSER = Fore.CYAN
    APIER = Fore.BLUE
    COURTER = Fore.GREEN
    LAWFIRMER = Fore.LIGHTBLUE_EX
    XZGXFER = Fore.LIGHTYELLOW_EX
    INDICTMENTER = Fore.LIGHTCYAN_EX
    REPORTER = Fore.LIGHTBLUE_EX
    ERRORER = Fore.RED
    PUBLISHER = Fore.MAGENTA
    MASTER = Fore.LIGHTYELLOW_EX


def print_agent_output(output: str, agent: str = "RESEARCHER"):
    print(f"{AgentColor[agent].value}{agent}: {output}{Style.RESET_ALL}")
