<script lang="ts">
	import { fade } from 'svelte/transition';

	import { awaitSocketClose, awaitSocketOpen } from '../../../utilities/socket';

	import {
		Accordion,
		AccordionItem,
		getModalStore,
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

	const showBiasModal: ModalSettings = {
		type: 'component',
		component: { ref: ShowBiasModal },
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

	type MitigationState = {
		mitigationName: string;
		ticked: boolean;
	};

	type RecruiterAndMitigationState = {
		recruiterName: string;
		ticked: boolean;
		mitigations: Record<string, MitigationState>;
	};

	const recruiterStates: Record<string, RecruiterAndMitigationState> = Object.fromEntries(
		Object.keys(recruiterNamesAndSlugs).map((recruiter) => [
			recruiter,
			{
				recruiterName: recruiter,
				ticked: false,
				mitigations: Object.fromEntries(
					Object.keys(mitigationNamesAndSlugs).map((mitigation) => [
						mitigation,
						{
							mitigationName: mitigation,
							ticked: false
						}
					])
				)
			}
		])
	);

	function generateSimulateJson() {
		return JSON.stringify({
			candidates_to_generate: candidatesToGenerate,
			train_proportion: trainProportion,
			recruiters: Object.fromEntries(
				Object.values(recruiterStates)
					.filter((recruiterState) => recruiterState.ticked)
					.map((recruiterState) => [
						recruiterNamesAndSlugs[recruiterState.recruiterName],
						['no_mitigation'].concat(
							Object.values(recruiterState.mitigations)
								.filter((mitigationState) => mitigationState.ticked)
								.map((mitigationState) => mitigationNamesAndSlugs[mitigationState.mitigationName])
						)
					])
			),
			protected_characteristic: selectedProtectedCharacteristic
		});
	}
</script>

{#if $modalStore[0]}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
	<div class="flex h-full flex-col items-center justify-center gap-5">
		<div
			transition:fade={{ duration: 400 }}
			on:click|stopPropagation
			role="alertdialog"
			class="view card bg-surface-200-700-token hide-scrollbar flex h-[40rem] max-h-[90vh] w-[50vw] min-w-64 flex-col justify-between overflow-y-scroll rounded-lg p-4 drop-shadow-md"
		>
			<div>
				<ModalDivider />
				<ModalRow center={false}>
					<h3 class="text-center text-2xl font-bold">Run Simulation and Measure Bias</h3>
				</ModalRow>

				<ModalRow center={true}>
					<div class="absolute left-4">
						<InfoHover target="number-of-nodes" />
					</div>
					<h3 class="text-md min-w-[10rem] font-bold">Candidates to Generate:</h3>
					<input
						class="input p-2 rounded-container-token"
						type="number"
						placeholder="Candidates to Generate..."
						bind:value={candidatesToGenerate}
						min={1000}
						max={100_000}
					/>
				</ModalRow>

				<ModalRow center={true} gap={10}>
					<div class="absolute left-4">
						<InfoHover target="number-of-nodes" />
					</div>
					<h3 class="text-md min-w-[10rem] font-bold">Training Proportion:</h3>

					<RangeSlider
						name="range-slider"
						bind:value={trainProportion}
						min={0.1}
						max={0.9}
						step={0.01}
						ticked
						class="w-[250%]"
					></RangeSlider>
					<input
						class="input flex-shrink p-2 rounded-container-token"
						type="number"
						placeholder="Proportion..."
						bind:value={trainProportion}
						min={1000}
						max={10_000_000}
					/>
				</ModalRow>

				<ModalRow>
					<div class="absolute left-4">
						<InfoHover target="number-of-nodes" />
					</div>
					<h3 class="text-md min-w-[10rem] font-bold">Recruiters:</h3>
					<div class="flex-grow"></div>
				</ModalRow>

				<Accordion class="px-8">
					{#each Object.values(recruiterStates) as recruiterAndMitigationState}
						<AccordionItem
							on:click={() => {
								recruiterAndMitigationState.ticked = !recruiterAndMitigationState.ticked;
							}}
						>
							<svelte:fragment slot="summary">
								<div>
									{#if recruiterAndMitigationState.ticked}
										<Check2Square class="inline size-5" />
									{:else}
										<Square class="inline size-5" />
									{/if}
									<h3 class="inline px-2 align-top text-xl font-bold">
										{recruiterAndMitigationState.recruiterName}
									</h3>
								</div>
							</svelte:fragment>
							<svelte:fragment slot="content">
								<div class="flex flex-grow flex-wrap justify-start gap-2">
									{#each Object.values(recruiterAndMitigationState.mitigations) as mitigationState}
										<button
											class="chip {mitigationState.ticked ? 'variant-filled' : 'variant-soft'}"
											on:click={() => {
												mitigationState.ticked = !mitigationState.ticked;
											}}
										>
											{#if mitigationState.ticked}
												<Check2Square class="inline size-4" />
											{:else}
												<Square class="inline size-4" />
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
					<h3 class="text-md min-w-[10rem] font-bold">Protected Characteristic:</h3>

					<select class="select" bind:value={selectedProtectedCharacteristic} required>
						{#each Object.values(network.characteristics) as characteristic}
							<option value={characteristic.name}>{characteristic.name}</option>
						{/each}
					</select>
				</ModalRow>
			</div>

			<footer class="flex justify-end">
				<div class="flex gap-2">
					<button
						class="variant-outline-primary btn"
						on:click={() => {
							modalStore.close();
						}}>Cancel</button
					>
					<button
						class="variant-outline-secondary btn"
						on:click={async () => {
							await awaitSocketClose(simulateSocket);

							simulateSocket = await awaitSocketOpen(
								new WebSocket(`${webSocketUrl}/simulate/?session_key=${$sessionKey}`)
							);

							simulateSocket.send(generateSimulateJson());

							modalStore.close();

							await $deconditionAll();

							await $loadProcess(simulateSocket);
							await $invalidateBias();
							modalStore.trigger(showBiasModal);
						}}
						>Submit
					</button>
				</div>
			</footer>
		</div>
	</div>
{/if}

<ModalPopups />
