<script lang="ts">
	import GraphVisualisation from '../components/GraphVisualisation.svelte';
	import { onMount } from 'svelte';
	import type { Network } from '../types/network.js';
	import * as d3 from 'd3';
	import type { NodeDistribution } from '../types/nodeDistribution';

	let network: Network | undefined;

	let nodeDistributionByName: Record<string, NodeDistribution> = {};

	let initialised = false;

	let innerWidth = 0;
	let innerHeight = 0;

	$: width = innerWidth;
	$: height = innerHeight - 4;

	onMount(async () => {
		network = await d3.json('http://localhost:8000/');


		if (network) {
			await Promise.all(network.graph.nodes.map(async (node) => {
				nodeDistributionByName[node.id] = await d3.json(`http://localhost:8000/distribution-${node.id}`) as NodeDistribution;
			}));

		}
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

<button type="button" class="btn-icon variant-filled-surface">(icon)</button>
{#if initialised && network}
	<GraphVisualisation network={network} width={width} height={height} nodeDistributionByName={nodeDistributionByName} />
{/if}

