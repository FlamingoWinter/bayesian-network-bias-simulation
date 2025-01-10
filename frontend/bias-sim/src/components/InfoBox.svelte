{#if isInfoBoxVisible}
	<div transition:fly={{ y: 50, duration: 400 }}
			 class="fixed bottom-4 right-4 card p-4 bg-surface-200-700-token w-72 min-h-80 drop-shadow-md rounded-lg">
		<h3 class="text-xl font-bold mb-4">{heading}</h3>
		<p class="text-base text-gray-600">{paragraph}</p>
	</div>
{/if}

<script lang="ts">
	import { cancelDescribe, describeNode, network } from '../stores/store';
	import { toTitleCase } from '../utiliites/toTitleCase.js';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';


	let heading = '';
	let paragraph = '';
	let isInfoBoxVisible = true;

	onMount(() => {
		$describeNode = (expandedNode: string) => {
			if (heading == toTitleCase(expandedNode)) {
				$cancelDescribe();
			} else {
				heading = toTitleCase(expandedNode);
				paragraph = $network!.descriptionsByCharacteristic[expandedNode];
				isInfoBoxVisible = true;
			}
		};

		$cancelDescribe = () => {
			heading = '';
			paragraph = '';
			isInfoBoxVisible = false;
		};
	});
</script>