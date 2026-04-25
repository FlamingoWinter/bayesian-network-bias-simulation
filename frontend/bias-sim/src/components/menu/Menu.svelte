<script lang="ts">
	import List from 'svelte-bootstrap-icons/lib/List.svelte';
	import { fly } from 'svelte/transition';
	import MenuButton from './MenuButton.svelte';
	import { conditioned } from '../../stores/store';
	import { deconditionAll } from '../../stores/functions';
	import { onMount } from 'svelte';
	import OpenModalMenuButton from '../modals/OpenModalMenuButton.svelte';
	import NewNetworkModal from '../modals/new_network_modal/NewNetworkModal.svelte';
	import NameNetworkModal from '../modals/name_network_modal/NameNetworkModal.svelte';
	import SimulateModal from '../modals/simulate_modal/SimulateModal.svelte';
	import ShowBiasModal from '../modals/show_bias_modal/ShowBiasModal.svelte';
	import type { Network } from '../../types/network';

	export let network: Network;

	let isHovered: boolean = false;
	let isOpen = false;

	const handleClickOutside = (event: MouseEvent) => {
		if (!isHovered && isOpen) {
			isOpen = false;
		}
	};

	onMount(() => {
		document.addEventListener('click', handleClickOutside);
		return () => {
			document.removeEventListener('click', handleClickOutside);
		};
	});
</script>

<div class="absolute bottom-0 left-0">
	<!-- svelte-ignore a11y-mouse-events-have-key-events -->
	<button
		class="card bg-surface-50-900-token btn absolute bottom-5 left-5 rounded-lg p-2 drop-shadow-md"
		on:click={() => {
			isOpen = !isOpen;
		}}
		on:mouseover={() => {
			isHovered = true;
		}}
		on:mouseleave={() => {
			isHovered = false;
		}}
	>
		<List width="28" height="28" />
	</button>

	{#if isOpen}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
		<!-- svelte-ignore a11y-mouse-events-have-key-events -->
		<div
			transition:fly={{ y: 50, duration: 400 }}
			on:click|stopPropagation
			role="alertdialog"
			on:mouseover={() => {
				isHovered = true;
			}}
			on:mouseleave={() => {
				isHovered = false;
			}}
			class="card bg-surface-50-900-token absolute bottom-20 left-4 flex min-h-80 w-52 flex-col items-center justify-start gap-2 rounded-lg p-4 drop-shadow-md"
		>
			<OpenModalMenuButton
				component={{ ref: SimulateModal, props: { network: network } }}
				classList="bg-primary-900"
				>Run Simulation...
			</OpenModalMenuButton>
			<OpenModalMenuButton component={{ ref: ShowBiasModal }} classList="bg-primary-700"
				>Show Bias...
			</OpenModalMenuButton>

			<OpenModalMenuButton component={{ ref: NewNetworkModal }} classList="bg-primary-900"
				>New Network...
			</OpenModalMenuButton>
			<OpenModalMenuButton component={{ ref: NameNetworkModal }} classList="bg-primary-700"
				>Name Network...
			</OpenModalMenuButton>

			{#if $conditioned}
				<MenuButton callback={$deconditionAll}>Decondition all</MenuButton>
			{/if}
		</div>
	{/if}
</div>
