{#if isInfoBoxVisible}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
	<div transition:fly={{ y: 50, duration: 400 } } on:click|stopPropagation role="alertdialog"
			 class="fixed bottom-4 right-4 card p-4 bg-surface-200-700-token w-72 min-h-80 drop-shadow-md rounded-lg flex flex-col">
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
					{/if}
				</div>
				<div class="flex w-full justify-center">
					<button type="button"
									class="btn btn-lg variant-filled py-2 px-4 rounded-full">
						Condition
						<CaretRightFill />
					</button>
				</div>

			{/if}
		</div>
	</div>
{/if}

<script lang="ts">
	import { RadioGroup, RadioItem } from '@skeletonlabs/skeleton';
	import { cancelDescribe, conditionNode, describeNode, network, nodeDistributionByName } from '../stores/store';
	import { toTitleCase } from '../utiliites/toTitleCase.js';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { CaretRightFill } from 'svelte-bootstrap-icons';

	type ConditionSettings = {
		isCategorical: boolean;
		categoricalValues: string[];
	}


	let nodeName = '';
	let paragraph = '';


	let conditionSettings: ConditionSettings = {
		isCategorical: true,
		categoricalValues: []
	};
	let isInfoBoxVisible = false;
	let describe = false;
	let valueSelected = '';

	onMount(() => {
		$describeNode = (expandedNode: string) => {

			if (nodeName == expandedNode && describe) {
				$cancelDescribe();
			} else {
				nodeName = expandedNode;
				paragraph = $network!.descriptionsByCharacteristic[expandedNode];
				isInfoBoxVisible = true;
			}
			describe = true;
		};

		$conditionNode = (expandedNode: string) => {
			describe = false;
			nodeName = expandedNode;
			isInfoBoxVisible = true;
			if ($nodeDistributionByName[expandedNode].distributionType == 'categorical') {
				conditionSettings.isCategorical = true;
				conditionSettings.categoricalValues = $nodeDistributionByName[expandedNode].categoriesForCategoricalDistributions!;
			}
		};

		$cancelDescribe = () => {
			nodeName = '';
			paragraph = '';
			isInfoBoxVisible = false;
		};
	});
</script>