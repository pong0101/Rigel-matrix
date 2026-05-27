from agents import build_default_agents
from core.memory_store import save_event


def process_task(task):
    agents = build_default_agents()
    result = {name: f'{role}: {task}' for name, role in agents.items()}
    save_event(task, result)
    return result
