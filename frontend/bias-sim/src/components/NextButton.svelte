<script lang="ts">
	import { CaretRightFill } from 'svelte-bootstrap-icons';
	import { getModalStore, type ModalSettings, ProgressRadial } from '@skeletonlabs/skeleton';
	import NewNetworkModal from './modals/new_network_modal/NewNetworkModal.svelte';
	import NameNetworkModal from './modals/name_network_modal/NameNetworkModal.svelte';
	import SimulateModal from './modals/simulate_modal/SimulateModal.svelte';
	import type { Network } from '../types/network';

	export let network: Network;
	let loading: boolean = false;
	let mode: 'new_network' | 'none' | 'name_network' | 'run_simulation' = 'new_network';

	$: if (network.characteristics) {
		const firstKey = Object.keys(network.characteristics)[0];
		mode = network.predefined
			? 'new_network'
			: /^\d+$/.test(firstKey)
				? 'name_network'
				: 'run_simulation';
	}

	// The mode should be generating a new network. If the network is the predefined demo network.

	const modalStore = getModalStore();

	$: modalComponent =
		mode === 'new_network'
			? { ref: NewNetworkModal }
			: mode === 'run_simulation'
				? { ref: SimulateModal, props: { network: network } }
				: { ref: NameNetworkModal };

	let modal: ModalSettings;
	$: modal = {
		type: 'component',
		component: modalComponent,
		backdropClasses: 'bg-gradient-to-tr from-indigo-500/50 via-purple-500/50 to-pink-500/50'
	};
</script>

{#if mode !== 'none'}
	<!-- svelte-ignore a11y-mouse-events-have-key-events -->
	<button
		type="button"
		class="variant-filled btn btn-xl absolute bottom-5 right-5 z-[5] min-w-32 rounded-full px-4 py-4 text-2xl"
		on:click={() => {
			modalStore.trigger(modal);
		}}
	>
		{#if loading}
			<ProgressRadial
				class="w-7"
				meter="stroke-primary-100"
				track="stroke-primary-100/30"
				strokeLinecap="butt"
				value={undefined}
				stroke={100}
			/>
		{:else}
			{mode === 'new_network'
				? 'New Network...'
				: mode === 'name_network'
					? 'Label Network...'
					: 'Run Simulation'}
			<CaretRightFill class="ml-2" width={20} height={20} />
		{/if}
	</button>
{/if}
