<script lang="ts">
	import { Accordion, AccordionItem, Tab, TabGroup } from '@skeletonlabs/skeleton';

	const biasMetrics: string[] = [
		'FNR Difference',
		'FPR Difference',
		'FOR Difference',
		'FDR Difference'
	];

	const biasMetricsAndDem: string[] =
		[
			'FNR Difference',
			'FPR Difference',
			'Demographic Parity',
			'FOR Difference',
			'FDR Difference'
		];

	let tabSet1: string = 'FNR Difference';
	let tabSet2: string = 'FNR Difference';
	let tabSet3: string = 'FNR Difference';
	let tabSet4: string = 'FPR Difference';
	let tabSet5: string = 'FNR Difference';
	let tabSet6: string = 'FPR Difference';
	let tabSet7: string = 'FNR Difference';
	let tabSet8: string = 'FNR Difference';
	let tabSet9: string = 'FNR Difference';
	let tabSet10: string = 'FNR Difference';
	let tabSet11: string = 'FNR Difference';
	let tabSet12: string = 'FNR Difference';
	let tabSet13: string = 'FNR Difference';


</script>

<h3 class="text-6xl font-bold mt-2 p-8">
	The Results
</h3>
<div class="flex justify-center pt-10 pb-10 text-center">
	<div class="text-lg max-w-[40rem] flex flex-col items-center">
		<p>
			At the very start of this walkthrough, we presented some findings under "sensible assumptions".
		</p>
		<p class="mt-16">
			Those assumptions are:
		</p>
		<div class="text-left p-4  card rounded-4 drop-shadow-xl mt-8">
			<Accordion autocollapse>
				<AccordionItem open>
					<svelte:fragment slot="summary"><span class="font-bold text-xl">
						1) Applicant Distributions are Bayesian Networks
					</span></svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4 text-sm">
							<p>
								Applicants are expected to follow the distribution of our simulated <span
								class="text-surface-600 font-bold">Bayesian Networks</span>.
							</p>
							<p class="mt-4">
								Learning about some
								characteristic of an applicant gives us information about every other characteristic of the applicant.
							</p>
							<p class="mt-4">
								(There are significant further implications to this which we discuss in TODO
							</p>
						</div>

					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-xl">2) Applicants don't Lie</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4 text-sm">
							<p>
								Applicant's don't lie in their applications or omit information,
								or them doing this doesn't significantly affect the
								scenario
								to invalidate these results.
							</p>
						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-xl">3) Recruiters have Perfect Training Data</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4 text-sm">
							<p>
								Recruiters train on randomly selected applicants and are given accurate measures of
								each applicant's competence.
							</p>
							<p class="mt-4">
								In reality, we know this is not true: training datasets are likely to contain their own bias.
							</p>
							<p class="mt-4">
								But we can assume that this training bias is unlikely to exactly counteract the inherent bias
								within the process.
							</p>
						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-xl">4) Equalised Odds <i>is</i> Unbiasedness</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4 text-sm">

							<p>
								<span class="text-surface-600 font-bold">Equalised Odds</span> (that equally competent candidates
								receive the same treatment) is a valid definition of
								"unbiasedness" within recruiting.
							</p>
							<p class="mt-4">
								<span class="text-emerald-700 font-bold">FNR Difference</span> and
								<span class="text-cyan-800 font-bold">FPR Difference</span> are valid measures of bias.
							</p>
						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-xl">5) Predictive Parity is the <i>Appearance</i> of Unbiasedness </span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4 text-sm">

							<p>
								<span class="text-surface-600 font-bold">Predictive Parity</span> (that there are no differences in the
								average competence of hired candidates across
								groups,
								or rejected candidates across groups) is a valid definition of "the
								external appearance of unbiasedness".
							</p>
							<p class="mt-4">
								<span class="text-purple-700 font-bold">FOR Difference</span> and
								<span class="text-yellow-700 font-bold">FDR Difference</span> are valid measures for the external
								appearance of
								bias.
							</p>
						</div>
					</svelte:fragment>
				</AccordionItem>

			</Accordion>
		</div>

		<p class="mt-16">
			This is how we justify each of the findings we gave:
		</p>

		<div class="text-left p-4  card rounded-4 drop-shadow-xl mt-16 text-base min-w-[56rem]">
			<Accordion>
				<AccordionItem>
					<svelte:fragment slot="summary"><span class="font-bold text-2xl">1) Bias is Common</span></svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-12">
							<p class="text-center font-semibold">
								"Bias is likely to exist in <i>any</i> machine learning process, even when input data is completely
								unbiased,
								and bias isn't introduced in other areas of the process."
							</p>
							<p class="mt-16">
								Across all recruiters and conditions, each bias metric is unlikely to show low values.
							</p>
							<p class="mt-16">
								On average, the <span class="text-emerald-700 font-bold">FNR Difference</span> and
								<span class="text-cyan-800 font-bold">FPR Difference</span> is about <span
								class="text-surface-600 font-bold">20%</span>.
							</p>
							<p class="mt-4">
								That means we can expect 20% of the competent candidates from the disfavoured group to be rejected,
								such that this wouldn't have happened if they were in the other group.
							</p>
							<p class="mt-4">
								And we can expect 20% of the non-competent candidates from the favoured group to be accepted,
								such that this wouldn't have happened if they were in the other group.
							</p>
							<p class="mt-16">
								On average, the <span class="text-purple-700 font-bold">FOR Difference</span>, and
								<span class="text-yellow-700 font-bold">FDR Difference</span> is about <span
								class="text-surface-600 font-bold">15%</span>.
							</p>
							<p class="mt-4">
								That means we can expect a difference of 15 percentage points
								in the proportions of hired candidates who aren't competent across groups, and a similar
								difference in the proportion of rejected candidates who are.
							</p>
							<p class="mt-16">
								We might think this is due to high FNR, FPR, FOR, and FDR in general.
								The average recruiter isn't particularly accurate (the average accuracy was about 78%).
							</p>
							<p class="mt-8">
								But even if we only consider the accurate recruiters (with accuracy >95%),
								the average bias displayed by these metrics
								is <span
								class="text-surface-600 font-bold">Above 10%</span>:
							</p>
							<p class="mt-2">
								Only about <span
								class="text-surface-600 font-bold">25%</span> of those accurate recruiters display an FPR or FNR
								Difference
								<span class="text-surface-600 font-bold">below 2%</span>.
							</p>
							<p class="mt-2">
								Only about <span class="text-surface-600 font-bold">30%</span> of those accurate recruiters display an
								FDR or FOR Difference
								<span class="text-surface-600 font-bold">below 2%</span>.
							</p>
							<p class="mt-16">
								We can visualise how much bias each of our recruiters shows using a <span
								class="text-surface-600 font-bold">Histogram</span>.

							</p>
							<p class="mt-4">
								Each bar shows how many recruiters fall into a certain range of bias.
								We've adjusted the metrics such that positive values represent bias in favour of the more competent
								group.
							</p>
							<p class="mt-4">
								The further to the right a bar is, the more bias in favour of the more competent group it represents.
								The further to the left, the more bias against that group it represents.
							</p>
							<TabGroup class="px-8 flex-grow mt-8" justify="flex-wrap">
								{#each biasMetrics as tabName}
									<Tab bind:group={tabSet1} name="{tabName}" value={tabName}>
										{tabName}
									</Tab>
								{/each}
								<svelte:fragment slot="panel">
									<div class="{tabSet1 === 'FNR Difference' ? '' : 'hidden'}">
										<img src="/results/fnr_difference_all.png" />
									</div>
									<div class="{tabSet1 === 'FPR Difference' ? '' : 'hidden'}">
										<img src="/results/fpr_difference_all.png" />
									</div>
									<div class="{tabSet1 === 'FDR Difference' ? '' : 'hidden'}">
										<img src="/results/fdr_difference_all.png" />
									</div>
									<div class="{tabSet1 === 'FOR Difference' ? '' : 'hidden'}">
										<img src="/results/for_difference_all.png" />
									</div>

								</svelte:fragment>
							</TabGroup>
							<p class="mt-12">
								We can perform the same visualisation for the <i>accurate</i> recruiters,
								(recruiters with accuracy >95%):
							</p>
							<TabGroup class="px-8 flex-grow mt-4" justify="flex-wrap">
								{#each biasMetrics as tabName}
									<Tab bind:group={tabSet2} name="{tabName}" value={tabName}>
										{tabName}
									</Tab>
								{/each}
								<svelte:fragment slot="panel">
									<div class="{tabSet2 === 'FNR Difference' ? '' : 'hidden'}">
										<img src="/results/fnr_difference_acc.png" />
									</div>
									<div class="{tabSet2 === 'FPR Difference' ? '' : 'hidden'}">
										<img src="/results/fpr_difference_acc.png" />
									</div>
									<div class="{tabSet2 === 'FDR Difference' ? '' : 'hidden'}">
										<img src="/results/fdr_difference_acc.png" />
									</div>
									<div class="{tabSet2 === 'FOR Difference' ? '' : 'hidden'}">
										<img src="/results/for_difference_acc.png" />
									</div>

								</svelte:fragment>
							</TabGroup>
						</div>


					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-2xl">2) Established Metrics for Bias Disagree</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-12">
							<p class="text-center font-semibold">
								"Two of the most commonly used metrics for defining bias in machine learning
								rarely agree. Under certain common
								conditions, they even <i>contradict</i> each other on which group the bias is against."
							</p>
							<p class="mt-16">
								The <span class="text-surface-600 font-bold">Competence Rate</span> for a group is the proportion of
								people in that group who are competent.
							</p>
							<p>
								The <span class="text-surface-600 font-bold">Competence Difference</span> is the difference between
								these values for different groups.
							</p>
							<p class="mt-8">
								When the competence difference value is low, the bias metrics are strongly correlated.
							</p>
							<p class="mt-4">
								For now, let's focus on simulation runs when this competence difference is less than 5%.

							</p>
							<p class="mt-12">
								Below, we plot <span class="text-surface-600 font-bold">Scatter Graphs</span> to compare each metric.
								Each dot represents a recruiter. For each one, we calculate the position of the
								dot based on the two metrics we're interested in.
							</p>

							<p class="mt-8">
								You can select both metrics to compare.
							</p>
							<div class="flex items-center mt-4">
								<div class="min-w-[5rem]">
									<TabGroup justify="flex-col"
														class=" flex-grow flex-col mt-4 pt-12 mx-4">
										{#each biasMetrics as tabName}
											<Tab bind:group={tabSet4} name="{tabName}" value={tabName}>
												<div style="writing-mode: vertical-rl"
														 class="rotate-180 {tabSet4 === tabName ? 'border-l-2 border-surface-600' : ''}">
													{tabName}
												</div>
											</Tab>
										{/each}
									</TabGroup>
								</div>
								<TabGroup class="flex-grow mt-4" justify="flex-wrap">
									{#each biasMetrics as tabName}
										<Tab bind:group={tabSet3} name="{tabName}" value={tabName}>
											{tabName}
										</Tab>
									{/each}
									<svelte:fragment slot="panel">
										<div class="flex px-8">
											<div>
												<div class="{tabSet3 === 'FNR Difference' && tabSet4 === 'FNR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fnr_fnr.png" />
												</div>
												<div class="{tabSet3 === 'FNR Difference' && tabSet4 === 'FPR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fnr_fpr.png" />
												</div>
												<div class="{tabSet3 === 'FNR Difference' && tabSet4 === 'FDR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fnr_fdr.png" />
												</div>
												<div class="{tabSet3 === 'FNR Difference' && tabSet4 === 'FOR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fnr_for.png" />
												</div>

												<div class="{tabSet3 === 'FPR Difference' && tabSet4 === 'FNR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fpr_fnr.png" />
												</div>
												<div class="{tabSet3 === 'FPR Difference' && tabSet4 === 'FPR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fpr_fpr.png" />
												</div>
												<div class="{tabSet3 === 'FPR Difference' && tabSet4 === 'FDR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fpr_fdr.png" />
												</div>
												<div class="{tabSet3 === 'FPR Difference' && tabSet4 === 'FOR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fpr_for.png" />
												</div>

												<div class="{tabSet3 === 'FDR Difference' && tabSet4 === 'FNR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fdr_fnr.png" />
												</div>
												<div class="{tabSet3 === 'FDR Difference' && tabSet4 === 'FPR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fdr_fpr.png" />
												</div>
												<div class="{tabSet3 === 'FDR Difference' && tabSet4 === 'FDR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fdr_fdr.png" />
												</div>
												<div class="{tabSet3 === 'FDR Difference' && tabSet4 === 'FOR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/fdr_for.png" />
												</div>

												<div class="{tabSet3 === 'FOR Difference' && tabSet4 === 'FNR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/for_fnr.png" />
												</div>
												<div class="{tabSet3 === 'FOR Difference' && tabSet4 === 'FPR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/for_fpr.png" />
												</div>
												<div class="{tabSet3 === 'FOR Difference' && tabSet4 === 'FDR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/for_fdr.png" />
												</div>
												<div class="{tabSet3 === 'FOR Difference' && tabSet4 === 'FOR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_low_disp/for_for.png" />
												</div>

											</div>
										</div>

									</svelte:fragment>
								</TabGroup>
							</div>
							<p class="mt-16">
								We find that while there are patterns between the bias metrics, it would be very difficult to
								accurately predict one from another.
								They show poor agreement in general.
							</p>
							<p class="mt-16">
								Another interesting finding is that
								<span class="text-purple-700 font-bold">FOR Difference</span> goes up as
								<span class="text-yellow-700 font-bold">FDR Difference</span> goes down.
							</p>
							<p class="mt-4">
								It seems that if more non-competent applicant's from group A are
								being hired (which appears to benefit group A),
								it's likely to come at the expense of competent
								applicant's from group A not being hired (which disadvantages group A).
							</p>

							<p class="mt-16">
								<span class="text-emerald-700 font-bold">FNR Difference</span> and <span
								class="text-purple-700 font-bold">FOR Difference</span>, as well as
								<span class="text-cyan-800 font-bold">FPR Difference</span> and <span class="text-yellow-700 font-bold">FDR Difference</span>
								are also negatively correlated.
							</p>
							<p class="mt-4">
								It seems that at least
								some of these bias metrics don't give an adequate picture of how an unfair a process is.
							</p>

							<p class="mt-32">
								When there is a high difference in competence between the two groups, the metrics for bias
								show even less agreement and usually contradict each other.
							</p>
							<p class="mt-8">
								Below we show the same scatter graphs for the case when the
								Competence Difference is over 30 percentage points:
							</p>
							<p class="mt-4">
								Notice that every recruiter in the yellow area exhibits metrics for bias which disagree on the
								direction of that bias.
							</p>

							<div class="flex items-center mt-4">
								<div class="min-w-[5rem]">
									<TabGroup justify="flex-col"
														class=" flex-grow flex-col mt-4 pt-12 mx-4">
										{#each biasMetrics as tabName}
											<Tab bind:group={tabSet6} name="{tabName}" value={tabName}>
												<div style="writing-mode: vertical-rl"
														 class="rotate-180 {tabSet6 === tabName ? 'border-l-2 border-surface-600' : ''}">
													{tabName}
												</div>
											</Tab>
										{/each}
									</TabGroup>
								</div>
								<TabGroup class="flex-grow mt-4" justify="flex-wrap">
									{#each biasMetrics as tabName}
										<Tab bind:group={tabSet5} name="{tabName}" value={tabName}>
											{tabName}
										</Tab>
									{/each}
									<svelte:fragment slot="panel">
										<div class="flex px-8">
											<div>
												<div class="{tabSet5 === 'FNR Difference' && tabSet6 === 'FNR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fnr_fnr.png" />
												</div>
												<div class="{tabSet5 === 'FNR Difference' && tabSet6 === 'FPR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fnr_fpr.png" />
												</div>
												<div class="{tabSet5 === 'FNR Difference' && tabSet6 === 'FDR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fnr_fdr.png" />
												</div>
												<div class="{tabSet5 === 'FNR Difference' && tabSet6 === 'FOR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fnr_for.png" />
												</div>

												<div class="{tabSet5 === 'FPR Difference' && tabSet6 === 'FNR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fpr_fnr.png" />
												</div>
												<div class="{tabSet5 === 'FPR Difference' && tabSet6 === 'FPR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fpr_fpr.png" />
												</div>
												<div class="{tabSet5 === 'FPR Difference' && tabSet6 === 'FDR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fpr_fdr.png" />
												</div>
												<div class="{tabSet5 === 'FPR Difference' && tabSet6 === 'FOR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fpr_for.png" />
												</div>

												<div class="{tabSet5 === 'FDR Difference' && tabSet6 === 'FNR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fdr_fnr.png" />
												</div>
												<div class="{tabSet5 === 'FDR Difference' && tabSet6 === 'FPR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fdr_fpr.png" />
												</div>
												<div class="{tabSet5 === 'FDR Difference' && tabSet6 === 'FDR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fdr_fdr.png" />
												</div>
												<div class="{tabSet5 === 'FDR Difference' && tabSet6 === 'FOR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/fdr_for.png" />
												</div>

												<div class="{tabSet5 === 'FOR Difference' && tabSet6 === 'FNR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/for_fnr.png" />
												</div>
												<div class="{tabSet5 === 'FOR Difference' && tabSet6 === 'FPR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/for_fpr.png" />
												</div>
												<div class="{tabSet5 === 'FOR Difference' && tabSet6 === 'FDR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/for_fdr.png" />
												</div>
												<div class="{tabSet5 === 'FOR Difference' && tabSet6 === 'FOR Difference' ? '' : 'hidden'}">
													<img src="/results/compare_metrics_high_disp/for_for.png" />
												</div>

											</div>
										</div>

									</svelte:fragment>
								</TabGroup>
							</div>

							<p class="mt-8">
								We see that Equalised Odds and Predictive Parity regularly disagree on the direction of bias.
							</p>
							<p class="mt-4">
								We'll discuss this further in the next section.
							</p>


							<p class="mt-48">
								We do find one interesting relationship between
								<span class="text-surface-600 font-bold">Equalised Odds</span>
								and
								<span class="text-surface-600 font-bold">Predictive Parity</span>:
							</p>
							<p class="mt-8">
								When both the competence difference is low, and
								<span>Demographic Parity</span> is close to being satisfied,
								then the absolute sum of <span class="text-emerald-700 font-bold">FNR Difference</span>
								and <span class="text-yellow-700 font-bold">FDR Difference</span>
								is closely correlated to the absolute sum of
								<span
									class="text-purple-700 font-bold">FOR Difference</span> and
								<span
									class="text-purple-700 font-bold">FDR Difference</span>.
							</p>


							<p class="mt-4">
								The following scatter graph only considers recruiters when the Competence Difference is less than 5%
								and the Hired Rate Difference is less than 5%.
							</p>

							<div class="flex justify-center mt-12">
								<img width="600" src="/results/equalised_odds_and_predictive_parity.png" />
							</div>


						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-2xl">3) Bias Exacerbates Existing Differences</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-12">
							<div class="text-center font-semibold">

								"If group A tends to be worse at the job than group B on average,
								this makes group A <i>more</i> likely to face unfair treatment in hiring.
								In other words, existing performance differences can lead to even stronger bias.
								<p class="mt-8">
									However, by only looking at the selection of people who were hired,
									and the selection of people who weren't, we are likely to conclude that the bias is
									actually in <i>favour</i> of group A, contradicting this finding.
								</p>
								<p class="mt-8">
									If both groups are just as good at the job on average, bias is <i>lower</i>
									but is still usually significant."
								</p>
							</div>
							<p class="mt-24">
								If the competence difference is high, then
								<span class="text-surface-600 font-bold">Equalised Odds</span> and
								<span class="text-surface-600 font-bold">Demographic Parity</span> are much more likely to measure the
								bias
								as being in favour of the more-competent group.
							</p>
							<p class="mt-4">
								However, <span class="text-surface-600 font-bold">Predictive Parity</span>
								is more likely to measure it in favour of the less-competent group.
							</p>
							<p class="mt-24">
								As before, we can plot a histogram. This only includes
								simulation runs with a >30% Competence Difference.
							</p>
							<p class="mt-4">
								Positive values show bias in favour of the more-competent group, and
								negative values show bias in favour of the less-competent group.
							</p>

							<TabGroup class=" flex-grow mt-12" justify="flex-wrap">
								{#each biasMetricsAndDem as tabName}
									<Tab bind:group={tabSet7} name="{tabName}" value={tabName}>
										{tabName}
									</Tab>
								{/each}
								<svelte:fragment slot="panel">
									<div class="{tabSet7 === 'FNR Difference' ? '' : 'hidden'}">
										<img src="/results/bias_high_disp/fnr.png" />
									</div>
									<div class="{tabSet7 === 'FPR Difference' ? '' : 'hidden'}">
										<img src="/results/bias_high_disp/fpr.png" />
									</div>
									<div class="{tabSet7 === 'FDR Difference' ? '' : 'hidden'}">
										<img src="/results/bias_high_disp/fdr.png" />
									</div>
									<div class="{tabSet7 === 'FOR Difference' ? '' : 'hidden'}">
										<img src="/results/bias_high_disp/for.png" />
									</div>
									<div class="{tabSet7 === 'Demographic Parity' ? '' : 'hidden'}">
										<img src="/results/bias_high_disp/dem.png" />
									</div>

								</svelte:fragment>
							</TabGroup>

							<p class="mt-12">
								In this case, Equalised Odds is the intuitionistically preferred definition.
							</p>
							<p class="mt-8">
								But by only considering the proportions of the hired and rejected pools who are competent,
								we may conclude that a process is biased against the group it actually favours.
							</p>

							<p class="mt-24">
								The amount of bias measured by each metric increases as the competence difference does.
							</p>
							<p class="mt-4">
								Below, we see how each bias metric varies with the competence difference.
							</p>

							<TabGroup class=" flex-grow mt-6" justify="flex-wrap">
								{#each biasMetricsAndDem as tabName}
									<Tab bind:group={tabSet8} name="{tabName}" value={tabName}>
										{tabName}
									</Tab>
								{/each}
								<svelte:fragment slot="panel">
									<div class="{tabSet8 === 'FNR Difference' ? '' : 'hidden'}">
										<img src="/results/compare_competence/fnr.png" />
									</div>
									<div class="{tabSet8 === 'FPR Difference' ? '' : 'hidden'}">
										<img src="/results/compare_competence/fpr.png" />
									</div>
									<div class="{tabSet8 === 'FDR Difference' ? '' : 'hidden'}">
										<img src="/results/compare_competence/fdr.png" />
									</div>
									<div class="{tabSet8 === 'FOR Difference' ? '' : 'hidden'}">
										<img src="/results/compare_competence/for.png" />
									</div>
									<div class="{tabSet8 === 'Demographic Parity' ? '' : 'hidden'}">
										<img src="/results/compare_competence/dem.png" />
									</div>

								</svelte:fragment>
							</TabGroup>

							<p class="mt-24">
								However, bias still exists when the competence difference is low.
							</p>
							<p class="mt-4">
								Below, we plot a histogram for each bias metric when the competence difference is
								very low (below 1%):
							</p>

							<TabGroup class=" flex-grow mt-6" justify="flex-wrap">
								{#each biasMetricsAndDem as tabName}
									<Tab bind:group={tabSet9} name="{tabName}" value={tabName}>
										{tabName}
									</Tab>
								{/each}
								<svelte:fragment slot="panel">
									<div class="{tabSet9 === 'FNR Difference' ? '' : 'hidden'}">
										<img src="/results/very_low_disparity/fnr.png" />
									</div>
									<div class="{tabSet9 === 'FPR Difference' ? '' : 'hidden'}">
										<img src="/results/very_low_disparity/fpr.png" />
									</div>
									<div class="{tabSet9 === 'FDR Difference' ? '' : 'hidden'}">
										<img src="/results/very_low_disparity/fdr.png" />
									</div>
									<div class="{tabSet9 === 'FOR Difference' ? '' : 'hidden'}">
										<img src="/results/very_low_disparity/for.png" />
									</div>
									<div class="{tabSet9 === 'Demographic Parity' ? '' : 'hidden'}">
										<img src="/results/very_low_disparity/dem.png" />
									</div>

								</svelte:fragment>
							</TabGroup>

						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-2xl">4) We can Reduce Bias by Hiding Information</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-12">
							<div class="text-center font-semibold">
								<p>
									"We can reduce bias by hiding which group each applicant belongs to.
								</p>
								<p class="mt-8">
									We can reduce it even more by removing any information that hints at group membership,
									although this might slightly reduce accuracy."
								</p>
							</div>

							<p class="mt-16">
								Recall the conditions we introduced in the last section:

							</p>
							<p class="mt-8 text-left">
								Each Applicant reveals the same set of 10 randomly selected characteristics, where...
							</p>
							<ol class="list-decimal list-inside ml-10 text-left space-y-4 min-w-[40rem] mt-4">
								<li>
									...this <i>doesn't</i> include the <span
									class="text-surface-600 font-bold">Protected Characteristic</span>.
								</li>
								<li>
									...this <i>does</i> include the Protected Characteristic.
								</li>
								<li>
									...this includes five <span class="text-surface-600 font-bold">Proxy Characteristics</span>
									(characteristics which are <i>directly</i>
									linked to the Protected Characteristic on the Bayesian Network).
								</li>
								<li>
									...this doesn't include <i>any</i> <span
									class="text-surface-600 font-bold">Distance Proxy Characteristics</span>
									(characteristics
									linked to the Protected Characteristic <i>by one or two edges</i> on the Bayesian Network).
								</li>
							</ol>

							<p class="mt-8">
								We abbreviate these conditions as
								<span class="text-surface-600 font-bold">Omit Protected</span>,
								<span class="text-surface-600 font-bold">Include Protected</span>,
								<span class="text-surface-600 font-bold">Include Proxies</span>, and
								<span class="text-surface-600 font-bold">Omit Distant Proxies</span>.
							</p>

							<p class="mt-12">
								We can visualise the amount of bias recruiters exhibit with each of these conditions,
								with a <span
								class="text-surface-600 font-bold">KDE Plot</span>.
							</p>
							<p class="mt-4">
								This is a smoothed version of a histogram, and we use it here as it allows us to see each condition on
								the same graph. The height of the line represents how many recruiters exhibited that level of bias.
							</p>
							<p class="mt-4">
								Positive values show bias in favour of the more-competent group, and
								negative values show bias in favour of the less-competent group.
							</p>

							<TabGroup class=" flex-grow mt-6" justify="flex-wrap">
								{#each biasMetricsAndDem as tabName}
									<Tab bind:group={tabSet10} name="{tabName}" value={tabName}>
										{tabName}
									</Tab>
								{/each}
								<svelte:fragment slot="panel">
									<div class="{tabSet10 === 'FNR Difference' ? '' : 'hidden'}">
										<img src="/results/compare_conditions/fnr.png" />
									</div>
									<div class="{tabSet10 === 'FPR Difference' ? '' : 'hidden'}">
										<img src="/results/compare_conditions/fpr.png" />
									</div>
									<div class="{tabSet10 === 'FDR Difference' ? '' : 'hidden'}">
										<img src="/results/compare_conditions/fdr.png" />
									</div>
									<div class="{tabSet10 === 'FOR Difference' ? '' : 'hidden'}">
										<img src="/results/compare_conditions/for.png" />
									</div>
									<div class="{tabSet10 === 'Demographic Parity' ? '' : 'hidden'}">
										<img src="/results/compare_conditions/dem.png" />
									</div>

								</svelte:fragment>
							</TabGroup>

							<p class="mt-8">
								A higher curve shows that bias is lower, because more recruiters have bias values around 0.
							</p>

							<p class="mt-4">
								Recall that equalised odds is our preferred definition of unbiasedness in the context of recruiting.
							</p>


							<p class="mt-16">
								We see we can reduce bias
								by omitting the protected characteristic from the application,
								and we can reduce it further by omitting all distant proxies as well.
							</p>
							<p class="mt-4">
								This is because a recruiter may be able to partially infer the
								protected characteristic from those proxies.
							</p>

							<p class="mt-12">
								However, we also see that by revealing the protected characteristic to a recruiter,
								we reduce it's bias from a Predictive Parity perspective.
							</p>

							<p class="mt-24">
								Finally, we can ask whether these conditions have some effect on accuracy.
								We find those effects are minimal:
							</p>
							<table class="table table-hover px-4 mt-8">
								<thead>
								<tr>
									<th>Condition</th>
									<th>Average Accuracy</th>
								</tr>
								</thead>
								<tbody>
								<tr>
									<td>Omit Protected</td>
									<td class="text-surface-600">83.1%</td>
								</tr>
								<tr>
									<td>Include Protected</td>
									<td class="text-surface-600">82.5%</td>
								</tr>
								<tr>
									<td>Include Proxies</td>
									<td class="text-surface-600">82.4%</td>
								</tr>
								<tr>
									<td>Omit Distant Proxies</td>
									<td class="text-surface-600">81.9%</td>
								</tr>
								</tbody>
							</table>


						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span class="font-bold text-2xl">5) Different ML Models lead to Different Levels of Bias</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-12">
							<div class="font-semibold text-center">
								"Different machine learning architectures show significant difference in the level of bias in the
								decisions they make."
							</div>
							<p class="mt-16">
								As before, we draw a KDE plot for each bias metric to compare recruiters.
							</p>
							<p class="mt-4">
								Positive values show bias in favour of the more-competent group, and
								negative values show bias in favour of the less-competent group.
							</p>

							<TabGroup class=" flex-grow mt-6" justify="flex-wrap">
								{#each biasMetricsAndDem as tabName}
									<Tab bind:group={tabSet11} name="{tabName}" value={tabName}>
										{tabName}
									</Tab>
								{/each}
								<svelte:fragment slot="panel">
									<div class="{tabSet11 === 'FNR Difference' ? '' : 'hidden'}">
										<img src="/results/recruiters/fnr.png" />
									</div>
									<div class="{tabSet11 === 'FPR Difference' ? '' : 'hidden'}">
										<img src="/results/recruiters/fpr.png" />
									</div>
									<div class="{tabSet11 === 'FDR Difference' ? '' : 'hidden'}">
										<img src="/results/recruiters/fdr.png" />
									</div>
									<div class="{tabSet11 === 'FOR Difference' ? '' : 'hidden'}">
										<img src="/results/recruiters/for.png" />
									</div>
									<div class="{tabSet11 === 'Demographic Parity' ? '' : 'hidden'}">
										<img src="/results/recruiters/dem.png" />
									</div>

								</svelte:fragment>
							</TabGroup>

							<p class="mt-12">
								We see that there are differences in the amount of bias shown by different recruiters,
								and that these differences are generally consistent across metrics.
							</p>
							<p class="mt-16">
								We might ask whether these differences are only due to differences in accuracy between the models,
								but one of the least accurate models, the
								<span class="text-surface-600 font-bold">Deep MLP</span> is relatively unbiased.
							</p>
							<p class="mt-4">
								We can also separately confirm that there is little relationship between accuracy and
								bias when there is low competence disparity, but these differences in recruiters largely remain.
							</p>
							<p class="mt-16">
								The following KDEs are for the runs when the competence rate difference is less than 5%.
							</p>

							<TabGroup class=" flex-grow mt-6" justify="flex-wrap">
								{#each biasMetricsAndDem as tabName}
									<Tab bind:group={tabSet12} name="{tabName}" value={tabName}>
										{tabName}
									</Tab>
								{/each}
								<svelte:fragment slot="panel">
									<div class="{tabSet12 === 'FNR Difference' ? '' : 'hidden'}">
										<img src="/results/recruiters_low_disp/fnr.png" />
									</div>
									<div class="{tabSet12 === 'FPR Difference' ? '' : 'hidden'}">
										<img src="/results/recruiters_low_disp/fpr.png" />
									</div>
									<div class="{tabSet12 === 'FDR Difference' ? '' : 'hidden'}">
										<img src="/results/recruiters_low_disp/fdr.png" />
									</div>
									<div class="{tabSet12 === 'FOR Difference' ? '' : 'hidden'}">
										<img src="/results/recruiters_low_disp/for.png" />
									</div>
									<div class="{tabSet12 === 'Demographic Parity' ? '' : 'hidden'}">
										<img src="/results/recruiters_low_disp/dem.png" />
									</div>

								</svelte:fragment>
							</TabGroup>


						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-2xl">6) Post-Training Mitigations can Reduce Bias</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-12">
							<div class="font-bold text-center">
								"Simple post-training bias mitigations can reduce levels of bias in machine learning recruiters, at
								a slight cost to accuracy."
							</div>
							<p class="mt-12">
								As before, we can draw a KDE plot to see how our mitigated recruiters perform on each bias metric.
							</p>

							<TabGroup class=" flex-grow mt-6" justify="flex-wrap">
								{#each biasMetricsAndDem as tabName}
									<Tab bind:group={tabSet13} name="{tabName}" value={tabName}>
										{tabName}
									</Tab>
								{/each}
								<svelte:fragment slot="panel">
									<div class="{tabSet13 === 'FNR Difference' ? '' : 'hidden'}">
										<img src="/results/mitigations/fnr.png" />
									</div>
									<div class="{tabSet13 === 'FPR Difference' ? '' : 'hidden'}">
										<img src="/results/mitigations/fpr.png" />
									</div>
									<div class="{tabSet13 === 'FDR Difference' ? '' : 'hidden'}">
										<img src="/results/mitigations/fdr.png" />
									</div>
									<div class="{tabSet13 === 'FOR Difference' ? '' : 'hidden'}">
										<img src="/results/mitigations/for.png" />
									</div>
									<div class="{tabSet13 === 'Demographic Parity' ? '' : 'hidden'}">
										<img src="/results/mitigations/dem.png" />
									</div>

								</svelte:fragment>
							</TabGroup>

							<p class="mt-12">
								We confirm that it is possible to use this method to partially optimise a particular
								metric.
							</p>
							<p class="mt-12">
								However, we are unable to use this method to fully satisfy Equalised Odds or
								Predictive Parity.
							</p>

							<p class="mt-12">
								Finally, we can ask whether these bias mitigations come at the expense of accuracy.
								We find that they don't, expect for the Demographic Parity mitigation:
							</p>

							<table class="table table-hover px-4 mt-8">
								<thead>
								<tr>
									<th>Mitigation</th>
									<th>Average Accuracy</th>
								</tr>
								</thead>
								<tbody>
								<tr>
									<td>No Mitigation</td>
									<td class="text-surface-600">83.2%</td>
								</tr>
								<tr>
									<td>Optimise for FDR and FOR Equality</td>
									<td class="text-surface-600">82.6%</td>
								</tr>
								<tr>
									<td>Optimise for FOR Equality</td>
									<td class="text-surface-600">82.2%</td>
								</tr>
								<tr>
									<td>Optimise for FDR Equality</td>
									<td class="text-surface-600">82.1%</td>
								</tr>
								<tr>
									<td>Optimise for FNR and FPR Equality</td>
									<td class="text-surface-600">81.8%</td>
								</tr>
								<tr>
									<td>Optimise for FNR Equality</td>
									<td class="text-surface-600">81.6%</td>
								</tr>
								<tr>
									<td>Optimise for FPR Equality</td>
									<td class="text-surface-600">81.6%</td>
								</tr>
								<tr>
									<td>Ensure Demographic Parity</td>
									<td class="text-surface-600">78.7%</td>
								</tr>
								</tbody>
							</table>


						</div>
					</svelte:fragment>
				</AccordionItem>
			</Accordion>
		</div>
	</div>
</div>