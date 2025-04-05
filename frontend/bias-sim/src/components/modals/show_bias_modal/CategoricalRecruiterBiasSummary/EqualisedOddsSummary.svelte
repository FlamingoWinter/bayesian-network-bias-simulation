<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import BiasSubTitle from '../BiasSubTitle.svelte';
	import BiasTitle from '../BiasTitle.svelte';
	import {
		absoluteDisparityToLevel,
		type MitigationBiasAnalysis,
		multiplierToLevel
	} from '../../../../types/Bias';
	import { levelToColorMapping } from '../../../../types/Bias.js';

	export let recruiter: MitigationBiasAnalysis;
		export let withoutMitigation: MitigationBiasAnalysis | null;



	$: minAndMaxFalseNegativeRates = Object.entries(recruiter.byGroup).reduce(
		(acc, [groupName, info]) => {
			if (info.falseNegativeRate > acc.maxFalseNegativeRate) {
				acc.max = groupName;
				acc.maxFalseNegativeRate = info.falseNegativeRate;
			}
			if (info.falseNegativeRate < acc.minFalseNegativeRate) {
				acc.min = groupName;
				acc.minFalseNegativeRate = info.falseNegativeRate;
			}
			return acc;
		},
		{ min: '', max: '', minFalseNegativeRate: 1, maxFalseNegativeRate: 0 }
	);

	$: absoluteFalseNegativeRateDisparity = minAndMaxFalseNegativeRates.maxFalseNegativeRate - minAndMaxFalseNegativeRates.minFalseNegativeRate;
	$: falseNegativeBiasLevel = absoluteDisparityToLevel(absoluteFalseNegativeRateDisparity);

	$: minAndMaxFalsePositiveRates = Object.entries(recruiter.byGroup).reduce(
		(acc, [groupName, info]) => {
			if (info.falsePositiveRate > acc.maxFalsePositiveRate) {
				acc.max = groupName;
				acc.maxFalsePositiveRate = info.falsePositiveRate;
			}
			if (info.falsePositiveRate < acc.minFalsePositiveRate) {
				acc.min = groupName;
				acc.minFalsePositiveRate = info.falsePositiveRate;
			}
			return acc;
		},
		{ min: '', max: '', minFalsePositiveRate: 1, maxFalsePositiveRate: 0 }
	);

	$: absoluteFalsePositiveRateDisparity = minAndMaxFalsePositiveRates.maxFalsePositiveRate - minAndMaxFalsePositiveRates.minFalsePositiveRate;
	$: falsePositiveBiasLevel = absoluteDisparityToLevel(absoluteFalsePositiveRateDisparity);


</script>

<AccordionItem>
	<svelte:fragment slot="summary">
		<BiasTitle subtitle="Separation">Equalised Odds</BiasTitle>
	</svelte:fragment>
	<svelte:fragment slot="content">

			<div class="py-4">
				<p class=" text-center">
					A random competent person from group {minAndMaxFalseNegativeRates.max} has a
					<span class="font-bold block center text-2xl">
						{(minAndMaxFalseNegativeRates.maxFalseNegativeRate * 100).toFixed(1)}%
					</span>
					chance of being rejected, while a random competent person from group {minAndMaxFalseNegativeRates.min} only has a
					<span  class="font-bold block center text-2xl">
						{(minAndMaxFalseNegativeRates.minFalseNegativeRate * 100).toFixed(1)}%
					</span>
					chance of being rejected
				</p>
				<p class="mt-4 text-center">
					This is an absolute difference of
					<span style="color: {levelToColorMapping[falseNegativeBiasLevel]}" class="font-bold block center text-3xl">
						{(absoluteFalseNegativeRateDisparity * 100).toFixed(1)}
					</span>
				</p>
				<p class="mt-8 text-center">By this metric, there is a <span
					style="color: {levelToColorMapping[falseNegativeBiasLevel]}"
					class="font-bold text-lg">{falseNegativeBiasLevel}</span> bias
					against group {minAndMaxFalseNegativeRates.max}</p>
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
									<th>False Negative Rate</th>
									<th>Proportion Competent</th>
								</tr>
								</thead>
								<tbody>
								{#each Object.keys(recruiter.byGroup) as group}
									<tr>
										<td>{group}</td>
										<td>{group}</td>
									{#if withoutMitigation === null}
																														<td class="font-bold">{recruiter.byGroup[group].falseNegativeRate.toFixed(3)}</td>


									{:else}
										<td>
											<span class="font-bold">{recruiter.byGroup[group].falseNegativeRate.toFixed(3)}</span>
											<span class="text-xs">({withoutMitigation.byGroup[group].falseNegativeRate.toFixed(3)})</span>
										</td>
									{/if}
										<td class="font-bold">{recruiter.byGroup[group].falseNegativeRate.toFixed(3)}</td>
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

			<hr />
			<div class="py-4">
				<p class=" text-center">
					A random person from group {minAndMaxFalsePositiveRates.min} who isn't competent has a
					<span class="font-bold block center text-2xl">
						{(minAndMaxFalsePositiveRates.minFalsePositiveRate * 100).toFixed(1)}%
					</span>
					chance of being hired mistakenly,
					while a random person from group {minAndMaxFalsePositiveRates.max} who isn't competent has a
					<span  class="font-bold block center text-2xl">
						{(minAndMaxFalsePositiveRates.maxFalsePositiveRate * 100).toFixed(1)}%
					</span>
					chance of being hired mistakenly
				</p>
				<p class="mt-4 text-center">
					This is an absolute difference of
					<span style="color: {levelToColorMapping[falsePositiveBiasLevel]}" class="font-bold block center text-3xl">
						{(absoluteFalsePositiveRateDisparity * 100).toFixed(1)}
					</span>
				</p>
				<p class="mt-8 text-center">By this metric, there is a <span
					style="color: {levelToColorMapping[falsePositiveBiasLevel]}"
					class="font-bold text-lg">{falsePositiveBiasLevel}</span> bias
					against group {minAndMaxFalsePositiveRates.min}</p>
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
									<th>False Positive Rate</th>
									<th>Proportion Not Competent</th>
								</tr>
								</thead>
								<tbody>
								{#each Object.keys(recruiter.byGroup) as group}
									<tr>
										<td>{group}</td>
										{#if withoutMitigation === null}
											<td class="font-bold">{recruiter.byGroup[group].falsePositiveRate.toFixed(3)}</td>
									{:else}
										<td>
											<span class="font-bold">{recruiter.byGroup[group].falsePositiveRate.toFixed(3)}</span>
											<span class="text-xs">{withoutMitigation.byGroup[group].falsePositiveRate.toFixed(3)}</span>
										</td>
									{/if}
										<td class="font-bold">{recruiter.byGroup[group].falsePositiveRate.toFixed(3)}</td>
										<td>{recruiter.byGroup[group].notCompetentRate.toFixed(3)}</td>
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