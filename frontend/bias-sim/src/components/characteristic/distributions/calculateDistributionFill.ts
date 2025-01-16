export function calculateDistributionFill(probabilityType: ProbabilityType) {
	switch (probabilityType) {
		case 'prior':
			return '#0d3b68';
		case 'conditioned':
			return '#d1d1d1';
		case 'posterior':
			return '#bf8b00';
	}
}