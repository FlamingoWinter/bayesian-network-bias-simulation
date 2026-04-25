<script lang="ts">
	import { fade } from 'svelte/transition';
	import { getModalStore, Tab, TabGroup } from '@skeletonlabs/skeleton';
	import ModalPopups from '../../popups/ModalPopups.svelte';
	import ModalDivider from '../ModalDivider.svelte';
	import { biasAnalysis } from '../../../stores/store';
	import { onMount } from 'svelte';
	import { X } from 'svelte-bootstrap-icons';
	import CategoricalRecruiterBiasSummary from './CategoricalRecruiterBiasSummary/CategoricalRecruiterBiasSummary.svelte';

	const modalStore = getModalStore();

	let tabSet: string = Object.keys($biasAnalysis!)[0];

	onMount(() => {
		if ($biasAnalysis !== undefined) {
			tabSet = Object.keys($biasAnalysis!)[0];
		}
	});
</script>

{#if $modalStore[0] && $biasAnalysis !== undefined}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
	<div class="flex h-full flex-col items-center justify-center gap-5">
		<div
			transition:fade={{ duration: 400 }}
			on:click|stopPropagation
			role="alertdialog"
			class="view card bg-surface-200-700-token flex h-[95vh] w-[50vw] min-w-64 flex-col justify-between overflow-hidden rounded-lg p-1 drop-shadow-md"
		>
			<div>
				<ModalDivider />
				<div class="flex items-center justify-between gap-4 gap-4 px-10 pt-2">
					<h3 class="pb-4 text-4xl font-bold">Bias Summary</h3>

					<button
						class="variant-outline-primary btn m-2"
						on:click={() => {
							modalStore.close();
						}}
					>
						<X />
					</button>
				</div>
			</div>

			<TabGroup class="flex-grow px-8" justify="flex-wrap">
				{#each Object.keys($biasAnalysis) as recruiterName}
					<Tab bind:group={tabSet} name={recruiterName} value={recruiterName}>
						{recruiterName}
					</Tab>
				{/each}
				<svelte:fragment slot="panel">
					{#each Object.keys($biasAnalysis) as recruiterName}
						<div class={tabSet === recruiterName ? 'block' : 'hidden'}>
							<div class="hide-scrollbar max-h-[80vh] overflow-y-scroll">
								{#each Object.keys($biasAnalysis[recruiterName]) as mitigation}
									<div class="mb-3 rounded-lg bg-gray-100 p-2">
										<h3 class="pb-4 pl-4 pt-2 text-xl font-bold text-secondary-700">
											{mitigation}:
										</h3>
										<CategoricalRecruiterBiasSummary
											recruiter={$biasAnalysis[recruiterName][mitigation]}
											withoutMitigation={mitigation === 'No Mitigation'
												? null
												: ($biasAnalysis[recruiterName]?.['No Mitigation'] ?? null)}
										/>
									</div>
								{/each}
								<div class="h-[10em]"></div>
							</div>
						</div>
					{/each}
				</svelte:fragment>
			</TabGroup>
		</div>
	</div>
{/if}

<ModalPopups />
