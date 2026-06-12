<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import BiasTitle from '../BiasTitle.svelte';
	import { type MitigationAnalysis, multiplierToLevel, minMaxGroups } from '../../../../types/Bias';
	import { levelToColorMapping } from '../../../../types/Bias.js';

	export let recruiter: MitigationAnalysis;
	export let withoutMitigation: MitigationAnalysis | null;

	$: hired = minMaxGroups(recruiter.byGroup, 'hiredRate');
	$: disparity = hired.maxVal / hired.minVal;
	$: biasLevel = multiplierToLevel(disparity);
</script>

<AccordionItem>
	<svelte:fragment slot="summary">
		<BiasTitle subtitle="Independence">Demographic Parity</BiasTitle>
	</svelte:fragment>
	<svelte:fragment slot="content">
		<div class="py-4">
			<p class=" text-center">
				A random person from group {hired.max} is
				<span
					style="color: {levelToColorMapping[biasLevel]}"
					class="center block text-3xl font-bold"
				>
					{disparity.toFixed(3)}x
				</span>
				as likely to be hired as a random person from group {hired.min}
			</p>
			<p class="mt-8 text-center">
				By this metric, there is a <span
					style="color: {levelToColorMapping[biasLevel]}"
					class="text-lg font-bold">{biasLevel}</span
				>
				bias against group {hired.min},
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
											<td
												><span class="font-bold">
													{recruiter.byGroup[group].hiredRate.toFixed(3)}
												</span></td
											>
										{:else}
											<td>
												<span class="font-bold"
													>{recruiter.byGroup[group].hiredRate.toFixed(3)}</span
												>
												<span class="text-xs"
													>{withoutMitigation.byGroup[group].hiredRate.toFixed(3)}</span
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
	</svelte:fragment>
</AccordionItem>
