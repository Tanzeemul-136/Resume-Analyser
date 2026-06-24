class Candidate:
    
    def __init__(
        self,
        name,
        email,
        skills
    ):
        
     # CHANGE THIS LINE FROM self.namev = name TO:
     self.name = name
     self.email = email
     self.skills = skills
     self.score = 0
    
    def set_score(self, score):
        self.score = score
        
    def get_data(self):
        return {
            "name": self.name,
            "email": self.email,
            "skills": self.skills,
            "score": self.score
        }