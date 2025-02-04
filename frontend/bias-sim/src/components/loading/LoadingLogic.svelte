<script lang="ts">
	import Loading from './Loading.svelte';
	import { onMount } from 'svelte';
	import { loadProcess } from '../../stores/functions';
	import { getToastStore, type ToastSettings } from '@skeletonlabs/skeleton';

	const toastStore = getToastStore();

	let loadingText: string;
	let isLoading: boolean = false;

	onMount(() => {
		$loadProcess = async (socket: WebSocket) => {
			isLoading = true;

			socket.onmessage = (event) => {
				const statusText = JSON.parse(event.data).message;

				const t: ToastSettings = {
					message: `${statusText}`,
					timeout: 5000,
					background: 'variant-filled-primary'
				};
				toastStore.trigger(t);
			};

			socket.onclose = () => {
				isLoading = false;
			};

			socket.onerror = () => {
				const t: ToastSettings = {
					message: 'Encountered an error in websocket.',
					timeout: 3000,
					background: 'variant-filled-error'
				};
				toastStore.trigger(t);


				isLoading = false;
			};

		};
	});
</script>

<Loading isLoading={isLoading} loadingText={loadingText} />