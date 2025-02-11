<script lang="ts">
	import { Accordion } from '@skeletonlabs/skeleton';
	import type { CategoricalRecruiterBiasAnalysis } from '../../../../types/Bias.js';
	import PerformanceSummary from './PerformanceSummary.svelte';
	import DemographicParitySummary from './DemographicParitySummary.svelte';
	import EqualisedOddsSummary from './EqualisedOddsSummary.svelte';
	import PredictiveParitySummary from './PredictiveParitySummary.svelte';

	export let recruiter: CategoricalRecruiterBiasAnalysis;
</script>

<div>
	<section>

		<Accordion>
			<PerformanceSummary recruiter={recruiter} />
			<hr />
			<DemographicParitySummary recruiter={recruiter} />
			<hr />
			<EqualisedOddsSummary recruiter={recruiter} />

			<hr />
			<PredictiveParitySummary recruiter={recruiter} />


		</Accordion>


	</section>

</div>