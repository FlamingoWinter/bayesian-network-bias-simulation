<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import BiasSubTitle from '../BiasSubTitle.svelte';
	import BiasTitle from '../BiasTitle.svelte';
	import { type MitigationBiasAnalysis, multiplierToLevel } from '../../../../types/Bias';
	import { levelToColorMapping } from '../../../../types/Bias.js';

	export let recruiter: MitigationBiasAnalysis;
	export let withoutMitigation: MitigationBiasAnalysis | null;

	$: minAndMaxHiredRates = Object.entries(recruiter.byGroup).reduce(
		(acc, [groupName, info]) => {
			if (info.hiredRate > acc.maxHiredRate) {
				acc.max = groupName;
				acc.maxHiredRate = info.hiredRate;
			}
			if (info.hiredRate < acc.minHiredRate) {
				acc.min = groupName;
				acc.minHiredRate = info.hiredRate;
			}
			return acc;
		},
		{ min: '', max: '', minHiredRate: 1, maxHiredRate: 0 }
	);

	$: disparity = minAndMaxHiredRates.maxHiredRate / minAndMaxHiredRates.minHiredRate;
	$: biasLevel = multiplierToLevel(disparity);


</script>

<AccordionItem>
	<svelte:fragment slot="summary">
		<BiasTitle subtitle="Independence">Demographic Parity</BiasTitle>
	</svelte:fragment>
	<svelte:fragment slot="content">
		<div class="py-4">
				<p class=" text-center">
					A random person from group {minAndMaxHiredRates.max} is
					<span style="color: {levelToColorMapping[biasLevel]}" class="font-bold block center text-3xl">
						{disparity.toFixed(3)}x
					</span>
					as likely to be hired as a random person
					from group {minAndMaxHiredRates.min}
				</p>
				<p class="mt-8 text-center">By this metric, there is a <span
					style="color: {levelToColorMapping[biasLevel]}"
					class="font-bold text-lg">{biasLevel}</span> bias
					against group {minAndMaxHiredRates.min},
				</p>

				<p class=" text-center">
					on the condition that the chance of both groups obtaining the job should be equal
				</p>
			</div>


		<Accordion spacing="0">
			<AccordionItem>
				<svelte:fragment slot="summary">
					<h2 class="font-bold">More Information</h2>

				</svelte:fragment>
				<svelte:fragment slot="content">
					<div class="table-container">
						<table class="table table-hover">
							<thead>
							<tr>
								<th>Group</th>
								<th>Proportion Hired</th>
								<th>Proportion Competent</th>
							</tr>
							</thead>
							<tbody>
							{#each Object.keys(recruiter.byGroup) as group}
								<tr>
									<td>{group}</td>
									{#if withoutMitigation === null}
																				<td><span class="font-bold">
																					{recruiter.byGroup[group].hiredRate.toFixed(3)}
																				</span></td>

									{:else}
										<td>
											<span class="font-bold">{recruiter.byGroup[group].hiredRate.toFixed(3)}</span>
											<span class="text-xs">{withoutMitigation.byGroup[group].hiredRate.toFixed(3)}</span>
										</td>
									{/if}
									<td>{recruiter.byGroup[group].competentRate.toFixed(3)}</td>
								</tr>
							{/each}
							</tbody>
						</table>
						{#if withoutMitigation !== null}
							<p class="text-xs py-2">* Bracketed values are from the model without the mitigation applied.</p>
						{/if}
					</div>
				</svelte:fragment>
			</AccordionItem>
					</Accordion>


	</svelte:fragment>
</AccordionItem>