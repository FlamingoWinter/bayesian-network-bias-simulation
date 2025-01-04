import * as d3 from 'd3';

export interface Node extends d3.SimulationNodeDatum {
	id: number;
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


