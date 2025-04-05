<script lang="ts">
	import { Accordion } from '@skeletonlabs/skeleton';
	import type { MitigationBiasAnalysis } from '../../../../types/Bias.js';
	import PerformanceSummary from './PerformanceSummary.svelte';
	import DemographicParitySummary from './DemographicParitySummary.svelte';
	import EqualisedOddsSummary from './EqualisedOddsSummary.svelte';
	import PredictiveParitySummary from './PredictiveParitySummary.svelte';

	export let recruiter: MitigationBiasAnalysis;
	export let withoutMitigation: MitigationBiasAnalysis | null;

</script>

<div>
	<section>

		<Accordion>
			<PerformanceSummary recruiter={recruiter} />
			<hr />
			<DemographicParitySummary recruiter={recruiter} withoutMitigation={withoutMitigation} />
			<hr />
			<EqualisedOddsSummary recruiter={recruiter} withoutMitigation={withoutMitigation} />

			<hr />
			<PredictiveParitySummary recruiter={recruiter} withoutMitigation={withoutMitigation} />


		</Accordion>


	</section>

</div>