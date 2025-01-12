<g class="innerNode"
	 style="transition: transform {defaultTransition}"
	 transform={expanded ? `scale(${scaleMultiplier})` : ""}
>

	<CharacteristicRectangle width={rectWidth} height={rectHeight}
													 expanded={expanded} nodeId={node.id}
													 heightMultiplier={heightMultiplier} />

	<CharacteristicTitle nodeId={node.id} rectHeight={rectHeight} />

	<g width={chartWidth} height={chartHeight}
		 transform={`translate(${chartMargin.left - rectWidth / 2}, ${chartMargin.top - rectHeight / 2})`}
	>
		{#if characteristic.type === "categorical"}
			<CategoricalDistribution characteristic={characteristic} width={chartWidth} height={chartHeight} />
		{:else if characteristic.type === "discrete"}
			<DiscreteDistribution characteristic={characteristic} width={chartWidth} height={chartHeight} />

		{:else}
			<ContinuousDistribution characteristic={characteristic} width={chartWidth} height={chartHeight} />
		{/if}
	</g>

	<CharacteristicConfigContainer height={foreignObjectHeight} width={foreignObjectWidth}
																 heightMultiplier={heightMultiplier} expanded={expanded} bind:isHovered={isHovered}
	>
		{#if !expanded}
			<ExpandButton isHovered={isHovered} callbackFunction={toggleExpand} />
		{:else}
			<CharacteristicConfig node={node} />
		{/if}

	</CharacteristicConfigContainer>
</g>

<script lang="ts">
	import type { Characteristic, Node } from '../../types/network';
	import { cancelDescribe, expandedNodeId, network, simulation } from '../../stores/store';
	import ExpandButton from './config/CharacteristicExpandButton.svelte';
	import { onDestroy, onMount } from 'svelte';
	import CategoricalDistribution from './distributions/CategoricalDistribution.svelte';
	import DiscreteDistribution from './distributions/DiscreteDistribution.svelte';
	import ContinuousDistribution from './distributions/ContinuousDistribution.svelte';
	import { defaultTransition } from '../../animation/transition';
	import CharacteristicRectangle from './CharacteristicRectangle.svelte';
	import CharacteristicTitle from './CharacteristicTitle.svelte';
	import CharacteristicConfigContainer from './config/CharacteristicConfigContainer.svelte';
	import CharacteristicConfig from './config/CharacteristicConfig.svelte';
	import { addRepelForceFromNode, removeRepelForce } from '../../animation/forceSimulation';


	export let node: Node;
	export let characteristic: Characteristic;

	const rectWidth = 160;
	const rectHeight = 120;
	const heightMultiplier = 1.58;
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
		if (!isHovered && expanded) {
			toggleExpand();
		}
	};

	onMount(() => {
		document.addEventListener('click', handleClickOutside);
	});
	onDestroy(() => {
		document.removeEventListener('click', handleClickOutside);
	});


	function toggleExpand() {
		if (!expanded) {
			$expandedNodeId = node.id;
			addRepelForceFromNode(node, $simulation, $network.graph, 120, 130);
		} else {
			removeRepelForce(node, $simulation);
			$cancelDescribe();
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
