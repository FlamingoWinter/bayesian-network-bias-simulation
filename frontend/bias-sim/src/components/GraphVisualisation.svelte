{#if network}
	<svg bind:this={svg} width={width} height={height}
			 class="font-roboto font-normal">
		<g bind:this={zoomGroup}>
			<g bind:this={linkGroup}>
				{#each network.graph.links as link}
					<line class="link" stroke="#aaa"
								marker-start={`url(#arrowhead-${link.index})`} />
				{/each}
			</g>
			<g bind:this={nodeGroup}>
				{#each network.graph.nodes as node}
					<g class="node" id="node-{node.id}">
						<Chart
							openConditionDialog={openConditionDialog}
							exitDialog={exitDialog}
							simulation={simulation}
							conditions={conditions} conditioned={conditioned} posteriorDistributions={posteriorDistributions}
							disableInteraction={disableInteraction} characteristic={network.characteristics[node.id]}
							node={node} bind:network={network}
							scoreAndApplication={scoreAndApplication} />
					</g>
				{/each}
			</g>
			<defs bind:this={markerGroup}>
				{#each network.graph.links as link}
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
	<InfoBox
		bind:openConditionDialog={openConditionDialog}
		bind:exitDialog={exitDialog}
		network={network} conditions={conditions} condition={condition} />
{/if}


<script lang="ts">
	import * as d3 from 'd3';
	import { onMount } from 'svelte';

	import InfoBox from './InfoBox.svelte';
	import Chart from './characteristic/Chart.svelte';
	import { applyForceSimulation } from '../animation/forceSimulation';
	import { applyZoom } from '../animation/zoom';
	import type { Network, Node } from '../types/network';
	import { apiRequest } from '../utilities/api';
	import { getToastStore, type ToastSettings } from '@skeletonlabs/skeleton';
	import { deconditionAll } from '../stores/functions';

	export let width: number;
	export let height: number;
	export let disableInteraction: boolean = false;
	export let noPan: boolean = false;
	export let scoreAndApplication: boolean = true;
	export let initialZoom: number = 1;
	export let predefinedModel: string | null = null;
	export let initialTranslate: Point | null = null;

	type Point = {
		x: number;
		y: number;
	};

	export let network: Network | undefined;

	let conditions: Record<string, number> = {};
	let condition: (characteristic: string, value: number | null) => Promise<void>;
	let conditioned: boolean = false;
	let posteriorDistributions: Record<string, number[]>;
	let simulation: d3.Simulation<Node, undefined>;

	let svg: SVGElement;

	let zoomGroup: SVGGElement;
	let linkGroup: SVGGElement;
	let nodeGroup: SVGGElement;
	let markerGroup: SVGDefsElement;

	let openConditionDialog: (expandedNode: string) => Promise<void> = async () => {
	};

	let exitDialog: () => void = () => {
	};


	onMount(async () => {
		const toastStore = getToastStore();

		applyZoom(svg, zoomGroup, initialZoom, initialTranslate, noPan);
		if (network) {
			simulation = applyForceSimulation(network.graph, width, height, nodeGroup, linkGroup, markerGroup);
		}

		condition = async (characteristic: string, value: number | null) => {
			const tempConditions = { ...conditions };
			if (value === null) {
				delete tempConditions[characteristic];
			} else {
				tempConditions[characteristic] = value;
			}

			let conditionResponse: Record<string, number[]> = {};
			try {
				if (Object.keys(tempConditions).length > 0) {
					conditionResponse = await apiRequest(`condition/${
						predefinedModel === null ? '' : predefinedModel + '/'
					}`, 'POST', JSON.stringify(tempConditions)) as Record<string, number[]>;
				}
				conditions = tempConditions;
				conditioned = Object.keys(tempConditions).length > 0;
				posteriorDistributions = conditionResponse;
			} catch (e) {
				const t: ToastSettings = {
					message: 'Conditioning for this variable failed. Did you try to condition on impossible evidence?',
					timeout: 3000,
					background: 'variant-filled-error'
				};
				toastStore.trigger(t);
			}
		};

		$deconditionAll = async () => {
			conditions = {};
			conditioned = false;
		};

	});


	$: {
		if (network) {
			applyZoom(svg, zoomGroup, initialZoom, initialTranslate, noPan);
			if (simulation) {
				simulation.stop();

			}
			simulation = applyForceSimulation(network.graph, width, height, nodeGroup, linkGroup, markerGroup);
		}
	}

	$: {
		if (simulation) {
			simulation.force('center', d3.forceCenter(width / 2, height / 2));
			simulation.alpha(1).restart();
		}
	}


</script>


