class UtilityBasedAgent:
    def __init__(self):
        pass

    def evaluate(self, options):
        # options is a dict {action: utility_value}
        best_action = max(options, key=options.get)
        return best_action, options[best_action]

    def act(self, options):
        action, utility = self.evaluate(options)
        return f"Chosen Action: {action}, Utility: {utility}"

# Example usage
agent = UtilityBasedAgent()
options = {"Clean": 8, "Move Forward": 5, "Avoid Obstacle": 7}

print(agent.act(options)) 
