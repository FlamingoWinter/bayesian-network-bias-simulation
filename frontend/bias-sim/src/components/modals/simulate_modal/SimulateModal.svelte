{#if $modalStore[0]}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
	<div class="h-full flex flex-col gap-5 justify-center items-center">
		<div transition:fade={{ duration: 400 } } on:click|stopPropagation role="alertdialog"
				 class="card p-4 bg-surface-200-700-token view w-[50vw] min-w-64 h-[40rem] max-h-[90vh] overflow-y-scroll drop-shadow-md rounded-lg flex flex-col justify-between">
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
								 min={1000} max={10_000_000} />
				</ModalRow>

				<ModalRow center={true} gap={10}>
					<div class="absolute left-4">
						<InfoHover target="number-of-nodes" />
					</div>
					<h3 class="text-md font-bold min-w-[10rem]">Training Proportion:</h3>

					<RangeSlider name="range-slider" bind:value={trainProportion} max={1} step={0.01} ticked
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
				{#each chipsets as chipset}
					<p class="pl-12">{chipset.name}:</p>

					<ModalRow>
						<div class="flex justify-start gap-2 flex-grow flex-wrap">

							{#each Object.keys(chipset.chips) as c}
								<button
									class="chip {chipset.chips[c] ? 'variant-filled' : 'variant-soft'}"
									on:click={() => { chipset.chips[c] = !chipset.chips[c]; }}
									on:keypress
								>
									{#if chipset.chips[c]}
										<Check2Square />
									{/if}
									<span class="capitalize">{c}</span>
								</button>
							{/each}
						</div>
					</ModalRow>
					<ModalDivider />
					<hr />
					<ModalDivider />
				{/each}

				<ModalRow center={true}>
					<div class="absolute left-4">
						<InfoHover target="number-of-nodes" />
					</div>
					<h3 class="text-md font-bold min-w-[10rem]">Protected Characteristic:</h3>

					<select class="select" bind:value={selectedProtectedCharacteristic} required>
						{#each Object.values($network.characteristics) as characteristic}
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

	import { awaitSocketClose, awaitSocketOpen } from '../../../utiliites/socket';


	import { getModalStore, type ModalComponent, type ModalSettings, RangeSlider } from '@skeletonlabs/skeleton';
	import ModalPopups from '../../popups/ModalPopups.svelte';
	import Check2Square from 'svelte-bootstrap-icons/lib/Check2Square.svelte';


	import { webSocketUrl } from '../../../utiliites/api';
	import { deconditionAll, invalidateBias, loadProcess } from '../../../stores/functions';
	import { network, sessionKey } from '../../../stores/store';
	import ModalDivider from '../ModalDivider.svelte';
	import ModalRow from '../ModalRow.svelte';
	import InfoHover from '../../popups/InfoHover.svelte';
	import ShowBiasModal from '../show_bias_modal/ShowBiasModal.svelte';

	const modalStore = getModalStore();

	const showBiasModalComponent: ModalComponent = { ref: ShowBiasModal };

	const showBiasModal: ModalSettings = {
		type: 'component',
		component: showBiasModalComponent
	};

	let simulateSocket: WebSocket | undefined = undefined;

	let candidatesToGenerate: number;
	let trainProportion: number = 0.9;
	let selectedProtectedCharacteristic: string;

	const categoricalRecruiters: string[] = [
		'Random Forest',
		'Logistic Regression',
		'One-Hot Encoded Neural Network',
		'Categorical Bayesian Network Approximation'];

	const continuousRecruiters: string[] = [
		'Simple Linear Regression',
		'Polynomial-Featured Linear Regression',
		'Fourier-Featured Linear Regression',
		'Neural Network',
		'Continuous Bayesian Network Approximation',
		'Support Vector Machine'];

	type Chipset = {
		name: string
		chips: Record<string, boolean>
	}

	let noMitigationChips: Chipset = {
		name: 'Without Bias Mitigation',
		chips: {}
	};

	$: if ($network.characteristics[$network.scoreCharacteristic].type == 'categorical') {
		noMitigationChips.chips = categoricalRecruiters.reduce<Record<string, boolean>>(
			(acc, key) => {
				acc[key] = false;
				return acc;
			},
			{}
		);
		updateChipset();
	} else {
		noMitigationChips.chips = categoricalRecruiters.concat(continuousRecruiters).reduce<Record<string, boolean>>(
			(acc, key) => {
				acc[key] = false;
				return acc;
			},
			{}
		);
		updateChipset();
	}

	let chipsets: Chipset[] = [];
	let ensureDemographicParityChipset: Chipset = {
		name: 'Ensure Demographic Parity',
		chips: {}
	};

	let ensureEqualisedOddsChipset: Chipset = {
		name: 'Ensure Equalised Odds',
		chips: {}
	};

	let ensurePredictiveParityChipset: Chipset = {
		name: 'Ensure Predictive Parity',
		chips: {}
	};


	function updateChipset() {
		ensureDemographicParityChipset.chips = { ...noMitigationChips.chips };

		ensureEqualisedOddsChipset.chips = { ...noMitigationChips.chips };
		ensurePredictiveParityChipset.chips = { ...noMitigationChips.chips };
		chipsets = [noMitigationChips, ensureDemographicParityChipset, ensureEqualisedOddsChipset, ensurePredictiveParityChipset];
	}


	function generateSimulateJson() {
		return JSON.stringify({
			'candidates_to_generate': candidatesToGenerate,
			'train_proportion': trainProportion,
			'recruiters': [], // TODO
			'protected_characteristic': selectedProtectedCharacteristic
		});
	}

</script>