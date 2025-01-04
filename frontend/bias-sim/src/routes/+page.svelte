<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<!--Adapted from https://gist.github.com/mbostock/2675ff61ea5e063ede2b5d63c08020c7 -->

<script lang="ts">
	import { onMount } from 'svelte';
	import type { D3DragEvent } from 'd3';
	import * as d3 from 'd3';
	import type { Graph, Link, Node } from '../types/network';

	let svg: SVGElement;
	const width = 600;
	const height = 500;

	onMount(async () => {
		const svgElement = d3.select(svg)
			.attr('width', width)
			.attr('height', height);

		const graph: Graph | undefined = await d3.json('http://localhost:8000/');

		if (graph) {
			renderGraph(graph, svgElement);
			console.log(graph);
		}
	});

	function renderGraph(graph: Graph, svgElement: d3.Selection<SVGElement, unknown, null, undefined>) {

		const simulation = d3.forceSimulation(graph.nodes)
			.force('link', d3.forceLink(graph.links).id((d: any) => d.id).distance(100))
			.force('charge', d3.forceManyBody().strength(-200))
			.force('center', d3.forceCenter(width / 2, height / 2));

		const link = svgElement.append('g')
			.selectAll('.link')
			.data(graph.links)
			.enter().append('line')
			.attr('class', 'link')
			.attr('stroke', '#aaa');

		const node = svgElement.append('g')
			.selectAll('.node')
			.data(graph.nodes)
			.enter().append('g')
			.attr('class', 'node');

		const arrowHead = svgElement.append('defs').selectAll('marker')
			.data(['arrowhead'])
			.enter().append('marker')
			.attr('id', 'arrowhead')
			.attr('viewBox', '0 -5 10 10')
			.attr('refX', 20)
			.attr('refY', 0)
			.attr('markerWidth', 20)
			.attr('markerHeight', 20)
			.attr('orient', 'auto')
			.append('path')
			.attr('d', 'M0,-5L10,0L0,5')
			.attr('fill', '#aaa');

		link.attr('marker-end', 'url(#arrowhead)');


		const rectWidth = 100;
		const rectHeight = 80;
		node.append('svg:rect')
			.attr('rx', 6)
			.attr('ry', 6)
			.attr('width', rectWidth)
			.attr('height', rectHeight)
			.attr('fill', '#ffffff')
			.attr('stroke', '#333333')
			.attr('stroke-width', 2)
			.attr('x', -rectWidth / 2)
			.attr('y', -rectHeight / 2);


		node.append('foreignObject')
			.attr('width', rectWidth)
			.attr('height', rectHeight)
			.attr('x', -rectWidth / 2)
			.attr('y', -rectHeight / 2)
			.append('xhtml:body')
			.style('font', '14px \'Helvetica Neue\'')
			.style('text-align', 'center')
			.html((d: Node) => `<p>${d.label}</p>`);

		node
			.call(d3.drag<SVGGElement, Node>()
				.on('start', dragstarted)
				.on('drag', dragged)
				.on('end', dragended));


		simulation
			.nodes(graph.nodes)
			.on('tick', () => {
				link
					.attr('x1', (d: Link) => (d.source as Node).x!)
					.attr('y1', (d: Link) => (d.source as Node).y!)
					.attr('x2', (d: Link) => (d.target as Node).x!)
					.attr('y2', (d: Link) => (d.target as Node).y!);

				node
					.attr('transform', d => `translate(${d.x},${d.y})`);
			});

		function dragstarted(event: D3DragEvent<SVGRectElement, Node, Node>, d: Node) {
			if (!event.active) simulation.alphaTarget(0.3).restart();
			d.fx = d.x;
			d.fy = d.y;
		}

		function dragged(event: D3DragEvent<SVGRectElement, Node, Node>, d: Node) {
			d.fx = event.x;
			d.fy = event.y;
		}

		function dragended(event: D3DragEvent<SVGRectElement, Node, Node>, d: Node) {
			if (!event.active) simulation.alphaTarget(0);
			d.fx = null;
			d.fy = null;
		}
	}

</script>

<svg bind:this={svg}></svg>
