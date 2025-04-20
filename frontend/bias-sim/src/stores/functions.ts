import { writable } from 'svelte/store';

export const condition = writable(async (characteristic: string, value: number | null) => {});
export const deconditionAll = writable(async () => {});

export const loadProcess = writable(async (socket: WebSocket) => {});

export const invalidateNetwork = writable(async () => {});

export const invalidateBias = writable(async () => {});
