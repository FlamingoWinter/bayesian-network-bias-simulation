{#if isInfoBoxVisible}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->

	<div transition:fly={{ y: 50, duration: 400 } } on:click|stopPropagation role="alertdialog"
			 class="fixed bottom-4 right-4 card p-4 bg-surface-200-700-token w-72 min-h-80 drop-shadow-md rounded-lg flex flex-col z-10">
		<div class="flex flex-col justify-between h-full flex-grow">

			{#if describe}
				<div>
					<h3 class="text-xl font-bold mb-4">{toTitleCase(nodeName)}</h3>
					<p class="text-base text-gray-600">{paragraph}</p>
				</div>
			{:else}
				<div>
					<h3 class="text-2xl font-bold mb-4 text-center">Condition {toTitleCase(nodeName)}</h3>
					<p class="text-xs text-gray-600 mb-4">Select a value to see how its observation affects uncertainty in the
						network:</p>
					{#if conditionSettings.isCategorical}
						<RadioGroup class="flex flex-wrap w-full mb-10" rounded="rounded-container-token">
							{#each conditionSettings.categoricalValues as categoricalValue}
								<RadioItem bind:group={valueSelected} name="justify"
													 value={categoricalValue}>{categoricalValue}</RadioItem>
							{/each}
						</RadioGroup>
					{:else}
						<RangeSlider name="range-slider" bind:value={numericalValueSelected}
												 min={(conditionSettings.min ?? 0)} max={conditionSettings.max ?? 0}
												 step={d3.tickStep(0, (conditionSettings.max ?? 0) - (conditionSettings.min ?? 0), 20)}
						>
							<div class="flex justify-between items-center">
								<div class="font-bold">{conditionSettings.min ?? 0}</div>
								<div class="font-bold">{conditionSettings.max ?? 0}</div>
							</div>
						</RangeSlider>
						<input class="input p-4 my-6" type="text" placeholder="Input" bind:value={numericalValueSelected}>
					{/if}
				</div>
				<div class="flex w-full justify-center">

					<button type="button"
									class="btn btn-lg variant-filled py-2 px-4 rounded-full relative min-w-32"
									on:click={async ()=>{
										loading = true;
										await condition(nodeName, conditionSettings.isCategorical ? conditionSettings.categoricalValues.indexOf(valueSelected) : numericalValueSelected);
									  loading = false;
										exitDialog()
										}}>
						{#if loading}
							<ProgressRadial class="w-7" meter="stroke-primary-100" track="stroke-primary-100/30"
															strokeLinecap="butt" value={undefined} stroke={100} />
						{:else}
							Condition
							<CaretRightFill />
						{/if}
					</button>

				</div>

			{/if}
		</div>
	</div>
{/if}

<script lang="ts">
	import { ProgressRadial, RadioGroup, RadioItem, RangeSlider } from '@skeletonlabs/skeleton';
	import { toTitleCase } from '../utiliites/toTitleCase.js';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { CaretRightFill } from 'svelte-bootstrap-icons';
	import * as d3 from 'd3';
	import type { Network } from '../types/network';

	type ConditionSettings = {
		isCategorical: boolean;
		categoricalValues: string[];
		min: number | null;
		max: number | null;
	}

	let loading = false;
	let nodeName = '';
	let paragraph = '';

	export let network: Network;
	export let conditions: Record<string, number>;
	export let condition: (characteristic: string, value: (number | null)) => Promise<void>;

	export let openConditionDialog: (expandedNode: string) => Promise<void>;
	export let openDescribeDialog: (expandedNode: string) => Promise<void>;
	export let exitDialog: () => void;


	let conditionSettings: ConditionSettings = {
		isCategorical: true,
		categoricalValues: [],
		min: null,
		max: null
	};
	let isInfoBoxVisible = false;
	let describe = false;
	let valueSelected = '';
	let numericalValueSelected: number;

	onMount(() => {
		openDescribeDialog = async (nodeId: string) => {
			const characteristic = network!.characteristics[nodeId];

			if (nodeName == nodeId && describe) {
				exitDialog();
			} else {
				if (!describe) {
					isInfoBoxVisible = false;
					await new Promise(resolve => setTimeout(resolve, 100));
					isInfoBoxVisible = true;
					describe = true;
				}

				nodeName = nodeId;
				paragraph = characteristic.description;
				isInfoBoxVisible = true;
			}
			describe = true;
		};


		openConditionDialog = async (nodeId: string) => {
			if (nodeId in conditions) {
				await condition(nodeId, null);
				return;
			}

			const characteristic = network!.characteristics[nodeId];
			if (describe) {
				isInfoBoxVisible = false;
				await new Promise(resolve => setTimeout(resolve, 100));
				isInfoBoxVisible = true;
				describe = false;
			}

			nodeName = nodeId;
			isInfoBoxVisible = true;
			conditionSettings.isCategorical = (characteristic.type === 'categorical');
			valueSelected = conditionSettings.categoricalValues[0];

			if (characteristic.type == 'categorical') {
				conditionSettings.categoricalValues = characteristic.categoryNames!;
			} else {
				const minValue = d3.min(characteristic.priorDistribution)!;
				const maxValue = d3.max(characteristic.priorDistribution)!;
				const ticks = d3.ticks(minValue, maxValue, 20);
				conditionSettings.min = ticks[0];
				conditionSettings.max = ticks[ticks.length - 1];

				if (minValue > ticks[0]) {
					conditionSettings.min = ticks[0] + (ticks[1] - ticks[0]);
				}
				if (maxValue < ticks[ticks.length - 1]) {
					conditionSettings.max = ticks[ticks.length - 1] - (ticks[1] - ticks[0]);
				}

				numericalValueSelected = conditionSettings.min;
			}
		};

		exitDialog = () => {
			nodeName = '';
			paragraph = '';
			isInfoBoxVisible = false;
		};
	});
</script>