import { writable, type Writable } from 'svelte/store';
import type { Network, Node } from '../types/network';
import * as d3 from 'd3';

export const conditioned = writable(false);

export const conditions: Writable<Record<string, number>> = writable({});

export const posteriorDistributions: Writable<Record<string, number[]>> = writable({});

export const expandedNodeId = writable('');

export const network: Writable<Network> = writable({} as Network);
export const simulation: Writable<d3.Simulation<Node, undefined>> = writable();
export const sessionKey: Writable<string> = writable();
