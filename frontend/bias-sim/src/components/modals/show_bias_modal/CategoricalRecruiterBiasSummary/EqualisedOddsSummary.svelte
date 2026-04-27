<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import BiasTitle from '../BiasTitle.svelte';
	import {
		absoluteDisparityToLevel,
		type MitigationAnalysis,
		minMaxGroups
	} from '../../../../types/Bias';
	import { levelToColorMapping } from '../../../../types/Bias.js';

	export let recruiter: MitigationAnalysis;
	export let withoutMitigation: MitigationAnalysis | null;

	$: fnr = minMaxGroups(recruiter.byGroup, 'falseNegativeRate');
	$: absoluteFNRDisparity = fnr.maxVal - fnr.minVal;
	$: fnrBiasLevel = absoluteDisparityToLevel(absoluteFNRDisparity);

	$: fpr = minMaxGroups(recruiter.byGroup, 'falsePositiveRate');
	$: absoluteFPRDisparity = fpr.maxVal - fpr.minVal;
	$: fprBiasLevel = absoluteDisparityToLevel(absoluteFPRDisparity);
</script>

<AccordionItem>
	<svelte:fragment slot="summary">
		<BiasTitle subtitle="Separation">Equalised Odds</BiasTitle>
	</svelte:fragment>
	<svelte:fragment slot="content">
		<div class="py-4">
			<p class=" text-center">
				A random competent person from group {fnr.max} has a
				<span class="center block text-2xl font-bold">
					{(fnr.maxVal * 100).toFixed(1)}%
				</span>
				chance of being rejected, while a random competent person from group {fnr.min}
				only has a
				<span class="center block text-2xl font-bold">
					{(fnr.minVal * 100).toFixed(1)}%
				</span>
				chance of being rejected
			</p>
			<p class="mt-4 text-center">
				This is an absolute difference of
				<span
					style="color: {levelToColorMapping[fnrBiasLevel]}"
					class="center block text-3xl font-bold"
				>
					{(absoluteFNRDisparity * 100).toFixed(1)}
				</span>
			</p>
			<p class="mt-8 text-center">
				By this metric, there is a <span
					style="color: {levelToColorMapping[fnrBiasLevel]}"
					class="text-lg font-bold">{fnrBiasLevel}</span
				>
				bias against group {fnr.max}
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
									<th>False Negative Rate</th>
									<th>Proportion Competent</th>
								</tr>
							</thead>
							<tbody>
								{#each Object.keys(recruiter.byGroup) as group}
									<tr>
										<td>{group}</td>
										{#if withoutMitigation === null}
											<td class="font-bold"
												>{recruiter.byGroup[group].falseNegativeRate.toFixed(3)}</td
											>
										{:else}
											<td>
												<span class="font-bold"
													>{recruiter.byGroup[group].falseNegativeRate.toFixed(3)}</span
												>
												<span class="text-xs"
													>({withoutMitigation.byGroup[group].falseNegativeRate.toFixed(3)})</span
												>
											</td>
										{/if}
										<td>{recruiter.byGroup[group].competentRate.toFixed(3)}</td>
									</tr>
								{/each}
							</tbody>
						</table>
						{#if withoutMitigation !== null}
							<p class="py-2 text-xs">
								* Bracketed values are from the model without the mitigation applied.
							</p>
						{/if}
					</div>
				</svelte:fragment>
			</AccordionItem>
		</Accordion>

		<hr />
		<div class="py-4">
			<p class=" text-center">
				A random person from group {fpr.min} who isn't competent has a
				<span class="center block text-2xl font-bold">
					{(fpr.minVal * 100).toFixed(1)}%
				</span>
				chance of being hired mistakenly, while a random person from group {fpr.max}
				who isn't competent has a
				<span class="center block text-2xl font-bold">
					{(fpr.maxVal * 100).toFixed(1)}%
				</span>
				chance of being hired mistakenly
			</p>
			<p class="mt-4 text-center">
				This is an absolute difference of
				<span
					style="color: {levelToColorMapping[fprBiasLevel]}"
					class="center block text-3xl font-bold"
				>
					{(absoluteFPRDisparity * 100).toFixed(1)}
				</span>
			</p>
			<p class="mt-8 text-center">
				By this metric, there is a <span
					style="color: {levelToColorMapping[fprBiasLevel]}"
					class="text-lg font-bold">{fprBiasLevel}</span
				>
				bias against group {fpr.min}
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
									<th>False Positive Rate</th>
									<th>Proportion Not Competent</th>
								</tr>
							</thead>
							<tbody>
								{#each Object.keys(recruiter.byGroup) as group}
									<tr>
										<td>{group}</td>
										{#if withoutMitigation === null}
											<td class="font-bold"
												>{recruiter.byGroup[group].falsePositiveRate.toFixed(3)}</td
											>
										{:else}
											<td>
												<span class="font-bold"
													>{recruiter.byGroup[group].falsePositiveRate.toFixed(3)}</span
												>
												<span class="text-xs"
													>{withoutMitigation.byGroup[group].falsePositiveRate.toFixed(3)}</span
												>
											</td>
										{/if}
										<td>{recruiter.byGroup[group].notCompetentRate.toFixed(3)}</td>
									</tr>
								{/each}
							</tbody>
						</table>
						{#if withoutMitigation !== null}
							<p class="py-2 text-xs">
								* Bracketed values are from the model without the mitigation applied.
							</p>
						{/if}
					</div>
				</svelte:fragment>
			</AccordionItem>
		</Accordion>
	</svelte:fragment>
</AccordionItem>
