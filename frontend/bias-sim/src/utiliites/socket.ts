export const awaitSocketOpen = (socket: WebSocket) => {
	return new Promise<WebSocket>((resolve, reject) => {
		socket.onopen = () => {
			resolve(socket);
		};
		socket.onerror = (error) => {
			reject(error);
		};
	});
};

export const awaitSocketClose = (socket: WebSocket | undefined) => {
	if (socket && socket.readyState !== WebSocket.CLOSED) {
		socket.close();
	} else {
		return Promise.resolve(socket);
	}
	return new Promise<WebSocket>((resolve, reject) => {
		socket.onclose = () => {
			resolve(socket);
		};
		socket.onerror = (error) => {
			reject(error);
		};
	});
};