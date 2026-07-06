class SelfDrivingCarAgent:
    def __init__(self):
        self.speed = 0

    def perceive(self, environment):
        if environment == "Red Light":
            return "Stop"
        elif environment == "Clear Road":
            return "Accelerate"
        elif environment == "Obstacle":
            return "Brake"
        else:
            return "Maintain Speed"

    def act(self, perception):
        if perception == "Stop":
            self.speed = 0
        elif perception == "Accelerate":
            self.speed += 10
        elif perception == "Brake":
            self.speed -= 10
        return f"Action: {perception}, Speed: {self.speed}"

# Example usage
car = SelfDrivingCarAgent()
environments = ["Clear Road", "Red Light", "Obstacle"]

for env in environments:
    perception = car.perceive(env)
    print(car.act(perception))
    print("---")

