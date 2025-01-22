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
				<g class="node" id="node-{node.id}">
					<Chart characteristic={$network.characteristics[node.id]} node={node} />
				</g>
			{/each}
		</g>
		<defs bind:this={markerGroup}>
			{#each $network.graph.links as link}
				<marker id={`arrowhead-${link.index}`}
								viewBox="0 -5 10 10"
								refY={0}
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
	import * as d3 from 'd3';
	import { onMount } from 'svelte';

	import { network, simulation } from '../stores/store';
	import InfoBox from './InfoBox.svelte';
	import Chart from './characteristic/Chart.svelte';
	import { applyForceSimulation } from '../animation/forceSimulation';
	import { applyZoom } from '../animation/zoom';
	import type { Node } from '../types/network';

	export let width: number;
	export let height: number;

	let svg: SVGElement;
	let svgElement: d3.Selection<SVGElement, unknown, null, undefined>;

	let zoomGroup: SVGGElement;
	let linkGroup: SVGGElement;
	let nodeGroup: SVGGElement;
	let markerGroup: SVGDefsElement;


	onMount(async () => {
		applyZoom(svg, zoomGroup);
		$simulation = applyForceSimulation($network.graph, width, height, nodeGroup, linkGroup, markerGroup);

	});


	$: {
		if ($simulation) {
			$simulation.force('center', d3.forceCenter(width / 2, height / 2));
			$simulation.alpha(1).restart();
		}
	}

	function getTranslationFromTransform(s: string) {
		const match = s.match(/translate\(([-\d.]+),\s*([-\d.]+)\)/);

		if (!match || match.length < 2) {
			return { x: 0, y: 0 };
		}

		return { x: parseFloat(match[1]), y: parseFloat(match[2]) };
	}

	function asNode(node: Node | any): Node {
		return node as Node;
	}


</script>


