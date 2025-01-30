import pandas as pd


def confusion_matrix(df):
    tp = ((df["predicted_score"] == 1) & (df["actual_score"] == 1)).sum()
    fp = ((df["predicted_score"] == 1) & (df["actual_score"] == 0)).sum()
    tn = ((df["predicted_score"] == 0) & (df["actual_score"] == 0)).sum()
    fn = ((df["predicted_score"] == 0) & (df["actual_score"] == 1)).sum()
    return tp, fp, tn, fn


class CategoricalGroupPredictionInformation:
    def __init__(self, application_subset: pd.DataFrame):
        self.total = len(application_subset)

        (self.hired_and_competent,
         self.hired_but_not_competent,
         self.not_hired_but_competent,
         self.not_hired_and_not_competent) = confusion_matrix(application_subset)

        self.hired = (application_subset["predicted_score"] == 1).sum()
        self.hired_rate = self.hired / self.total
        self.not_hired = (application_subset["predicted_score"] == 0).sum()
        self.not_hired_rate = self.not_hired / self.total
        self.correct = (application_subset["predicted_score"] == application_subset["actual_score"]).sum()
        self.correct_rate = self.correct / self.total
        self.incorrect = (application_subset["predicted_score"] != application_subset["actual_score"]).sum()
        self.incorrect_rate = self.incorrect / self.total
        self.competent = (application_subset["actual_score"] == 1).sum()
        self.competent_rate = self.competent / self.total
        self.not_competent = (application_subset["actual_score"] == 0).sum()
        self.not_competent_rate = self.not_competent / self.total

        self.accuracy = self.correct / self.total
        self.false_negative_rate = self.not_hired_and_not_competent / self.competent
        self.false_positive_rate = self.hired_but_not_competent / self.not_competent
        self.false_discovery_rate = self.hired_but_not_competent / self.hired
        self.false_omission_rate = self.not_hired_and_not_competent / self.not_hired
