import { writable, type Writable } from 'svelte/store';
import type { Network, Node } from '../types/network';
import * as d3 from 'd3';

export const describeNode = writable(async (expandedNode: string) => {
});
export const conditionNode = writable(async (expandedNode: string) => {
});
export const cancelDescribe = writable(() => {
});

export const expandedNodeId = writable('');

export const network: Writable<Network> = writable({} as Network);
export const simulation: Writable<d3.Simulation<Node, undefined>> = writable();

