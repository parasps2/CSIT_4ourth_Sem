class MedicalDiagnosisAgent:
    def __init__(self):
        self.diagnosis = None

    def perceive(self, symptoms):
        if "fever" in symptoms and "cough" in symptoms:
            return "Possible Flu"
        elif "chest pain" in symptoms:
            return "Possible Heart Issue"
        else:
            return "Unknown Condition"

    def act(self, perception):
        self.diagnosis = perception
        return f"Diagnosis: {perception}"

# Example usage
agent = MedicalDiagnosisAgent()
patients = [["fever", "cough"], ["chest pain"], ["headache"]]

for symptoms in patients:
    perception = agent.perceive(symptoms)
    print(agent.act(perception))
    print("---")

