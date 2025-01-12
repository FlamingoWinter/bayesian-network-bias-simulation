<script lang="ts">
	import { toTitleCase } from '../utiliites/toTitleCase';
	import type { Node } from '../types/network';
	import { cancelDescribe, conditionNode, describeNode, expandedNodeId, network } from '../stores/store';
	import ButtonRow from './ButtonRow.svelte';
	import ExpandButton from './ExpandButton.svelte';
	import ButtonBelowDistribution from './ButtonBelowDistribution.svelte';
	import { onDestroy, onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import CategoricalDistribution from './CategoricalDistribution.svelte';
	import DiscreteDistribution from './DiscreteDistribution.svelte';
	import ContinuousDistribution from './ContinuousDistribution.svelte';

	interface Margin {
		top: number,
		right: number,
		bottom: number,
		left: number
	}

	export let node: Node;

	const rectWidth = 160;
	const rectHeight = 120;
	const foreignObjectWidth = rectWidth * 1.1;
	const foreignObjectHeight = rectHeight * 1.2;

	const chartMargin: Margin = {
		top: 15,
		right: 14,
		bottom: 25,
		left: $network.characteristics[node.id].type == 'categorical' ? 36 : 14
	};

	const chartWidth = rectWidth - chartMargin.left - chartMargin.right;
	const chartHeight = rectHeight - chartMargin.top - chartMargin.bottom;


	let expanded: boolean = false;
	let isHovered: boolean = false;

	function calculateRectangleFill(characteristic: string,
																	scoreCharacteristic: string,
																	applicationCharacteristics: string[]) {
		if (characteristic == scoreCharacteristic) {
			return '#fffade';
		}
		if (applicationCharacteristics.includes(characteristic)) {
			return '#fff3fc';
		}
		return '#ffffff';
	}

	const heightMultiplier = 1.58;
	const scaleMultiplier = 1.4;

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
		} else {
			$cancelDescribe();
		}
		expanded = !expanded;
	}

	$:if (expanded && $expandedNodeId != node.id) {
		toggleExpand();
	}

	function toggleScoreCharacteristic() {
		if ($network.scoreCharacteristic === node.id) {
			$network.scoreCharacteristic = '';
		} else {
			$network.scoreCharacteristic = node.id;
		}
		const index = $network.applicationCharacteristics.indexOf(node.id);
		if (index > -1) {
			$network.applicationCharacteristics.splice(index, 1);
		}
	}

	function toggleApplicationCharacteristic() {
		if ($network.scoreCharacteristic === node.id) {
			$network.scoreCharacteristic = '';
		}
		const index = $network.applicationCharacteristics.indexOf(node.id);
		if (index > -1) {
			$network.applicationCharacteristics.splice(index, 1);
		} else {
			$network.applicationCharacteristics.push(node.id);
		}
		$network.applicationCharacteristics = [...$network.applicationCharacteristics];

	}
</script>


<g class="innerNode"
	 style="transition: transform 500ms cubic-bezier(0.68, -0.55, 0.27, 1.55)"
	 transform={expanded ? `scale(${scaleMultiplier})` : ""}
>


	<rect rx="2" ry="2" width={rectWidth} height={expanded ? rectHeight * heightMultiplier : rectHeight}
				stroke="#333333" stroke-width="0.7"
				x={-rectWidth/2} y={-rectHeight/2}
				fill={calculateRectangleFill(node.id, $network.scoreCharacteristic, $network.applicationCharacteristics)}
				style="transition: height 500ms cubic-bezier(0.68, -0.55, 0.27, 1.55), fill 300ms">

	</rect>

	<text x={0} y={-rectHeight /2 - 7} text-anchor="middle" fill="#333333" font-weight="600" font-size="18px">
		{toTitleCase(node.id)}
	</text>
	<g width={chartWidth} height={chartHeight}
		 transform={`translate(${chartMargin.left - rectWidth / 2}, ${chartMargin.top - rectHeight / 2})`}
	>
		{#if $network.characteristics[node.id].type === "categorical"}
			<CategoricalDistribution nodeId={node.id} width={chartWidth} height={chartHeight} />
		{:else if $network.characteristics[node.id].type === "discrete"}
			<DiscreteDistribution nodeId={node.id} width={chartWidth} height={chartHeight} />

		{:else}
			<ContinuousDistribution nodeId={node.id} width={chartWidth} height={chartHeight} />
		{/if}
	</g>

	<!--svelte-ignore a11y-mouse-events-have-key-events-->
	<!--svelte-ignore a11y-no-static-element-interactions-->
	<foreignObject height={expanded ? foreignObjectHeight * heightMultiplier : foreignObjectHeight}
								 width={foreignObjectWidth}
								 class="expand-button-container"
								 x={-foreignObjectWidth / 2}
								 y={-foreignObjectHeight / 2}
								 style="pointer-events: all;
											transition: height 500ms cubic-bezier(0.68, -0.55, 0.27, 1.55);
											z-index: 20"
								 on:mouseover={() => {isHovered = true}}
								 on:mouseleave={() => {isHovered = false}}>

		{#if !expanded}
			<div class="absolute bottom-1 right-0">
				<ExpandButton isHovered={isHovered} callbackFunction={toggleExpand} />
			</div>
		{/if}


		{#if expanded}
			<div class="flex items-center flex-col justify-end h-full pb-8 pr-4 pl-4 gap-1"
					 in:fade={{ duration: 200, delay: 300 }}
					 out:fade={{ duration: 100 }}
			>
				<ButtonRow>
					<ButtonBelowDistribution text="Describe" callback={()=>{$describeNode(node.id)}} />
					<ButtonBelowDistribution text="Condition" callback={()=>{$conditionNode(node.id)}} />
				</ButtonRow>
				<ButtonRow>
					<ButtonBelowDistribution
						text="{$network.scoreCharacteristic === node.id ? `Unset` : `Set`} Score Characteristic"
						callback={toggleScoreCharacteristic} />
				</ButtonRow>

				<ButtonRow>
					<ButtonBelowDistribution
						text="{$network.applicationCharacteristics.includes(node.id)  ? `Unset` : `Set`} Application Characteristic"
						callback={toggleApplicationCharacteristic}
					/>
				</ButtonRow>

			</div>
		{/if}

	</foreignObject>
</g>