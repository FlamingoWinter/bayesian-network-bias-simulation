{#if mode !== "none"}
	<!-- svelte-ignore a11y-mouse-events-have-key-events -->
	<button type="button"
					class="absolute right-5 bottom-5 btn btn-xl text-2xl variant-filled py-4 px-4 rounded-full min-w-32 z-[5]"
					on:click={()=>{	modalStore.trigger(modal)}}>
		{#if loading}
			<ProgressRadial class="w-7" meter="stroke-primary-100" track="stroke-primary-100/30"
											strokeLinecap="butt" value={undefined} stroke={100} />
		{:else}
			{mode === "new_network" ? "New Network..." : mode === "name_network" ? "Label Network..." : "Run Simulation"}
			<CaretRightFill class="ml-2" width={20} height={20} />
		{/if}
	</button>
{/if}
<script lang="ts">

	import { CaretRightFill } from 'svelte-bootstrap-icons';
	import { getModalStore, ProgressRadial } from '@skeletonlabs/skeleton';
	import NewNetworkModal from './modals/new_network_modal/NewNetworkModal.svelte';
	import NameNetworkModal from './modals/name_network_modal/NameNetworkModal.svelte';
	import SimulateModal from './modals/simulate_modal/SimulateModal.svelte';
	import type { Network } from '../types/network';

	export let network: Network;
	let loading: boolean = false;
	let mode: 'new_network' | 'none' | 'name_network' | 'run_simulation' = 'new_network';

	$: if (network.characteristics) {
		mode = network.predefined ? 'new_network' :
			Object.keys(network.characteristics)[0] in ['0', '1', '2', '3'] ? 'name_network' :
				Object.keys(network.characteristics).some(a => a.includes('Characteristic')) ? 'run_simulation' :
					'none';
	}


	// The mode should be generating a new network. If the network is the predefined demo network.


	const modalStore = getModalStore();

	$: modalComponent = (mode == 'new_network' ? { ref: NewNetworkModal } :
		(mode == 'run_simulation') ? { ref: SimulateModal, props: { network: network } } :
			{ ref: NameNetworkModal });


	$: modal = {
		type: 'component',
		component: modalComponent,
		backdropClasses: 'bg-gradient-to-tr from-indigo-500/50 via-purple-500/50 to-pink-500/50'

	};
</script>