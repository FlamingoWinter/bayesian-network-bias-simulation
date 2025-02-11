<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import BiasSubTitle from '../BiasSubTitle.svelte';
	import BiasTitle from '../BiasTitle.svelte';
	import {
		absoluteDisparityToLevel,
		type CategoricalRecruiterBiasAnalysis,
		multiplierToLevel
	} from '../../../../types/Bias';
	import { levelToColorMapping } from '../../../../types/Bias.js';

	export let recruiter: CategoricalRecruiterBiasAnalysis;

	$: minAndMaxFalseDiscoveryRates = Object.entries(recruiter.byGroup).reduce(
		(acc, [groupName, info]) => {
			if (info.falseDiscoveryRate > acc.maxFalseDiscoveryRate) {
				acc.max = groupName;
				acc.maxFalseDiscoveryRate = info.falseDiscoveryRate;
			}
			if (info.falseDiscoveryRate < acc.minFalseDiscoveryRate) {
				acc.min = groupName;
				acc.minFalseDiscoveryRate = info.falseDiscoveryRate;
			}
			return acc;
		},
		{ min: '', max: '', minFalseDiscoveryRate: 1, maxFalseDiscoveryRate: 0 }
	);

	$: absoluteFalseDiscoveryRateDisparity = minAndMaxFalseDiscoveryRates.maxFalseDiscoveryRate - minAndMaxFalseDiscoveryRates.minFalseDiscoveryRate;
	$: falseDiscoveryBiasLevel = absoluteDisparityToLevel(absoluteFalseOmissionRateDisparity);

	$: minAndMaxFalseOmissionRates = Object.entries(recruiter.byGroup).reduce(
		(acc, [groupName, info]) => {
			if (info.falseOmissionRate > acc.maxFalseOmissionRate) {
				acc.max = groupName;
				acc.maxFalseOmissionRate = info.falseOmissionRate;
			}
			if (info.falseOmissionRate < acc.minFalseOmissionRate) {
				acc.min = groupName;
				acc.minFalseOmissionRate = info.falseOmissionRate;
			}
			return acc;
		},
		{ min: '', max: '', minFalseOmissionRate: 1, maxFalseOmissionRate: 0 }
	);

	$: absoluteFalseOmissionRateDisparity = minAndMaxFalseOmissionRates.maxFalseOmissionRate - minAndMaxFalseOmissionRates.minFalseOmissionRate;
	$: falseOmissionBiasLevel = absoluteDisparityToLevel(absoluteFalseOmissionRateDisparity);


</script>

<AccordionItem>
	<svelte:fragment slot="summary">
		<BiasTitle subtitle="Sufficiency">Predictive Parity</BiasTitle>
	</svelte:fragment>
	<svelte:fragment slot="content">

			<div class="py-4">
				<p class=" text-center">
					<span class="font-bold block center text-2xl">
						{((1- minAndMaxFalseDiscoveryRates.maxFalseDiscoveryRate) * 100).toFixed(1)}%
					</span>
					of the people hired from group {minAndMaxFalseDiscoveryRates.max} are competent, while
					<span  class="font-bold block center text-2xl">
						{((1-minAndMaxFalseDiscoveryRates.minFalseDiscoveryRate) * 100).toFixed(1)}%
					</span>
					of people hired from group {minAndMaxFalseDiscoveryRates.min} are competent.
				</p>
				<p class="mt-4 text-center">
					This is an absolute difference of
					<span style="color: {levelToColorMapping[falseDiscoveryBiasLevel]}" class="font-bold block center text-3xl">
						{(absoluteFalseDiscoveryRateDisparity * 100).toFixed(1)}
					</span>
				</p>
				<p class="mt-8 text-center">By this metric, there is a <span
					style="color: {levelToColorMapping[falseDiscoveryBiasLevel]}"
					class="font-bold text-lg">{falseDiscoveryBiasLevel}</span> bias
					against group {minAndMaxFalseDiscoveryRates.min}</p>
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
									<th>False Discovery Rate</th>
									<th>Proportion Hired</th>
								</tr>
								</thead>
								<tbody>
								{#each Object.keys(recruiter.byGroup) as group}
									<tr>
										<td>{group}</td>
										<td class="font-bold">{recruiter.byGroup[group].falseDiscoveryRate.toFixed(3)}</td>
										<td>{recruiter.byGroup[group].hiredRate.toFixed(3)}</td>
									</tr>
								{/each}
								</tbody>
							</table>
						</div>
					</svelte:fragment>
				</AccordionItem>
			</Accordion>

			<hr />
			<div class="py-4">
				<p class=" text-center">
					<span class="font-bold block center text-2xl">
						{(minAndMaxFalseOmissionRates.minFalseOmissionRate * 100).toFixed(1)}%
					</span>
					of people rejected from group {minAndMaxFalseOmissionRates.min} were actually competent while
					<span  class="font-bold block center text-2xl">
						{(minAndMaxFalseOmissionRates.maxFalseOmissionRate * 100).toFixed(1)}%
					</span>
					of people rejected from group {minAndMaxFalseOmissionRates.max} were actually competent.
				</p>
				<p class="mt-4 text-center">
					This is an absolute difference of
					<span style="color: {levelToColorMapping[falseOmissionBiasLevel]}" class="font-bold block center text-3xl">
						{(absoluteFalseOmissionRateDisparity * 100).toFixed(1)}
					</span>
				</p>
				<p class="mt-8 text-center">By this metric, there is a <span
					style="color: {levelToColorMapping[falseOmissionBiasLevel]}"
					class="font-bold text-lg">{falseOmissionBiasLevel}</span> bias
					against group {minAndMaxFalseOmissionRates.max}</p>
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
									<th>False Omission Rate</th>
									<th>Proportion Rejected</th>
								</tr>
								</thead>
								<tbody>
								{#each Object.keys(recruiter.byGroup) as group}
									<tr>
										<td>{group}</td>
										<td class="font-bold">{recruiter.byGroup[group].falseOmissionRate.toFixed(3)}</td>
										<td>{recruiter.byGroup[group].notHiredRate.toFixed(3)}</td>
									</tr>
								{/each}
								</tbody>
							</table>
						</div>
					</svelte:fragment>
				</AccordionItem>
			</Accordion>

	</svelte:fragment>
</AccordionItem>