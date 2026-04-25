<script lang="ts">
	import { fade } from 'svelte/transition';

	import { biasAnalysis, sessionKey } from '../../../stores/store';

	import { awaitSocketClose, awaitSocketOpen } from '../../../utilities/socket';

	import { getModalStore, RadioGroup, RadioItem } from '@skeletonlabs/skeleton';
	import ModalRow from '../ModalRow.svelte';
	import ModalDivider from '../ModalDivider.svelte';
	import ModalMinMaxAny from '../ModalMinMaxAny.svelte';
	import VariableValueDistributionPieChart, {
		type DataItem
	} from './VariableValueDistributionPieChart.svelte';
	import PInputAndLabel from './PInputAndLabel.svelte';
	import InfoHover from '../../popups/InfoHover.svelte';
	import ModalPopups from '../../popups/ModalPopups.svelte';

	import { webSocketUrl } from '../../../utilities/api';
	import { invalidateNetwork, loadProcess } from '../../../stores/functions';

	const modalStore = getModalStore();

	let generateNetworkSocket: WebSocket | undefined = undefined;

	let randomOrPredefined: 'random' | 'predefined' = 'random';
	let predefinedModel: string = 'sprinkler';

	let numberOfNodes: number;

	let minParents: number;
	let maxParents: number;
	let anyParents: boolean = false;

	let minMutualInformation: number;
	let maxMutualInformation: number;
	let anyMutualInformation: boolean = false;

	let p: DataItem[] = [
		{ name: '2', value: 0.7 },
		{ name: '3', value: 0.25 },
		{ name: '4', value: 0.05 },
		{ name: '5', value: 0 }
	];

	function updateProbabilities(probabilityIndex: number) {
		let difference = 1 - p.reduce((sum, item) => sum + item.value, 0);
		let indexToChange = probabilityIndex == 3 ? 2 : 3;

		if (difference > 0) {
			// Probabilities need to increase
			while (p[indexToChange].value + difference >= 1) {
				difference -= 1 - p[indexToChange].value;
				p[indexToChange].value = 1;
				indexToChange -= 1;
				if (indexToChange == probabilityIndex) {
					indexToChange -= 1;
				}
			}
			p[indexToChange].value += difference;
		} else if (difference < 0) {
			// Probabilities need to decrease
			while (p[indexToChange].value + difference <= 0) {
				difference += p[indexToChange].value;
				p[indexToChange].value = 0;
				indexToChange -= 1;
				if (indexToChange == probabilityIndex) {
					indexToChange -= 1;
				}
			}
			p[indexToChange].value += difference;
		}

		for (let i = 0; i < p.length; i++) {
			p[i].value = Number(p[i].value.toFixed(10));
		}
	}

	function generateCreateNetworkJson() {
		return JSON.stringify({
			random_or_predefined: randomOrPredefined,
			predefined_model: predefinedModel,
			categorical_or_continuous: 'categorical',
			number_of_nodes: numberOfNodes,
			parents_range: [minParents, maxParents],
			mutual_information_range: [minMutualInformation, maxMutualInformation],
			values_per_variable: Object.fromEntries(p.map((item) => [item.name, item.value]))
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
					<h3 class="text-center text-2xl font-bold">New Network</h3>
				</ModalRow>

				<ModalRow center={false}>
					<RadioGroup rounded="rounded-container-token">
						<RadioItem bind:group={randomOrPredefined} name="justify" value={'random'}
							>Random Network
						</RadioItem>
						<RadioItem bind:group={randomOrPredefined} name="justify" value={'predefined'}
							>Predefined Network
						</RadioItem>
					</RadioGroup>
				</ModalRow>

				<ModalDivider />
				<ModalDivider />

				{#if randomOrPredefined === 'random'}
					<div transition:fade={{ duration: 400 }} class="absolute">
						<ModalRow center={true}>
							<div class="absolute -left-0">
								<InfoHover target="number-of-nodes" />
							</div>
							<h3 class="text-md min-w-[10rem] font-bold">Number of Nodes:</h3>
							<input
								class="input p-2 rounded-container-token"
								type="number"
								placeholder="Number of Nodes..."
								bind:value={numberOfNodes}
								min={4}
								max={20}
							/>
						</ModalRow>
						<ModalRow center={false}>
							<div class="absolute -left-0">
								<InfoHover target="allowed-parents" />
							</div>
							<h3 class="text-md min-w-[10rem] font-bold">Allowed Parents:</h3>

							<ModalMinMaxAny
								bind:min={minParents}
								bind:max={maxParents}
								bind:any={anyParents}
								minBound={1}
								maxBound={4}
							/>
						</ModalRow>
						<ModalDivider />
						<hr />
						<ModalDivider />

						<div>
							<ModalRow center={false}>
								<div class="absolute -left-0">
									<InfoHover target="allowed-mutual-information" />
								</div>
								<div class="w-[10rem]">
									<h3 class="text-md w-[8rem] font-bold">Allowed Mutual Information:</h3>
								</div>
								<ModalMinMaxAny
									bind:min={minMutualInformation}
									bind:max={maxMutualInformation}
									bind:any={anyMutualInformation}
									minBound={0.1}
									maxBound={0.9}
									step={0.01}
								/>
							</ModalRow>

							<ModalRow center={false}>
								<div class="absolute -left-0">
									<InfoHover target="values-per-variable" />
								</div>
								<div class="w-[10rem]">
									<h3 class="text-md w-[12rem] font-bold">Values per Variable (Probabilities):</h3>
								</div>

								<div class="flex gap-4">
									{#each p as probability, i}
										<PInputAndLabel
											onChange={() => {
												updateProbabilities(i);
											}}
											bind:p={probability.value}
											label={probability.name}
										/>
									{/each}
								</div>

								<VariableValueDistributionPieChart data={p} />
							</ModalRow>
						</div>
					</div>
				{:else}
					<div transition:fade={{ duration: 400 }} class="absolute left-0 px-14">
						<RadioGroup rounded="rounded-container-token">
							<div class="flex flex-wrap gap-2">
								<RadioItem bind:group={predefinedModel} name="justify" value={'sprinkler'}
									>Sprinkler Network
								</RadioItem>
								<RadioItem bind:group={predefinedModel} name="justify" value={'shark_sighting'}
									>Shark Sightings Network
								</RadioItem>
							</div>
						</RadioGroup>
					</div>
				{/if}
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
							await awaitSocketClose(generateNetworkSocket);

							generateNetworkSocket = await awaitSocketOpen(
								new WebSocket(`${webSocketUrl}/generate-random-network/?session_key=${$sessionKey}`)
							);
							modalStore.close();

							const jsonMessage = generateCreateNetworkJson();
							generateNetworkSocket.send(jsonMessage);

							await $loadProcess(generateNetworkSocket);
							await $invalidateNetwork();
							$biasAnalysis = undefined;
						}}
						>Submit
					</button>
				</div>
			</footer>
		</div>
	</div>
{/if}

<ModalPopups />
