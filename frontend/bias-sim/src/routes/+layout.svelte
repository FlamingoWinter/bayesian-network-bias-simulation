<script>
	import '../app.css';
	import { afterNavigate } from '$app/navigation';
	import {
		Drawer,
		getDrawerStore,
		initializeStores,
		Modal,
		storePopup,
		Toast
	} from '@skeletonlabs/skeleton';
	import { arrow, autoUpdate, computePosition, flip, offset, shift } from '@floating-ui/dom';
	import Popups from '../components/popups/Popups.svelte';
	import LoadingLogic from '../components/loading/LoadingLogic.svelte';
	import LeftDrawerVisualisation from '../components/menu/LeftDrawerVisualisation.svelte';
	import LeftDrawerWalkthrough from '../components/menu/LeftDrawerWalkthrough.svelte';

	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

	initializeStores();
	const drawerStore = getDrawerStore();

	// GoatCounter counts the initial load itself; count in-app navigations here.
	afterNavigate((navigation) => {
		if (navigation.type === 'enter') return;
		// @ts-expect-error injected by the GoatCounter script
		window.goatcounter?.count?.({ path: location.pathname + location.search });
	});
</script>

<Toast />
<Modal transitionInParams={{ duration: 400 }} transitionOutParams={{ duration: 400 }} />
<LoadingLogic />

<Popups />
<Drawer>
	{#if $drawerStore.id === 'visualisation'}
		<LeftDrawerVisualisation network={$drawerStore.meta.network} />
	{:else if $drawerStore.id === 'walkthrough'}
		<LeftDrawerWalkthrough />
	{/if}
</Drawer>

<slot />

<style>
	:global(body) {
		margin: 0;
		padding: 0;
	}
</style>
