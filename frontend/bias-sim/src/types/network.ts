import * as d3 from 'd3';

export interface Node extends d3.SimulationNodeDatum {
	id: string;
	label: string;
	name?: string;
}

export interface Link extends d3.SimulationLinkDatum<d3.SimulationNodeDatum> {
	value?: number;
}

export interface Graph {
	nodes: Node[];
	links: Link[];
}

export interface Network {
	graph: Graph;
	scoreCharacteristic: string;
	applicationCharacteristics: string[];
	characteristics: Record<string, Characteristic>;
	predefined: boolean;
}

export interface Characteristic {
	name: string;
	type: 'continuous' | 'discrete' | 'categorical';
	categoryNames: string[];
	priorDistribution: number[];
}
