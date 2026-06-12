import * as d3 from 'd3';
import type { CharacteristicResponse, NetworkResponse } from './generated';

export type Characteristic = CharacteristicResponse;

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

// Network is the backend NetworkResponse with `graph` swapped from null to the
// client-side D3 Graph object (the backend omits graph; the client builds it).
export type Network = Omit<NetworkResponse, 'graph'> & { graph: Graph };
