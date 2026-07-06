class GoalBasedAgent:
    def __init__(self, goal):
        self.goal = goal
        self.position = 0

    def perceive(self, environment):
        if environment == "Obstacle":
            return "Avoid"
        elif self.position < self.goal:
            return "Move Forward"
        else:
            return "Goal Reached"

    def act(self, perception):
        if perception == "Move Forward":
            self.position += 1
        elif perception == "Avoid":
            self.position += 0  # stays in place
        return f"Action: {perception}, Position: {self.position}"

# Example usage
agent = GoalBasedAgent(goal=3)
environments = ["Clear", "Obstacle", "Clear", "Clear"]

for env in environments:
    perception = agent.perceive(env)
    print(agent.act(perception))
    print("---")

 