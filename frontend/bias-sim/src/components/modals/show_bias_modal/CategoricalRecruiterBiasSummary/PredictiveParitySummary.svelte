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

	$: fdr = minMaxGroups(recruiter.byGroup, 'falseDiscoveryRate');
	$: absoluteFDRDisparity = fdr.maxVal - fdr.minVal;
	$: fdrBiasLevel = absoluteDisparityToLevel(absoluteFDRDisparity);

	$: omission = minMaxGroups(recruiter.byGroup, 'falseOmissionRate');
	$: absoluteFORDisparity = omission.maxVal - omission.minVal;
	$: forBiasLevel = absoluteDisparityToLevel(absoluteFORDisparity);
</script>

<AccordionItem>
	<svelte:fragment slot="summary">
		<BiasTitle subtitle="Sufficiency">Predictive Parity</BiasTitle>
	</svelte:fragment>
	<svelte:fragment slot="content">
		<div class="py-4">
			<p class=" text-center">
				<span class="center block text-2xl font-bold">
					{((1 - fdr.maxVal) * 100).toFixed(1)}%
				</span>
				of the people hired from group {fdr.max} are competent, while
				<span class="center block text-2xl font-bold">
					{((1 - fdr.minVal) * 100).toFixed(1)}%
				</span>
				of people hired from group {fdr.min} are competent.
			</p>
			<p class="mt-4 text-center">
				This is an absolute difference of
				<span
					style="color: {levelToColorMapping[fdrBiasLevel]}"
					class="center block text-3xl font-bold"
				>
					{(absoluteFDRDisparity * 100).toFixed(1)}
				</span>
			</p>
			<p class="mt-8 text-center">
				By this metric, there is a <span
					style="color: {levelToColorMapping[fdrBiasLevel]}"
					class="text-lg font-bold">{fdrBiasLevel}</span
				>
				bias against group {fdr.min}
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
									<th>False Discovery Rate</th>

									<th>Proportion Hired</th>
								</tr>
							</thead>
							<tbody>
								{#each Object.keys(recruiter.byGroup) as group}
									<tr>
										<td>{group}</td>
										{#if withoutMitigation === null}
											<td class="font-bold"
												>{recruiter.byGroup[group].falseDiscoveryRate.toFixed(3)}</td
											>
										{:else}
											<td>
												<span class="font-bold"
													>{recruiter.byGroup[group].falseDiscoveryRate.toFixed(3)}</span
												>
												<span class="text-xs"
													>{withoutMitigation.byGroup[group].falseDiscoveryRate.toFixed(3)}</span
												>
											</td>
										{/if}
										<td>{recruiter.byGroup[group].hiredRate.toFixed(3)}</td>
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
				<span class="center block text-2xl font-bold">
					{(omission.minVal * 100).toFixed(1)}%
				</span>
				of people rejected from group {omission.min} were actually competent while
				<span class="center block text-2xl font-bold">
					{(omission.maxVal * 100).toFixed(1)}%
				</span>
				of people rejected from group {omission.max} were actually competent.
			</p>
			<p class="mt-4 text-center">
				This is an absolute difference of
				<span
					style="color: {levelToColorMapping[forBiasLevel]}"
					class="center block text-3xl font-bold"
				>
					{(absoluteFORDisparity * 100).toFixed(1)}
				</span>
			</p>
			<p class="mt-8 text-center">
				By this metric, there is a <span
					style="color: {levelToColorMapping[forBiasLevel]}"
					class="text-lg font-bold">{forBiasLevel}</span
				>
				bias against group {omission.max}
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
									<th>False Omission Rate</th>
									<th>Proportion Rejected</th>
								</tr>
							</thead>
							<tbody>
								{#each Object.keys(recruiter.byGroup) as group}
									<tr>
										<td>{group}</td>
										{#if withoutMitigation === null}
											<td class="font-bold"
												>{recruiter.byGroup[group].falseOmissionRate.toFixed(3)}</td
											>
										{:else}
											<td>
												<span class="font-bold"
													>{recruiter.byGroup[group].falseOmissionRate.toFixed(3)}</span
												>
												<span class="text-xs"
													>{withoutMitigation.byGroup[group].falseOmissionRate.toFixed(3)}</span
												>
											</td>
										{/if}
										<td>{recruiter.byGroup[group].notHiredRate.toFixed(3)}</td>
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
