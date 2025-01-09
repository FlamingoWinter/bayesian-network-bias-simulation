export interface NodeDistribution {
	distribution: number[];
	distributionType: 'categorical' | 'discrete' | 'continuous';
	categoriesForCategoricalDistributions: string[] | null;

}