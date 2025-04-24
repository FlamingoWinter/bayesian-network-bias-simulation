class CharacteristicName:
    def __init__(self, name: str, values: list[str] = None, hml=False):
        self.name = name
        self.values = values
        self.hml = hml

    def set_number_values(self, num_values: int) -> 'CharacteristicName':
        if self.hml:
            self.values = ["V. High", "High", "Medium", "Low", "V. Low"]
            if num_values == 2:
                self.values = ["High", "Low"]
            if num_values == 3:
                self.values = ["High", "Medium", "Low"]
            if num_values == 4:
                self.values = ["Very High", "High", "Low", "Very Low"]
        if num_values is not None:
            self.values = self.values[:num_values]

        return self


protected_characteristics = [
    CharacteristicName("Gender", ["Male", "Female", "Non-Binary", "Other"]),
    CharacteristicName("Race", ["White", "Black", "Asian", "Hispanic", "Other"]),
    CharacteristicName("Religion or Belief", ["Christian", "Muslim", "Jewish", "Hindu", "Other"]),
    CharacteristicName("Sexual Orientation", ["Heterosexual", "Homosexual", "Bisexual", "Other"]),
    CharacteristicName("Gender Identity", ["Cisgender", "Transgender", "Non-Binary", "Other"]),
    CharacteristicName("Age", ["18-30", "31-40", "41-50", "51-60", "61+"]),
    CharacteristicName("Marital Status", ["Married", "Single", "Divorced", "Widowed"]),
    CharacteristicName("Family Income Class", ["High Upper Class", "Upper Class", "Middle Class", "Lower Class"]),
    CharacteristicName("School Attended", ["Private", "State", "Selective"]),
]

hide_protected_characteristics = True

intermediary_characteristics = [
    CharacteristicName("Education Opportunities", hml=True),
    CharacteristicName("Work Experience Opportunities", hml=True),
    CharacteristicName("Networking Opportunities", hml=True),
    CharacteristicName("Encouragement to Pursue Job from Family", hml=True),
    CharacteristicName("Encouragement to Pursue Job from Friends", hml=True),
    CharacteristicName("Geographical Mobility", hml=True),
    CharacteristicName("Exposure to Role Models", hml=True),
    CharacteristicName("Confidence in Abilities", hml=True),
    CharacteristicName("Nutritional Access", hml=True),
    CharacteristicName("Healthcare Access", hml=True),
    CharacteristicName("Mental Health Stability", hml=True),
    CharacteristicName("Happiness Within Community", hml=True),
    CharacteristicName("Access to Career Advice", hml=True),
    CharacteristicName("Success on First Impression", hml=True),
    CharacteristicName("Exposure to Threats or Violence", hml=True),
    CharacteristicName("Financial Stability", hml=True),
    CharacteristicName("Pressure of Other Responsibilities", hml=True),
]

affector_characteristics = [
    CharacteristicName("Education", hml=True),
    CharacteristicName("Learning Ability", hml=True),
    CharacteristicName("Cognitive Ability", hml=True),
    CharacteristicName("Interpersonal Skills", hml=True),
    CharacteristicName("Technical Skills", hml=True),
    CharacteristicName("Technical Knowledge", hml=True),
    CharacteristicName("Creative Skills", hml=True),
    CharacteristicName("Analytical Skills", hml=True),
    CharacteristicName("Written Communication Skills", hml=True),
    CharacteristicName("Job Motivation", hml=True),
    CharacteristicName("Conflict Resolution Skills", hml=True),
    CharacteristicName("Leadership Ability", hml=True),
    CharacteristicName("Emotional Intelligence", hml=True),

]

affected_characteristics = [
    CharacteristicName("Interview Performance", hml=True),
    CharacteristicName("Resume Quality", hml=True),
    CharacteristicName("Employee Test Performance", hml=True),
    CharacteristicName("Previous Job Performance", hml=True),
    CharacteristicName("Trial Period Performance", hml=True),
    CharacteristicName("Internship Performance", hml=True),
    CharacteristicName("Commendations from Co-Workers", hml=True),
    CharacteristicName("Job Satisfaction", hml=True),
]

score_characteristic = CharacteristicName("Job Competency", ["Competent", "Not Competent"])
