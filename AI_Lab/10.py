# Comparison demonstration with examples

agents = {
    "Simple Reflex": "Acts only on current percept (e.g., vacuum cleaner).",
    "Model-Based": "Uses memory of past states (e.g., robot remembering obstacles).",
    "Goal-Based": "Acts to achieve a goal (e.g., navigation to destination).",
    "Utility-Based": "Chooses best action using utility values (e.g., self-driving car optimizing safety and speed)."
}

for agent, description in agents.items():
    print(f"{agent} Agent -> {description}")

