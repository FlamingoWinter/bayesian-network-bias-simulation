<script lang="ts">
	import GraphVisualisation from '../components/GraphVisualisation.svelte';
	import { onMount } from 'svelte';
	import type { Graph } from '../types/network.js';
	import * as d3 from 'd3';
	import type { NodeInformation } from '../types/nodeInformation';

	let graph: Graph | undefined;

	let nodeInformationByName: Record<string, NodeInformation> = {};

	let initialised = false;

	let innerWidth = 0;
	let innerHeight = 0;

	$: width = innerWidth;
	$: height = innerHeight - 4;

	onMount(async () => {
		graph = await d3.json('http://localhost:8000/');


		if (graph) {
			await Promise.all(graph.nodes.map(async (node) => {
				nodeInformationByName[node.id] = await d3.json(`http://localhost:8000/node-${node.id}`) as NodeInformation;
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
	<GraphVisualisation graph={graph} width={width} height={height} nodeInformationByName={nodeInformationByName} />
{/if}
