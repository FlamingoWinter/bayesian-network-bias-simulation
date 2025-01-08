<!--Adapted from https://gist.github.com/mbostock/2675ff61ea5e063ede2b5d63c08020c7 -->


<svg bind:this={svg} width={width} height={height} />


<script lang="ts">
	import * as d3 from 'd3';
	import type { Graph, Node } from '../types/network';
	import { onMount } from 'svelte';
	import { renderGraph } from '../d3/renderGraph';
	import type { NodeDistribution } from '../types/nodeDistribution';

	export let graph: Graph;
	export let width: number;
	export let height: number;
	export let nodeDistributionByName: Record<string, NodeDistribution>;

	let svg: SVGElement;
	let svgElement: d3.Selection<SVGElement, unknown, null, undefined>;
	let simulation: d3.Simulation<Node, undefined>;

	onMount(async () => {
		svgElement = d3.select(svg);

		const zoomGroup = svgElement.append('g')
			.attr('class', 'zoom-group');

		svgElement.call(d3.zoom<SVGElement, unknown>()
			.scaleExtent([0.5, 5])
			.on('zoom', (event) => {
				zoomGroup.attr('transform', event.transform);
			}));


		if (graph) {
			simulation = renderGraph(graph, nodeDistributionByName, zoomGroup, width, height);
		}
	});


	$: {
		if (simulation) {
			simulation.force('center', d3.forceCenter(width / 2, height / 2));
			simulation.alpha(1).restart();
		}
	}


</script>


