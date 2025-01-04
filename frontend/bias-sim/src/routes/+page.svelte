<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<svg id="graph" width="600px" height="400px" />

<!--Adapted from https://gist.github.com/mbostock/2675ff61ea5e063ede2b5d63c08020c7 -->

<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import type { Graph, Node } from '../types/network';

	onMount(async () => {
		const graph: Graph | undefined = await d3.json('http://localhost:8000/');
		if (graph) {
			buildSimulation(graph);
		}
		console.log(graph);
	});


	function buildSimulation(graph: Graph) {
		const svg = d3.select('#graph'),
			width = +svg.attr('width'),
			height = +svg.attr('height');


		const nodeElements: d3.Selection<SVGCircleElement, Node, SVGGElement, unknown> = svg.append('g')
			.attr('class', 'nodes')
			.selectAll('circle')
			.data(graph.nodes)
			.enter().append('circle')
			.attr('r', 5);
		// .call(d3.drag<SVGCircleElement, Node>();
		// .on('start', dragstarted)
		// .on('drag', dragged)
		// .on('end', dragended));

		const link = svg.append('g')
			.attr('class', 'links')
			.selectAll('line')
			.data(graph.links)
			.enter().append('line')
			.attr('stroke-width', d => Math.sqrt(d.value || 1));

		const simulation = d3.forceSimulation()
			.force('link', d3.forceLink().id(d => d.index!))
			.force('charge', d3.forceManyBody())
			.force('center', d3.forceCenter(width / 2, height / 2));


	}


</script>
