const fillByType: Record<ProbabilityType, string> = {
	prior: '#0d3b68',
	conditioned: '#494660',
	posterior: '#bf8b00'
};

export function calculateDistributionFill(probabilityType: ProbabilityType) {
	return fillByType[probabilityType];
}
