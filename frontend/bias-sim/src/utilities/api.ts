import * as d3 from 'd3';

export const apiUrl = 'https://api.modelling-bias.com/';
export const webSocketUrl = 'wss://api.modelling-bias.com/ws';

export async function apiRequest(
	url: string,
	method: 'GET' | 'POST' = 'GET',
	body: any = undefined
) {
	const headers: any = {
		'Content-Type': 'application/json'
	};
	if (method == 'POST') {
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
