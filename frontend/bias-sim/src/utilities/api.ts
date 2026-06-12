import * as d3 from 'd3';

const defaultApiUrl = 'http://localhost:8000/';
const defaultWsUrl = 'ws://localhost:8000/ws';

export const apiUrl = import.meta.env.VITE_API_URL ?? defaultApiUrl;
export const webSocketUrl = import.meta.env.VITE_WS_URL ?? defaultWsUrl;

export async function apiRequest(
	url: string,
	method: 'GET' | 'POST' = 'GET',
	body: string | undefined = undefined
) {
	const headers: Record<string, string> = {
		'Content-Type': 'application/json'
	};
	if (method === 'POST') {
		headers['X-CSRFToken'] = (
			(await d3.json(`${apiUrl}csrf/`, { credentials: 'include' })) as { token: string }
		).token;
	}
	return await d3.json(`${apiUrl}${url}`, {
		method: method,
		body: body,
		headers: headers,
		credentials: 'include'
	});
}
