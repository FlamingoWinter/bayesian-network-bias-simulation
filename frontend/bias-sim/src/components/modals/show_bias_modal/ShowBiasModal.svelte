{#if $modalStore[0] && $biasAnalysis !== undefined}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
	<div class="h-full flex flex-col gap-5 justify-center items-center">
		<div transition:fade={{ duration: 400 } } on:click|stopPropagation role="alertdialog"
				 class="card p-1 bg-surface-200-700-token view w-[50vw] min-w-64 h-[95vh]  drop-shadow-md rounded-lg flex flex-col justify-between">
			<div>
				<ModalDivider />
				<div class="flex pt-2 px-10 justify-between items-center gap-4 gap-4">
					<h3 class="text-4xl font-bold pb-4">Bias Summary</h3>

					<button class="btn variant-outline-primary m-2" on:click={()=>{modalStore.close()}}>
						<X />
					</button>
				</div>


				<TabGroup class="px-8" justify="flex-wrap">
					{#each Object.keys($biasAnalysis) as recruiterName}
						<Tab bind:group={tabSet} name="{recruiterName}" value={recruiterName}>
							{recruiterName}
						</Tab>
					{/each}
					<svelte:fragment slot="panel">
						{#each Object.keys($biasAnalysis) as recruiterName}
							<div class="{tabSet === recruiterName ? 'block' : 'hidden'}">
								<div class="overflow-y-scroll max-h-[65vh]">
									{#each Object.keys($biasAnalysis[recruiterName]) as mitigation}
										<div class="bg-gray-100 p-2 rounded-lg mb-3">
											<h3 class="text-xl font-bold pb-4 pl-4 pt-2 text-secondary-700">{mitigation}:</h3>
											<CategoricalRecruiterBiasSummary
												recruiter={$biasAnalysis[recruiterName][mitigation]}
												withoutMitigation={mitigation === "No Mitigation"
												? null
												: $biasAnalysis[recruiterName]?.["No Mitigation"] ?? null}
											/>

										</div>
									{/each}
								</div>
							</div>
						{/each}
					</svelte:fragment>
				</TabGroup>
			</div>


		</div>
	</div>


{/if}

<ModalPopups />

<script lang="ts">
	import { fade } from 'svelte/transition';
	import { getModalStore, Tab, TabGroup } from '@skeletonlabs/skeleton';
	import ModalPopups from '../../popups/ModalPopups.svelte';
	import ModalDivider from '../ModalDivider.svelte';
	import { biasAnalysis } from '../../../stores/store';
	import { onMount } from 'svelte';
	import { X } from 'svelte-bootstrap-icons';
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