<script lang="ts">
	import GraphVisualisation from '../components/GraphVisualisation.svelte';
	import { onMount } from 'svelte';
	import { network, sessionKey } from '../stores/store';
	import type { Network } from '../types/network';
	import { apiRequest, apiUrl } from '../utiliites/api';
	import ConditionLogic from '../components/ConditionLogic.svelte';
	import Menu from '../components/menu/Menu.svelte';
	import { deconditionAll, invalidateNetwork } from '../stores/functions';
	import * as d3 from 'd3';
	import NextButton from '../components/NextButton.svelte';

	let initialised = false;
	let innerWidth: number;
	let innerHeight: number;

	$: width = innerWidth;
	$: height = innerHeight - 4;

	onMount(async () => {
		$network = await apiRequest('') as Network;

		$invalidateNetwork = async () => {
			$network = await apiRequest('') as Network;
			$deconditionAll();
		};

		$sessionKey = (await d3.json(`${apiUrl}session/`, { credentials: 'include' }) as { key: string }).key;


		initialised = true;
	});
</script>


<style>
    :global(body) {
        margin: 0;
        padding: 0;
    }
</style>

<svelte:window bind:innerWidth bind:innerHeight />

<ConditionLogic />
{#if initialised}
	<GraphVisualisation width={width} height={height} />
{/if}
<Menu />
<NextButton />