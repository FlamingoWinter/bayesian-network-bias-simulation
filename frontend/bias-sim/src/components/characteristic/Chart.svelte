<g class="innerNode"
	 style="transition: transform {defaultTransition}"
	 transform={(expanded && !disableInteraction) ? `scale(${scaleMultiplier})` : ""}
>

	<CharacteristicRectangle width={rectWidth} height={rectHeight}
													 expanded={(expanded && !disableInteraction)} nodeId={node.id}
													 heightMultiplier={heightMultiplier}
													 network={network}
													 scoreAndApplication={scoreAndApplication} />

	<CharacteristicTitle nodeId={node.id} rectHeight={rectHeight} />

	<g width={chartWidth} height={chartHeight}
		 transform={`translate(${chartMargin.left - rectWidth / 2}, ${chartMargin.top - rectHeight / 2})`}
	>
		{#if characteristic.type === "categorical"}
			<CategoricalDistribution
				conditions={conditions} conditioned={conditioned} posteriorDistributions={posteriorDistributions}
				characteristic={characteristic} width={chartWidth} height={chartHeight} />
		{:else if characteristic.type === "discrete"}
			<DiscreteDistribution
				conditions={conditions} conditioned={conditioned} posteriorDistributions={posteriorDistributions}
				characteristic={characteristic} width={chartWidth} height={chartHeight} />
		{:else}
			<ContinuousDistribution
				conditions={conditions} conditioned={conditioned} posteriorDistributions={posteriorDistributions}
				characteristic={characteristic} width={chartWidth} height={chartHeight} />
		{/if}
	</g>

	<CharacteristicConfigContainer height={foreignObjectHeight} width={foreignObjectWidth}
																 heightMultiplier={heightMultiplier} expanded={(expanded && !disableInteraction)}
																 bind:isHovered={isHovered}
	>
		{#if !disableInteraction}
			{#if !expanded}
				<ExpandButton isHovered={isHovered} callbackFunction={toggleExpand} />
			{:else}
				<CharacteristicConfig
					openConditionDialog={openConditionDialog}
					conditions={conditions}
					network={network} node={node} scoreAndApplication={scoreAndApplication} />
			{/if}
		{/if}

	</CharacteristicConfigContainer>
</g>

<script lang="ts">
	import type { Characteristic, Network, Node } from '../../types/network';
	import { expandedNodeId } from '../../stores/store';
	import ExpandButton from './config/CharacteristicExpandButton.svelte';
	import { onMount } from 'svelte';
	import CategoricalDistribution from './distributions/CategoricalDistribution.svelte';
	import DiscreteDistribution from './distributions/DiscreteDistribution.svelte';
	import ContinuousDistribution from './distributions/ContinuousDistribution.svelte';
	import { defaultTransition } from '../../animation/transition';
	import CharacteristicRectangle from './CharacteristicRectangle.svelte';
	import CharacteristicTitle from './CharacteristicTitle.svelte';
	import CharacteristicConfigContainer from './config/CharacteristicConfigContainer.svelte';
	import CharacteristicConfig from './config/CharacteristicConfig.svelte';
	import { addRepelForceFromNode, removeRepelForce } from '../../animation/forceSimulation';
	import * as d3 from 'd3';


	export let network: Network;
	export let node: Node;
	export let characteristic: Characteristic;
	export let disableInteraction: boolean;
	export let conditions: Record<string, number>;
	export let conditioned: boolean;
	export let posteriorDistributions: Record<string, number[]>;

	export let scoreAndApplication: boolean;
	export let simulation: d3.Simulation<Node, undefined>;
	export let openConditionDialog: (expandedNode: string) => Promise<void>;
	export let exitDialog: () => void;


	const rectWidth = 160;
	const rectHeight = 120;
	const heightMultiplier = scoreAndApplication ? 1.58 : 1.3;
	const scaleMultiplier = 1.4;
	const foreignObjectWidth = rectWidth * 1.1;
	const foreignObjectHeight = rectHeight * 1.2;

	const chartMargin: Margin = {
		top: 15,
		right: 14,
		bottom: 25,
		left: characteristic.type == 'categorical' ? 36 : 14
	};

	const chartWidth = rectWidth - chartMargin.left - chartMargin.right;
	const chartHeight = rectHeight - chartMargin.top - chartMargin.bottom;


	let expanded: boolean = false;
	let isHovered: boolean = false;


	const handleClickOutside = (event: MouseEvent) => {
		if (isHovered && !expanded) {
			toggleExpand();
		}
		if (!isHovered && expanded) {
			toggleExpand();
		}
	};

	onMount(() => {
		document.addEventListener('click', handleClickOutside);
		return () => {
			document.removeEventListener('click', handleClickOutside);
		};
	});


	function toggleExpand() {
		if (!expanded) {
			$expandedNodeId = node.id;
			addRepelForceFromNode(node, simulation, network.graph, 120, 130);
		} else {
			removeRepelForce(node, simulation);
			exitDialog();
		}
		expanded = !expanded;
	}

	$:if (expanded && $expandedNodeId != node.id) {
		toggleExpand();
	}


	interface Margin {
		top: number,
		right: number,
		bottom: number,
		left: number
	}
</script>
