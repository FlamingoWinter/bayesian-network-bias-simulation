import type { GroupPredictionInformationResponse, RecruiterBiasAnalysisResponse } from './generated';

export type MitigationAnalysis = RecruiterBiasAnalysisResponse;
export type RecruiterBiasAnalysis = Record<string, MitigationAnalysis>;
export type BiasAnalysis = Record<string, RecruiterBiasAnalysis>;

export type BiasLevel = 'Minimal' | 'Moderate' | 'High' | 'Very High';

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

/** Find the groups with the minimum and maximum value for a numeric field. */
export function minMaxGroups(
	byGroup: Record<string, GroupPredictionInformationResponse>,
	field: keyof GroupPredictionInformationResponse
): { min: string; max: string; minVal: number; maxVal: number } {
	return Object.entries(byGroup).reduce(
		(acc, [groupName, info]) => {
			const val = info[field] as number;
			if (val > acc.maxVal) { acc.max = groupName; acc.maxVal = val; }
			if (val < acc.minVal) { acc.min = groupName; acc.minVal = val; }
			return acc;
		},
		{ min: '', max: '', minVal: 1, maxVal: 0 }
	);
}

export const levelToColorMapping: Record<BiasLevel, string> = {
	Minimal: '#22bd28',
	Moderate: '#c3b223',
	High: '#ba832f',
	'Very High': '#bf4138'
};
