interface CategoricalGroupPredictionInformation {
	total: number;
	hiredAndCompetent: number;
	hiredButNotCompetent: number;
	notHiredButCompetent: number;
	notHiredAndNotCompetent: number;

	hired: number;
	hiredRate: number;
	notHired: number;
	notHiredRate: number;
	correct: number;
	correctRate: number;
	incorrect: number;
	incorrectRate: number;
	competent: number;
	competentRate: number;
	notCompetent: number;
	notCompetentRate: number;

	accuracy: number;
	falseNegativeRate: number;
	falsePositiveRate: number;
	falseDiscoveryRate: number;
	falseOmissionRate: number;
}


export interface CategoricalRecruiterBiasAnalysis {
	general: CategoricalGroupPredictionInformation;
	byGroup: Record<string, CategoricalGroupPredictionInformation>;
}

interface ContinuousRecruiterBiasAnalysis {

}

interface RecruiterBiasAnalysis {
	categoricalBiasAnalysis: CategoricalRecruiterBiasAnalysis,
	continuousBiasAnalysis: ContinuousRecruiterBiasAnalysis
}

export type BiasAnalysis = Record<string, RecruiterBiasAnalysis>

export type BiasLevel = 'Minimal' | 'Moderate' | 'High' | 'Very High'

export function multiplierToLevel(multiplier: number): BiasLevel {
	if (multiplier > 1) {
		if (multiplier < 1.02) return 'Minimal';
		if (multiplier < 1.1) return 'Moderate';
		if (multiplier < 1.25) return 'High';
		return 'Very High';
	}
	if (multiplier > 1 / 1.02) return 'Minimal';
	if (multiplier > 1 / 1.1) return 'Moderate';
	if (multiplier > 1 / 1.25) return 'High';
	return 'Very High';
}

export function absoluteDisparityToLevel(absoluteDisparity: number): BiasLevel {
	if (absoluteDisparity < 0.02) return 'Minimal';
	if (absoluteDisparity < 0.1) return 'Moderate';
	if (absoluteDisparity < 0.25) return 'High';
	return 'Very High';
}


export const levelToColorMapping: Record<BiasLevel, string> = {
	'Minimal': '#22bd28',
	'Moderate': '#c3b223',
	'High': '#ba832f',
	'Very High': '#bf4138'
};