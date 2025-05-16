{#if $modalStore[0]}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
	<div class="h-full flex flex-col gap-5 justify-center items-center">
		<div transition:fade={{ duration: 400 } } on:click|stopPropagation role="alertdialog"
				 class="card p-4 bg-surface-200-700-token view w-[50vw] min-w-64 h-[40rem] max-h-[90vh] overflow-y-scroll hide-scrollbar drop-shadow-md rounded-lg flex flex-col justify-between">
			<div>
				<ModalDivider />
				<ModalRow center={false}>
					<h3 class="text-2xl font-bold  text-center">Run Simulation and Measure Bias</h3>
				</ModalRow>

				<ModalRow center={true}>
					<div class="absolute left-4">
						<InfoHover target="number-of-nodes" />
					</div>
					<h3 class="text-md font-bold min-w-[10rem]">Candidates to Generate:</h3>
					<input class="input p-2 rounded-container-token"
								 type="number" placeholder="Candidates to Generate..."
								 bind:value={candidatesToGenerate}
								 min={1000} max={100_000} />
				</ModalRow>
				{#if candidatesToGenerate < 1000}
					<p class="text-red-500 text-md">Minimum is 1000 candidates</p>
				{/if}

				<ModalRow center={true} gap={10}>
					<div class="absolute left-4">
						<InfoHover target="number-of-nodes" />
					</div>
					<h3 class="text-md font-bold min-w-[10rem]">Training Proportion:</h3>

					<RangeSlider name="range-slider" bind:value={trainProportion} min={0.1} max={0.9} step={0.01} ticked
											 class="w-[250%]">
					</RangeSlider>
					<input class="input p-2 rounded-container-token flex-shrink"
								 type="number" placeholder="Proportion..."
								 bind:value={trainProportion}
								 min={1000} max={10_000_000} />
				</ModalRow>

				<ModalRow>
					<div class="absolute left-4">
						<InfoHover target="number-of-nodes" />
					</div>
					<h3 class="text-md font-bold min-w-[10rem]">Recruiters:</h3>
					<div class="flex-grow"></div>
				</ModalRow>

				<Accordion class="px-8">
					{#each Object.values(recruiterStates) as recruiterAndMitigationState}
						<AccordionItem
							on:click={() => { recruiterAndMitigationState.ticked = !recruiterAndMitigationState.ticked; }}>
							<svelte:fragment slot="summary">
								<div>
									{#if recruiterAndMitigationState.ticked}
										<Check2Square class="size-5 inline" />
									{:else}
										<Square class="size-5 inline" />
									{/if}
									<h3
										class="text-xl font-bold align-top inline px-2"
									>{recruiterAndMitigationState.recruiterName}</h3>
								</div>
							</svelte:fragment>
							<svelte:fragment slot="content">
								<div class="flex justify-start gap-2 flex-grow flex-wrap">
									{#each Object.values(recruiterAndMitigationState.mitigations) as mitigationState}
										<button
											class="chip {mitigationState.ticked ? 'variant-filled' : 'variant-soft'}"
											on:click={() => { mitigationState.ticked = !mitigationState.ticked; }}
										>

											{#if mitigationState.ticked}
												<Check2Square class="size-4 inline" />
											{:else}
												<Square class="size-4 inline" />
											{/if}
											<span class="capitalize">{mitigationState.mitigationName}</span>
										</button>
									{/each}
								</div>
							</svelte:fragment>
						</AccordionItem>
					{/each}
				</Accordion>


				<ModalRow center={true}>
					<div class="absolute left-4">
						<InfoHover target="number-of-nodes" />
					</div>
					<h3 class="text-md font-bold min-w-[10rem]">Protected Characteristic:</h3>

					<select class="select" bind:value={selectedProtectedCharacteristic} required>
						{#each Object.values(network.characteristics) as characteristic}
							<option value={characteristic.name}>{characteristic.name}</option>
						{/each}
					</select>
				</ModalRow>


			</div>

			<footer class="flex justify-end">
				<div class="flex gap-2">
					<button class="btn variant-outline-primary" on:click={()=>{modalStore.close()}}>Cancel</button>
					<button class="btn variant-outline-secondary"
									on:click={async ()=>{
							await awaitSocketClose(simulateSocket)

							simulateSocket = await awaitSocketOpen(new WebSocket(`${webSocketUrl}/simulate/?session_key=${$sessionKey}`));

							simulateSocket.send(generateSimulateJson())

							modalStore.close()

							await $deconditionAll()

							await $loadProcess(simulateSocket)
							await $invalidateBias()
							modalStore.trigger(showBiasModal)
						}}>Submit
					</button>
				</div>
			</footer>

		</div>
	</div>


{/if}

<ModalPopups />

<script lang="ts">
	import { fade } from 'svelte/transition';

	import { awaitSocketClose, awaitSocketOpen } from '../../../utilities/socket';


	import {
		Accordion,
		AccordionItem,
		getModalStore,
		type ModalComponent,
		type ModalSettings,
		RangeSlider
	} from '@skeletonlabs/skeleton';
	import ModalPopups from '../../popups/ModalPopups.svelte';
	import Check2Square from 'svelte-bootstrap-icons/lib/Check2Square.svelte';
	import Square from 'svelte-bootstrap-icons/lib/Square.svelte';


	import { webSocketUrl } from '../../../utilities/api';
	import { deconditionAll, invalidateBias, loadProcess } from '../../../stores/functions';
	import { sessionKey } from '../../../stores/store';
	import ModalDivider from '../ModalDivider.svelte';
	import ModalRow from '../ModalRow.svelte';
	import InfoHover from '../../popups/InfoHover.svelte';
	import ShowBiasModal from '../show_bias_modal/ShowBiasModal.svelte';
	import type { Network } from '../../../types/network';

	export let network: Network;

	const modalStore = getModalStore();

	const showBiasModalComponent: ModalComponent = { ref: ShowBiasModal };

	const showBiasModal: ModalSettings = {
		type: 'component',
		component: showBiasModalComponent,
		backdropClasses: 'bg-gradient-to-tr from-indigo-500/50 via-purple-500/50 to-pink-500/50'

	};

	let simulateSocket: WebSocket | undefined = undefined;

	let candidatesToGenerate: number = 10_000;
	let trainProportion: number = 0.9;
	let selectedProtectedCharacteristic: string;

	const recruiterNamesAndSlugs: Record<string, string> = {
		'Random Forest': 'random_forest',
		'Logistic Regression': 'logistic_regression',
		'Encoder-Only Transformer': 'transformer',
		'Shallow Multi-Layer Perceptron': 'shallow_mlp',
		'Deep Multi-Layer Perceptron': 'deep_mlp',
		'Bayesian Network Approximation': 'bayesian',
		'Support Vector Machine': 'svm'
	};

	const mitigationNamesAndSlugs: Record<string, string> = {
		'Satisfy Demographic Parity': 'satisfy_dp',
		'Satisfy Proportional Parity': 'satisfy_pp',
		'Optimise FNR Parity, FPR Parity, and Accuracy': 'optimise_fnr_fpr_accuracy',
		'Optimise FNR Parity and FPR Parity': 'optimise_fnr_fpr',
		'Optimise FNR Parity': 'optimise_fnr',
		'Optimise FPR Parity': 'optimise_fpr',
		'Optimise FDR Parity, FOR Parity and Accuracy': 'optimise_fdr_for_accuracy',
		'Optimise FDR Parity and FOR Parity': 'optimise_fdr_for',
		'Optimise FDR Parity': 'optimise_fdr',
		'Optimise FOR Parity': 'optimise_for'
	};

	const continuousRecruiters: string[] = [
		'Simple Linear Regression'
	];

	type MitigationState = {
		mitigationName: string,
		ticked: boolean
	}

	type RecruiterAndMitigationState = {
		recruiterName: string,
		ticked: boolean,
		mitigations: Record<string, MitigationState>
	}

	const recruiterStates: Record<string, RecruiterAndMitigationState> = Object.fromEntries(
		Object.keys(recruiterNamesAndSlugs).map(recruiter => [
			recruiter,
			{
				recruiterName: recruiter,
				ticked: false,
				mitigations: Object.fromEntries(
					Object.keys(mitigationNamesAndSlugs).map(mitigation => [mitigation, {
						mitigationName: mitigation,
						ticked: false
					}])
				)
			}
		])
	);


	function generateSimulateJson() {
		return JSON.stringify({
			'candidates_to_generate': candidatesToGenerate,
			'train_proportion': trainProportion,
			'recruiters': Object.fromEntries(
				Object.values(recruiterStates)
					.filter(recruiterState => recruiterState.ticked)
					.map(recruiterState => [
						recruiterNamesAndSlugs[recruiterState.recruiterName],
						['no_mitigation'].concat(Object.values(recruiterState.mitigations)
							.filter(mitigationState => mitigationState.ticked)
							.map(mitigationState => mitigationNamesAndSlugs[mitigationState.mitigationName]))
					])
			),
			'protected_characteristic': selectedProtectedCharacteristic
		});
	}

</script>