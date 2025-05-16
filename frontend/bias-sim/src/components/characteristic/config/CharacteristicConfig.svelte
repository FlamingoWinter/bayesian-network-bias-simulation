<div class="flex items-center flex-col justify-end h-full pb-8 pr-4 pl-4 gap-1"
		 in:fade={{ duration: 200, delay: 300 }}
		 out:fade={{ duration: 100 }}
>
	<ButtonRow>
		<ButtonBelowDistribution
			text="{node.id in conditions ? `Decondition` : `Condition`}"
			callback={()=>{openConditionDialog(node.id)}} />
	</ButtonRow>
	{#if scoreAndApplication}
		<ButtonRow>
			<ButtonBelowDistribution
				text="{network.scoreCharacteristic === node.id ? `Unset` : `Set`} Score Characteristic"
				callback={toggleScoreCharacteristic} />
		</ButtonRow>

		<ButtonRow>
			<ButtonBelowDistribution
				text={(network.applicationCharacteristics.includes(node.id) ? 'Unset' : 'Set') + ' Application Characteristic'}
				callback={toggleApplicationCharacteristic}
			/>
		</ButtonRow>
	{/if}

</div>


<script lang="ts">
	import ButtonRow from './ButtonRow.svelte';
	import ButtonBelowDistribution from './ButtonBelowDistribution.svelte';
	import { fade } from 'svelte/transition';
	import type { Network, Node } from '../../../types/network';

	export let node: Node;
	export let network: Network;
	export let scoreAndApplication: boolean = true;
	export let conditions: Record<string, number>;
	export let openConditionDialog: (expandedNode: string) => Promise<void>;


	function toggleScoreCharacteristic() {
		if (network.scoreCharacteristic === node.id) {
			network.scoreCharacteristic = '';
		} else {
			network.scoreCharacteristic = node.id;
		}
		const index = network.applicationCharacteristics.indexOf(node.id);
		if (index > -1) {
			network.applicationCharacteristics.splice(index, 1);
		}
		network = { ...network, applicationCharacteristics: [...network.applicationCharacteristics] };
	}

	function toggleApplicationCharacteristic() {
		if (network.scoreCharacteristic === node.id) {
			network.scoreCharacteristic = '';
		}
		const updatedApplicationCharacteristics = [...network.applicationCharacteristics];
		const index = network.applicationCharacteristics.indexOf(node.id);
		if (index > -1) {
			updatedApplicationCharacteristics.splice(index, 1);
		} else {
			updatedApplicationCharacteristics.push(node.id);
		}
		network = { ...network, applicationCharacteristics: updatedApplicationCharacteristics };

	}
</script>