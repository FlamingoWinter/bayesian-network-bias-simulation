export function calculateDistributionFill(probabilityType: ProbabilityType) {
	switch (probabilityType) {
		case 'prior':
			return '#0d3b68';
		case 'conditioned':
			return '#C47335';
		case 'posterior':
			return '#000';
	}
}