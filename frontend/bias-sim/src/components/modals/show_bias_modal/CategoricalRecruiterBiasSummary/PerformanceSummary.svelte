<script lang="ts">
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import BiasSubTitle from '../BiasSubTitle.svelte';
	import BiasTitle from '../BiasTitle.svelte';
	import type { CategoricalRecruiterBiasAnalysis } from '../../../../types/Bias.js';

	export let recruiter: CategoricalRecruiterBiasAnalysis;

</script>

<AccordionItem>
	<svelte:fragment slot="summary">
		<BiasTitle>Performance</BiasTitle>
	</svelte:fragment>
	<svelte:fragment slot="content">
		<Accordion spacing="0">
			<AccordionItem>
				<svelte:fragment slot="summary">
					<BiasSubTitle title="Model Accuracy:" value={recruiter.general.accuracy} />
				</svelte:fragment>
				<svelte:fragment slot="content">
					<p>The proportion of times the model predicted the applicant's competence correctly.</p>
				</svelte:fragment>
			</AccordionItem>
			<hr />

			<AccordionItem>
				<svelte:fragment slot="summary">
					<BiasSubTitle title="Proportion of People Hired:" value={recruiter.general.hiredRate} />
					<BiasSubTitle title={"Proportion of People Competent:"}
												value={recruiter.general.competentRate} />
				</svelte:fragment>
				<svelte:fragment slot="content">
					<div>
						<p>The proportion of people the model predicted were competent.</p>
						<p>The proportion of people who were actually competent.</p>
					</div>
				</svelte:fragment>
			</AccordionItem>
			<hr />
			<AccordionItem>
				<svelte:fragment slot="summary">
					<BiasSubTitle title="False Positive Rate:" value={recruiter.general.falsePositiveRate} />

				</svelte:fragment>
				<svelte:fragment slot="content">
					<div>
						<p>Of people who weren't competent, how many got hired anyway?</p>
					</div>
				</svelte:fragment>
			</AccordionItem>
			<hr />
			<AccordionItem>
				<svelte:fragment slot="summary">
					<BiasSubTitle title="False Negative Rate:" value={recruiter.general.falseNegativeRate} />

				</svelte:fragment>
				<svelte:fragment slot="content">
					<div>
						<p>Of people who were actually competent, how many didn't get hired?</p>
					</div>
				</svelte:fragment>
			</AccordionItem>
			<hr />
			<AccordionItem>
				<svelte:fragment slot="summary">

					<BiasSubTitle title="False Discovery Rate:" value={recruiter.general.falseDiscoveryRate} />
				</svelte:fragment>
				<svelte:fragment slot="content">
					<div>
						<p>Of people hired, how many weren't actually competent?</p>
					</div>
				</svelte:fragment>
			</AccordionItem>
			<hr />
			<AccordionItem>
				<svelte:fragment slot="summary">
					<BiasSubTitle title="False Omission Rate:" value={recruiter.general.falseOmissionRate} />
				</svelte:fragment>
				<svelte:fragment slot="content">
					<div>
						<p>Of people not hired, how many were actually competent?</p>
					</div>
				</svelte:fragment>
			</AccordionItem>
		</Accordion>
	</svelte:fragment>
</AccordionItem>