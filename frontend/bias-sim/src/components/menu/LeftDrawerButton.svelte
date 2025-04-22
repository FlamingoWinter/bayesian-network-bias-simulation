<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<button type="button"
				class="fixed -left-2 -top-2 btn text-2xl
				variant-filled  min-h-[4rem] rounded-none rounded-br-xl z-50 transition-all
				duration-300
				{$drawerStore.open ? 'w-[20rem]' : 'w-[4rem]'}"
				on:click={toggleDrawer}>
	<List width="28" height="28" />
</button>

<script lang="ts">

	import { type DrawerSettings, getDrawerStore } from '@skeletonlabs/skeleton';
	import { List } from 'svelte-bootstrap-icons';
	import { onMount } from 'svelte';
	import type { Network } from '../../types/network';

	export let network: Network | undefined = undefined;
	const drawerStore = getDrawerStore();

	onMount(() => {
		const path: string = window.location.pathname;
		drawerSettings.id = (path.includes('visualisation')) ? 'visualisation' : 'walkthrough';
		drawerSettings.meta = { network: network };
	});

	const drawerSettings: DrawerSettings = {
		bgDrawer: 'bg-black',
		bgBackdrop: 'bg-gradient-to-tr from-indigo-500/30 via-purple-500/30 to-pink-500/30',
		width: 'w-[20rem]',
		rounded: 'rounded-none'
	};


	function toggleDrawer() {
		if (!$drawerStore.open) {
			drawerStore.open(drawerSettings);
		} else {
			drawerStore.close();
		}
	}

</script>