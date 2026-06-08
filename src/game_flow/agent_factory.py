from src.agents.human_agent import HumanAgent
from src.agents.llm_agent import LLMAgent
from src.game_options import AgentType


class AgentBuilder:
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type

    def build_agent(self):
        if self.agent_type == AgentType.HUMAN:
            return HumanAgent()
        else:
            return LLMAgent(self.agent_type)
