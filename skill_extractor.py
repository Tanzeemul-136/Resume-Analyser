import pandas as pd

class SkillExtractor:
    def __init__(self):
        self.skills = pd.read_csv(
            "data/skills.csv"
        )["skills"].tolist()
        
    def extract(
        self,
        text
    ):
        
        found=[]
        for skill in self.skills:
            if skill.lower() in text.lower():
                found.append(skill)
        return found
        
    