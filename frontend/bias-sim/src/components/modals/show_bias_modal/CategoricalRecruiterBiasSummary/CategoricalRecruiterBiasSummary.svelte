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
