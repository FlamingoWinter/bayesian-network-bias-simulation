import { writable } from 'svelte/store';

export const openDescribeDialog = writable(async (expandedNode: string) => {
});
export const openConditionDialog = writable(async (expandedNode: string) => {
});
export const exitDialog = writable(() => {
});
export const condition = writable(async (characteristic: string, value: number) => {
});