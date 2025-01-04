<!--Adapted from https://gist.github.com/mbostock/2675ff61ea5e063ede2b5d63c08020c7 -->
<script lang="ts">
	import { onMount } from 'svelte';
	import type { D3DragEvent } from 'd3';
	import * as d3 from 'd3';
	import type { Graph, Link, Node } from '../types/network';

	let svg: SVGElement;
	let svgElement: d3.Selection<SVGElement, unknown, null, undefined>;
	let innerWidth = 0;
	let innerHeight = 0;

	$: width = innerWidth;
	$: height = innerHeight - 4;

	onMount(async () => {
		svgElement = d3.select(svg)
			.attr('width', innerWidth)
			.attr('height', innerHeight);

		const graph: Graph | undefined = await d3.json('http://localhost:8000/');

		if (graph) {
			renderGraph(graph, svgElement);
		}
	});

	$: if (svgElement) {
		svgElement
			.attr('width', width)
			.attr('height', height);
	}

	function renderGraph(graph: Graph, svgElement: d3.Selection<SVGElement, unknown, null, undefined>) {

		const simulation = d3.forceSimulation(graph.nodes)
			.force('link', d3.forceLink(graph.links).id((d: any) => d.id).distance(150).strength(0.25))
			.force('charge', d3.forceManyBody().strength(-400))
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

		const markers = svgElement.append('defs').selectAll('marker')
			.data(graph.links)
			.enter().append('marker')
			.attr('id', d => `arrowhead-${d.index}`)
			.attr('viewBox', '0 -5 10 10')
			.attr('refY', 0)
			.attr('markerWidth', 20)
			.attr('markerHeight', 20)
			.attr('orient', 'auto');


		markers.append('path')
			.attr('d', 'M0,-5L10,0L0,5')
			.attr('fill', '#aaa');

		link.attr('marker-start', d => `url(#arrowhead-${d.index})`);


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
			.style('padding', '10px')
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


				markers
					.attr('refX', d => {
						const x1 = (d.source as Node).x!;
						const y1 = (d.source as Node).y!;
						const x2 = (d.target as Node).x!;
						const y2 = (d.target as Node).y!;


						return -Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2)) / 4;
					});


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

<style>
    :global(body) {
        margin: 0;
        padding: 0;
    }
</style>

<svelte:window bind:innerWidth bind:innerHeight />

<svg bind:this={svg}></svg>

