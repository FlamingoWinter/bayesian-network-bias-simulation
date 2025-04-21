from typing import Dict, Callable

import pandas as pd

from backend.api.responseTypes.recruiter_bias_analysis_response import \
    RecruiterBiasAnalysisResponse
from backend.bias.group_prediction_information import GroupPredictionInformation
from backend.network.bayesian_network import Characteristic
from backend.utilities.capitalise_first import capitalise_first


class MitigationBiasAnalysis:
    def __init__(self, applications: pd.DataFrame, protected_characteristic: Characteristic):
        # Requires that application has a categorical column "group" denoting whether it is in the biased group,
        # a categorical column "predicted_score" and a categorical column "actual_score",
        # with 0 or 1 for rejected/not competent or hired/competent.
        super().__init__()

        self.general = GroupPredictionInformation(applications)

        self.by_group: Dict[str, GroupPredictionInformation] = {}

        for group_index, group in enumerate(protected_characteristic.category_names):
            application_subset = applications[applications["group"] == group_index]
            if len(application_subset) > 0:
                self.by_group[group] = GroupPredictionInformation(application_subset)

    def print_summary(self):
        s = ""
        s += self.get_pretty_performance_summary()

        s += get_pretty_title("Demographic Parity (Independence)")
        s += self.get_pretty_metric(lambda info: info.hired_rate,
                                    "Proportion of People Hired",
                                    "a random person from group {max_group} is {percentage} more likely to be hired than a person from group {min_group}.",
                                    with_competence=True)

        s += get_pretty_title("Equalised Odds (Separation)")

        s += self.get_pretty_metric(lambda info: info.false_negative_rate,
                                    "False Negative Rate",
                                    "a random competent person from group {max_group} is {percentage} more likely to be rejected than a random competent person from group {min_group}.",
                                    positive_correlation_between_metric_and_advantage=False)

        s += get_space()

        s += self.get_pretty_metric(lambda info: info.false_positive_rate,
                                    "False Positive Rate",
                                    "a random person from group {max_group} who isn't competent is {percentage} more likely to be hired than a random person from group {min_group} who also isn't competent.")

        s += get_pretty_title("Predictive Parity (Sufficiency)")

        s += self.get_pretty_metric(lambda info: info.false_discovery_rate,
                                    "False Discovery Rate",
                                    "a random hired person from group {max_group} is {percentage} more likely to not be competent than a random hired person from group {min_group}.")

        s += get_space()

        s += self.get_pretty_metric(lambda info: info.false_omission_rate,
                                    "False Omission Rate",
                                    "a random rejected person from group {max_group} is {percentage} more likely to actually be competent than a random rejected person from group {min_group}.",
                                    positive_correlation_between_metric_and_advantage=False)
        print(s)

    def get_pretty_performance_summary(self) -> str:
        group = self.general

        return get_pretty_title("Performance") + f"""
        Model Accuracy: {group.accuracy:.2g}
        
        Proportion of People Hired: {group.hired_rate}
            Proportion of People Competent: {group.competent_rate:.2g}
        
        False Positive Rate: {group.false_positive_rate:.2g}
            (Of people who weren't competent, how many got hired anyway?)
        
        False Negative Rate: {group.false_negative_rate:.2g}
            (Of people who were competent, how many didn't get hired?)
        
        False Discovery Rate: {group.false_discovery_rate:.2g}
            (Of people hired, how many weren't actually competent?)
        
        False Omission Rate: {group.false_omission_rate:.2g}
            (Of people not hired, how many were actually competent?)"""

    def get_pretty_metric(self, find_metric: Callable[[GroupPredictionInformation], float],
                          metric_english_name: str, explanation: str,
                          with_competence=False,
                          positive_correlation_between_metric_and_advantage=True) -> str:
        s = ""
        for group_name, info in self.by_group.items():
            s += f"""
        {metric_english_name} in group {group_name}: {find_metric(info):.2g}"""

        metric_and_group_names = [(find_metric(info), group_name) for [group_name, info] in self.by_group.items()]
        min_rate, min_group = min(metric_and_group_names)
        max_rate, max_group = max(metric_and_group_names)
        percentage = (max_rate / min_rate - 1) * 100
        formatted_percentage = f"{float(f'{percentage:.2g}'):.0f}%"

        if len(self.by_group) > 2:
            s += f"""
            The biggest difference among groups in the proportion of people hired is {min_group} and {max_group}, 
            where """ + explanation.format(min_group=min_group, max_group=max_group, percentage=formatted_percentage)
        else:
            s += f"""
            
        {capitalise_first(explanation.format(min_group=min_group, max_group=max_group, percentage=formatted_percentage))}"""

        superlative = ("minimal" if percentage < 2 else
                       "subtle" if percentage < 10 else
                       "moderate" if percentage < 25 else  # For demographic parity, this breaks the disparate impact, and could be illegal in some contexts.
                       "significant")

        s += f"""
        
        ** By this metric,{" and if we assume these groups should have the same chance at attaining a job," if with_competence else ""} there is a {superlative} bias for group {
        min_group if not positive_correlation_between_metric_and_advantage else max_group
        } and against group {
        max_group if not positive_correlation_between_metric_and_advantage else min_group
        }"""

        if with_competence:
            min_competence = self.by_group[min_group].competent_rate
            max_competence = self.by_group[max_group].competent_rate
            if min_competence > max_competence:
                min_group, max_group = max_group, min_group
                min_competence, max_competence = max_competence, min_competence
            percentage = (max_competence / min_competence - 1) * 100
            formatted_percentage = f"{float(f'{percentage:.2g}'):.0f}%"

            s += f"""
            
        (A random person from group {max_group} is {formatted_percentage} more likely to be competent than one from group {min_group}):"""
            for group_name, info in self.by_group.items():
                s += f"""
        Proportion of People Competent in group {group_name}: {info.competent_rate:.2g}"""

        return s

    def to_response(self) -> RecruiterBiasAnalysisResponse:
        return {
            "general": self.general.to_response(),
            "byGroup": {g_name: g.to_response() for g_name, g in self.by_group.items()}
        }


def get_pretty_title(title: str) -> str:
    return f"""
    -------------------------------------------------------------------
    {title}:
    -------------------------------------------------------------------"""


def get_space() -> str:
    return f"""
    ---"""
