<script lang="ts">
	import GraphVisualisation from '../components/GraphVisualisation.svelte';
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import { condition, conditioned, conditions, network } from '../stores/store';
	import type { Network } from '../types/network';
	import { apiRequest, apiUrl } from '../utiliites/api';

	let initialised = false;
	let innerWidth: number;
	let innerHeight: number;

	$: width = innerWidth;
	$: height = innerHeight - 4;

	onMount(async () => {
		$network = await d3.json(apiUrl) as Network;

		initialised = true;

		$condition = async (characteristic: string, value: number) => {
			$conditions[characteristic] = value;

			console.log($conditions);

			const conditionResponse = await apiRequest('condition/', 'POST', JSON.stringify($conditions)) as Record<string, number[]>;

			$conditioned = true;

			for (const [characteristic, posteriorDistribution] of Object.entries(conditionResponse)) {
				// $network.characteristics[characteristic].posteriorDistribution = posteriorDistribution;
			}
		};
	});
</script>


<style>
    :global(body) {
        margin: 0;
        padding: 0;
    }
</style>

<svelte:window bind:innerWidth bind:innerHeight />


{#if initialised}
	<GraphVisualisation width={width} height={height} />
{/if}

