export function calculateDistributionFill(probabilityType: ProbabilityType) {
	switch (probabilityType) {
		case 'prior':
			return '#0d3b68';
		case 'conditioned':
			return '#000';
		case 'posterior':
			return '#C47335';
	}
}