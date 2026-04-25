<script lang="ts">
	import { Accordion } from '@skeletonlabs/skeleton';
	import type { MitigationAnalysis } from '../../../../types/Bias.js';
	import PerformanceSummary from './PerformanceSummary.svelte';
	import DemographicParitySummary from './DemographicParitySummary.svelte';
	import EqualisedOddsSummary from './EqualisedOddsSummary.svelte';
	import PredictiveParitySummary from './PredictiveParitySummary.svelte';

	export let recruiter: MitigationAnalysis;
	export let withoutMitigation: MitigationAnalysis | null;
</script>

<div>
	<section>
		<Accordion>
			<PerformanceSummary {recruiter} />
			<hr />
			<DemographicParitySummary {recruiter} {withoutMitigation} />
			<hr />
			<EqualisedOddsSummary {recruiter} {withoutMitigation} />

			<hr />
			<PredictiveParitySummary {recruiter} {withoutMitigation} />
		</Accordion>
	</section>
</div>
