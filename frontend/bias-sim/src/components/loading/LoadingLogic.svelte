<script lang="ts">
	import Loading from './Loading.svelte';
	import { onMount } from 'svelte';
	import { loadProcess } from '../../stores/functions';
	import { getToastStore, type ToastSettings } from '@skeletonlabs/skeleton';

	const toastStore = getToastStore();

	let loadingText: string = 'Loading...';
	let isLoading: boolean = false;

	onMount(() => {
		$loadProcess = (socket: WebSocket): Promise<void> => {
			return new Promise((resolve) => {
				isLoading = true;

				socket.onmessage = (event) => {
					const statusText = JSON.parse(event.data).message;

					const t: ToastSettings = {
						message: `${statusText}`,
						timeout: 2500,
						background: 'variant-filled-primary'
					};
					toastStore.trigger(t);
				};

				const resolve_promise = () => {
					isLoading = false;
					resolve();
				};

				socket.onclose = resolve_promise;
				socket.onerror = () => {
					const t: ToastSettings = {
						message: 'Encountered an error in websocket.',
						timeout: 3000,
						background: 'variant-filled-error'
					};
					toastStore.trigger(t);
					resolve_promise();
				};
			});
		};

	});
</script>

<Loading isLoading={isLoading} loadingText={loadingText} />