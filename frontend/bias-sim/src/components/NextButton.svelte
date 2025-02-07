<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<button type="button"
				class="absolute right-5 bottom-5 btn btn-xl text-2xl variant-filled py-4 px-4 rounded-full min-w-32"
				on:click={()=>{	modalStore.trigger(modal)}}>
	{#if loading}
		<ProgressRadial class="w-7" meter="stroke-primary-100" track="stroke-primary-100/30"
										strokeLinecap="butt" value={undefined} stroke={100} />
	{:else}
		New Network...
		<CaretRightFill class="ml-2" width={20} height={20} />
	{/if}
</button>

<script lang="ts">

	import { CaretRightFill } from 'svelte-bootstrap-icons';
	import { getModalStore, type ModalComponent, type ModalSettings, ProgressRadial } from '@skeletonlabs/skeleton';
	import NewNetworkModal from './modals/new_network_modal/NewNetworkModal.svelte';

	let loading: boolean = false;
	let mode: 'newNetwork' | 'nameNetwork';

	// The mode should be generating a new network. If the network is the predefined demo network.


	const modalStore = getModalStore();

	const modalComponent: ModalComponent = { ref: NewNetworkModal };

	const modal: ModalSettings = {
		type: 'component',
		component: modalComponent
	};
</script>