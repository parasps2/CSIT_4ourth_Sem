class VacuumCleanerAgent:
    def __init__(self):
        self.cleaned = 0

    def perceive(self, dirt_present):
        return "Dirt Detected" if dirt_present else "No Dirt"

    def act(self, perception):
        if perception == "Dirt Detected":
            self.cleaned += 1
            return "Cleaning Dirt"
        else:
            return "Moving Forward"

# Example usage
agent = VacuumCleanerAgent()
environments = [True, False, True]

for dirt in environments:
    perception = agent.perceive(dirt)
    print(perception)
    print(agent.act(perception))
    print("---")

