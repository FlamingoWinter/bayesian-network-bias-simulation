<script lang="ts">
	import SimulateModal from '../modals/simulate_modal/SimulateModal.svelte';
	import ShowBiasModal from '../modals/show_bias_modal/ShowBiasModal.svelte';
	import NewNetworkModal from '../modals/new_network_modal/NewNetworkModal.svelte';
	import NameNetworkModal from '../modals/name_network_modal/NameNetworkModal.svelte';
	import { biasAnalysis, conditioned } from '../../stores/store';
	import { deconditionAll } from '../../stores/functions';
	import BottomHrefButtons from './BottomHrefButtons.svelte';
	import TopUtilityButtons from './TopUtilityButtons.svelte';

	import { getDrawerStore, getModalStore, type ModalSettings } from '@skeletonlabs/skeleton';
	import type { Network } from '../../types/network';

	const modalStore = getModalStore();
	export let network: Network;
	const drawerStore = getDrawerStore();

	let modal: ModalSettings = {
		type: 'component',
		backdropClasses: 'bg-gradient-to-tr from-indigo-500/50 via-purple-500/50 to-pink-500/50'
	};


	function openModal(ModalComponent: any) {
		modal.component = { ref: ModalComponent };
		modalStore.trigger(modal);
		drawerStore.close();
	}

	let showBias: boolean = false;

	$: if (network.characteristics) {
		showBias = ($biasAnalysis !== undefined);
	}
</script>
<div class="pt-14 flex flex-col justify-between items-start  h-full">
	<div class="flex flex-col justify-start items-start w-full pr-8 gap-2">
		<TopUtilityButtons utilityButtonInfos={[
			{name: "New Network", callback: () => openModal(NewNetworkModal)},
			{name: "Label Network", callback: () => openModal(NameNetworkModal)},
			{name: "Run Simulation", callback: () => openModal(SimulateModal)},
			...(showBias ? [{name: "Show Bias", callback: () => openModal(ShowBiasModal)}] : []),
			...($conditioned ? [{name: "Decondition All", callback: $deconditionAll}] : []),
		]} />
	</div>
	<BottomHrefButtons buttonInfos={[
			{name: "Walkthrough", slug: "/walkthrough"},
			{name: "Guide", slug: "/guide"},
		]} />
</div>
