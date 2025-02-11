{#if $modalStore[0] && $biasAnalysis !== undefined}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
	<div class="h-full flex flex-col gap-5 justify-center items-center">
		<div transition:fade={{ duration: 400 } } on:click|stopPropagation role="alertdialog"
				 class="card p-1 bg-surface-200-700-token view w-[50vw] min-w-64 h-[40rem] max-h-[90vh] overflow-y-scroll drop-shadow-md rounded-lg flex flex-col justify-between">
			<div>
				<ModalDivider />
				<ModalRow center={false}>
					<h3 class="text-4xl font-bold pb-4">Bias Summary</h3>
				</ModalRow>

				<TabGroup class="px-8">
					{#each Object.keys($biasAnalysis) as recruiterName}
						<Tab bind:group={tabSet} name="{recruiterName}" value={recruiterName}>
							{recruiterName}
						</Tab>
					{/each}
					<svelte:fragment slot="panel">
						{#each Object.keys($biasAnalysis) as recruiterName}
							{#if tabSet === recruiterName}
								<CategoricalRecruiterBiasSummary recruiter={$biasAnalysis[recruiterName].categoricalBiasAnalysis} />
							{/if}
						{/each}
					</svelte:fragment>
				</TabGroup>
			</div>

			<footer class="flex justify-end">
				<div class="flex gap-2">
					<button class="btn variant-outline-primary m-2" on:click={()=>{modalStore.close()}}>Close</button>
				</div>
			</footer>
		</div>
	</div>


{/if}

<ModalPopups />

<script lang="ts">
	import { fade } from 'svelte/transition';
	import { getModalStore, Tab, TabGroup } from '@skeletonlabs/skeleton';
	import ModalPopups from '../../popups/ModalPopups.svelte';
	import ModalDivider from '../ModalDivider.svelte';
	import ModalRow from '../ModalRow.svelte';
	import { biasAnalysis } from '../../../stores/store';
	import { onMount } from 'svelte';
	import CategoricalRecruiterBiasSummary
		from './CategoricalRecruiterBiasSummary/CategoricalRecruiterBiasSummary.svelte';

	const modalStore = getModalStore();

	let tabSet: string = Object.keys($biasAnalysis!)[0];

	onMount(() => {
		if ($biasAnalysis !== undefined) {
			tabSet = Object.keys($biasAnalysis!)[0];
		}
	});
</script>