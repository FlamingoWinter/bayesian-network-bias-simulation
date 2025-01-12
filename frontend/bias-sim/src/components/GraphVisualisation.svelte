<svg bind:this={svg} width={width} height={height}
		 class="font-roboto font-normal">
	<g bind:this={zoomGroup}>
		<g bind:this={linkGroup}>
			{#each $network.graph.links as link}
				<line class="link" stroke="#aaa"
							marker-start={`url(#arrowhead-${link.index})`} />
			{/each}
		</g>
		<g bind:this={nodeGroup}>
			{#each $network.graph.nodes as node}
				<g class="node">
					<Chart node={node} />
				</g>
			{/each}
		</g>
		<defs bind:this={markerGroup}>
			{#each $network.graph.links as link}
				<marker id={`arrowhead-${link.index}`}
								viewBox="0 -5 10 10"
								refY="0"
								markerWidth="15" markerHeight="15" orient="auto"
								class="marker">
					<path d="M0,-5L10,0L0,5" fill="#aaa" />
				</marker>
			{/each}
		</defs>
	</g>
</svg>

<InfoBox />

<script lang="ts">
	import type { D3DragEvent } from 'd3';
	import * as d3 from 'd3';
	import type { Graph, Link, Node } from '../types/network';
	import { onMount } from 'svelte';

	import { network } from '../stores/store';
	import InfoBox from './InfoBox.svelte';
	import Chart from './Chart.svelte';

	export let width: number;
	export let height: number;

	let svg: SVGElement;
	let svgElement: d3.Selection<SVGElement, unknown, null, undefined>;
	let simulation: d3.Simulation<Node, undefined>;

	let zoomGroup: SVGGElement;
	let linkGroup: SVGGElement;
	let nodeGroup: SVGGElement;
	let markerGroup: SVGDefsElement;


	onMount(async () => {
		applyZoom(svg, zoomGroup);
		simulation = applyForceSimulation($network.graph, nodeGroup, linkGroup, markerGroup);

	});


	$: {
		if (simulation) {
			simulation.force('center', d3.forceCenter(width / 2, height / 2));
			simulation.alpha(1).restart();
		}
	}

	function applyZoom(svg: SVGElement, zoomGroup: SVGGElement) {
		d3.select(svg).call(d3.zoom<SVGElement, unknown>()
			.scaleExtent([0.5, 5])
			.on('zoom', (event) => {
				d3.select(zoomGroup).attr('transform', event.transform);
			}));
	}

	function applyForceSimulation(graph: Graph, nodeGroup: SVGGElement, linkGroup: SVGGElement, markerGroup: SVGDefsElement) {
		function leftRightForce(alpha: number) {
			const strength = 30;

			graph.links.forEach((link: Link) => {
				const sourceNode = link.source as Node;
				const targetNode = link.target as Node;

				if (sourceNode.x && targetNode.x) {
					sourceNode.x -= alpha * strength;

					targetNode.x += alpha * strength;
				}
			});
		}

		const simulation = d3.forceSimulation(graph.nodes)
			.force('link', d3.forceLink(graph.links).id((d: any) => d.id).distance(200).strength(0.25))
			.force('charge', d3.forceManyBody().strength(-800))
			.force('center', d3.forceCenter(width / 2, height / 2).strength(1000))
			.force('left-right', leftRightForce);

		simulation
			.nodes(graph.nodes)
			.on('tick', () => {
				d3.select(linkGroup)
					.selectAll('.link')
					.data(graph.links)
					.attr('x1', (d: Link) => (d.source as Node).x!)
					.attr('y1', (d: Link) => (d.source as Node).y!)
					.attr('x2', (d: Link) => (d.target as Node).x!)
					.attr('y2', (d: Link) => (d.target as Node).y!);


				d3.select(markerGroup).selectAll('.marker').data(graph.links)
					.attr('refX', d => {
						const x1 = (d.source as Node).x!;
						const y1 = (d.source as Node).y!;
						const x2 = (d.target as Node).x!;
						const y2 = (d.target as Node).y!;

						return -Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2)) / 3.3;
					});


				d3.select(nodeGroup).selectAll('.node').data(graph.nodes)
					.attr('transform', d => `translate(${d.x},${d.y})`);
			});

		(d3.select(nodeGroup).selectAll('.node').data(graph.nodes) as d3.Selection<Element, Node, SVGGElement, unknown>)
			.call(d3.drag<Element, Node>()
				.on('start', dragStarted)
				.on('drag', dragged)
				.on('end', dragEnded));

		function dragStarted(event: D3DragEvent<SVGRectElement, Node, Node>, d: Node) {
			if (!event.active) simulation.alphaTarget(0.3).restart();
			d.fx = d.x;
			d.fy = d.y;
		}

		function dragged(event: D3DragEvent<SVGRectElement, Node, Node>, d: Node) {
			d.fx = event.x;
			d.fy = event.y;
		}

		function dragEnded(event: D3DragEvent<SVGRectElement, Node, Node>, d: Node) {
			if (!event.active) simulation.alphaTarget(0);
			d.fx = null;
			d.fy = null;
		}

		return simulation;

	}


</script>


