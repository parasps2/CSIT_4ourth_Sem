class ModelBasedAgent:
    def __init__(self):
        self.memory = []

    def perceive(self, environment):
        self.memory.append(environment)
        return f"Perceived: {environment}"

    def act(self):
        if "Dirty" in self.memory[-1]:
            return "Cleaning Dirt"
        elif "Obstacle" in self.memory[-1]:
            return "Avoiding Obstacle"
        else:
            return "Exploring"

# Example usage
agent = ModelBasedAgent()
environments = ["Clear", "Dirty", "Obstacle"]

for env in environments:
    print(agent.perceive(env))
    print(agent.act())
    print("Memory:", agent.memory)
    print("---")

 