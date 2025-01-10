import { writable, type Writable } from 'svelte/store';
import type { Network } from '../types/network';
import type { NodeDistribution } from '../types/nodeDistribution';

export const describeNode = writable((expandedNode: string) => {
});
export const cancelDescribe = writable(() => {
});

export const expandedNode = writable('');

export const network: Writable<Network | undefined> = writable(undefined);
export const nodeDistributionByName: Writable<Record<string, NodeDistribution>> = writable({});

