import * as d3 from 'd3';

export const apiUrl = 'http://localhost:8000/';

export async function apiRequest(url: string, method: 'GET' | 'POST' = 'GET', body: any) {
	const headers: any = {
		'Content-Type': 'application/json'
	};
	if (method == 'POST') {
		headers['X-CSRFToken'] = (await d3.json(`${apiUrl}csrf/`, { credentials: 'include' }) as { token: string }).token;
	}
	return await d3.json(`${apiUrl}${url}`, {
		method: method,
		body: body,
		headers: headers,
		credentials: 'include'
	});
}