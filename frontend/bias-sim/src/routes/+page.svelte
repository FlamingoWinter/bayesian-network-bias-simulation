<script lang="ts">
	import GraphVisualisation from '../components/GraphVisualisation.svelte';
	import { onMount } from 'svelte';
	import type { Graph } from '../types/network.js';
	import * as d3 from 'd3';

	let graph: Graph | undefined;
	let nodeDistributionByName: Record<string, string[]> = {};

	let initialised = false;

	let innerWidth = 0;
	let innerHeight = 0;

	$: width = innerWidth;
	$: height = innerHeight - 4;

	onMount(async () => {
		graph = await d3.json('http://localhost:8000/');


		if (graph) {
			await Promise.all(graph.nodes.map(async (node) => {
				nodeDistributionByName[node.id] = await d3.json(`http://localhost:8000/node-${node.id}`) as string[];
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


{#if initialised && graph}
	<GraphVisualisation graph={graph} width={width} height={height} nodeDistributionByName={nodeDistributionByName} />
{/if}
