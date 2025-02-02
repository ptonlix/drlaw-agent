from colorama import Fore, Style
from enum import Enum


class AgentColor(Enum):
    TOOLSELECT = Fore.LIGHTBLUE_EX
    EXECUTOR = Fore.YELLOW
    ANSWERER = Fore.LIGHTGREEN_EX
    PUBLISHER = Fore.MAGENTA
    REVIEWER = Fore.CYAN
    MASTER = Fore.LIGHTYELLOW_EX


def print_agent_output(output: str, agent: str = "RESEARCHER"):
    print(f"{AgentColor[agent].value}{agent}: {output}{Style.RESET_ALL}")
