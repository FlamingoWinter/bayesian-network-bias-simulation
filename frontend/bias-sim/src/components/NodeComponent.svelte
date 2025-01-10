<script lang="ts">
	import ExpandButton from './ExpandButton.svelte';
	import * as d3 from 'd3';
	import { onDestroy, onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import ButtonBelowDistribution from './ButtonBelowDistribution.svelte';
	import ButtonRow from './ButtonRow.svelte';

	import { cancelDescribe, describeNode, expandedNode } from '../stores/store';


	export let foreignObjectElement: SVGForeignObjectElement;
	export let innerNode: SVGGElement;
	export let rect: SVGRectElement;
	export let nodeName: string;

	let isHovered = false;
	let expanded = false;

	let originalInnerNodeTransform: string;
	let originalRectHeight: number;
	let originalForeignObjectHeight: number;

	const heightMultiplier = 1.58;
	const scaleMultiplier = 1.4;


	onMount(() => {
		if (innerNode) {
			originalInnerNodeTransform = d3.select(innerNode).attr('transform') || '';
		}
		if (rect) {
			originalRectHeight = +d3.select(rect).attr('height');
		}
		if (foreignObjectElement) {
			originalForeignObjectHeight = +d3.select(foreignObjectElement).attr('height');
		}
		if (foreignObjectElement) {
			d3.select(foreignObjectElement)
				.on('mouseover', () => {
					isHovered = true;
				})
				.on('mouseout', () => {
					isHovered = false;
				});
		}
	});

	const handleClickOutside = (event: MouseEvent) => {
		if (!isHovered && expanded) {
			toggleExpand();
		}
	};

	document.addEventListener('click', handleClickOutside);

	onDestroy(() => {
		document.removeEventListener('click', handleClickOutside);
	});


	function toggleExpand() {
		if (!expanded) {
			$expandedNode = nodeName;
			d3.select(innerNode).attr('transform', `${originalInnerNodeTransform} scale(${scaleMultiplier})`);
			d3.select(rect).attr('height', originalRectHeight * heightMultiplier);
			d3.select(foreignObjectElement).attr('height', originalForeignObjectHeight * heightMultiplier);
		} else {
			$cancelDescribe();
			d3.select(innerNode).attr('transform', `${originalInnerNodeTransform}`);
			d3.select(rect).attr('height', originalRectHeight);
			d3.select(foreignObjectElement).attr('height', originalForeignObjectHeight);
		}
		expanded = !expanded;
	}

	$:if (expanded && $expandedNode != nodeName) {
		toggleExpand();
	}
</script>

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
			<ButtonBelowDistribution text="Describe" callback={()=>{$describeNode(nodeName)}} />
			<ButtonBelowDistribution text="Condition" />
		</ButtonRow>
		<ButtonRow>
			<ButtonBelowDistribution text="Set Score Characteristic" />
		</ButtonRow>

		<ButtonRow>
			<ButtonBelowDistribution text="Set Application Characteristic" />
		</ButtonRow>

	</div>
{/if}