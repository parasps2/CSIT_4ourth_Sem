class SimpleReflexAgent:
    def __init__(self):
        pass

    def perceive(self, environment):
        if environment == "Dirty":
            return "Clean"
        elif environment == "Obstacle":
            return "Turn"
        else:
            return "Move Forward"

    def act(self, perception):
        return f"Action: {perception}"

# Example usage
agent = SimpleReflexAgent()
environments = ["Dirty", "Clear", "Obstacle"]

for env in environments:
    perception = agent.perceive(env)
    print(agent.act(perception))
    print("---")

 