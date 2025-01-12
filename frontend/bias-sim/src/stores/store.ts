import { writable, type Writable } from 'svelte/store';
import type { Network } from '../types/network';
import type { NodeDistribution } from '../types/nodeDistribution';

export const describeNode = writable(async (expandedNode: string) => {
});
export const conditionNode = writable(async (expandedNode: string) => {
});
export const cancelDescribe = writable(() => {
});

export const expandedNodeId = writable('');

export const network: Writable<Network> = writable({} as Network);
export const distributionById: Writable<Record<string, NodeDistribution>> = writable({});

