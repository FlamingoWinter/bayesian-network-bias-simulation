<script lang="ts">
	import GraphVisualisation from '../components/GraphVisualisation.svelte';
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import type { NodeDistribution } from '../types/nodeDistribution';
	import { network, nodeDistributionByName } from '../stores/store';

	let expandedNodeName: string;

	let fetchedNodeDistributionByName: Record<string, NodeDistribution> = {};

	let initialised = false;

	let innerWidth = 0;
	let innerHeight = 0;

	$: width = innerWidth;
	$: height = innerHeight - 4;

	onMount(async () => {
		$network = await d3.json('http://localhost:8000/');


		if ($network) {
			await Promise.all($network.graph.nodes.map(async (node) => {
				fetchedNodeDistributionByName[node.id] = await d3.json(`http://localhost:8000/distribution-${node.id}`) as NodeDistribution;
			}));

		}

		$nodeDistributionByName = fetchedNodeDistributionByName;
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


{#if initialised && network}
	<GraphVisualisation width={width} height={height} />
{/if}

