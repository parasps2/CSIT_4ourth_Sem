class VacuumCleanerReflexAgent:
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
agent = VacuumCleanerReflexAgent()
environments = [True, False, True, False]

for dirt in environments:
    perception = agent.perceive(dirt)
    print(perception)
    print(agent.act(perception))
    print("---")

 