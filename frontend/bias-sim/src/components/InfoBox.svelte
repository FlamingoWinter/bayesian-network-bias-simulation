<script lang="ts">
	import { ProgressRadial, RadioGroup, RadioItem } from '@skeletonlabs/skeleton';
	import { toTitleCase } from '../utilities/toTitleCase.js';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { CaretRightFill } from 'svelte-bootstrap-icons';
	import type { Network } from '../types/network';

	let loading = false;
	let nodeName = '';

	export let network: Network;
	export let conditions: Record<string, number>;
	export let condition: (characteristic: string, value: number | null) => Promise<void>;

	export let openConditionDialog: (expandedNode: string) => Promise<void>;
	export let exitDialog: () => void;

	let categoricalValues: string[] = [];
	let isInfoBoxVisible = false;
	let valueSelected = '';

	onMount(() => {
		openConditionDialog = async (nodeId: string) => {
			if (nodeId in conditions) {
				await condition(nodeId, null);
				return;
			}

			const characteristic = network!.characteristics[nodeId];

			nodeName = nodeId;
			isInfoBoxVisible = true;
			categoricalValues = characteristic.categoryNames;
			valueSelected = categoricalValues[0];
		};

		exitDialog = () => {
			nodeName = '';
			isInfoBoxVisible = false;
		};
	});
</script>

{#if isInfoBoxVisible}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->

	<div
		transition:fly={{ y: 50, duration: 400 }}
		on:click|stopPropagation
		role="alertdialog"
		class="card bg-surface-200-700-token fixed bottom-4 right-4 z-10 flex min-h-80 w-72 flex-col rounded-lg p-4 drop-shadow-md"
	>
		<div class="flex h-full flex-grow flex-col justify-between">
			<div>
				<h3 class="mb-4 text-center text-2xl font-bold">Condition {toTitleCase(nodeName)}</h3>
				<p class="mb-4 text-xs text-gray-600">
					Select a value to see how its observation affects uncertainty in the network:
				</p>
				<RadioGroup class="mb-10 flex w-full flex-wrap" rounded="rounded-container-token">
					{#each categoricalValues as categoricalValue}
						<RadioItem bind:group={valueSelected} name="justify" value={categoricalValue}
							>{categoricalValue}</RadioItem
						>
					{/each}
				</RadioGroup>
			</div>
			<div class="flex w-full justify-center">
				<button
					type="button"
					class="variant-filled btn btn-lg relative min-w-32 rounded-full px-4 py-2"
					on:click={async () => {
						loading = true;
						await condition(nodeName, categoricalValues.indexOf(valueSelected));
						loading = false;
						exitDialog();
					}}
				>
					{#if loading}
						<ProgressRadial
							class="w-7"
							meter="stroke-primary-100"
							track="stroke-primary-100/30"
							strokeLinecap="butt"
							value={undefined}
							stroke={100}
						/>
					{:else}
						Condition
						<CaretRightFill />
					{/if}
				</button>
			</div>
		</div>
	</div>
{/if}
