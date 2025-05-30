<g>
	{#each bars as bar}
		<g class="bar">
			<rect rx="2" x={x(bar.x)} y={ mounted ? y(bar.y) : y(0)}
						width={(x(barWidth) - x(0)) * 0.9} height={ mounted ? height - y(bar.y) : 0}
						fill={calculateDistributionFill(probabilityType)}
						style="transition: height  {defaultTransition},
															 y {defaultTransition},
																fill {defaultTransition}">

			</rect>
		</g>
	{/each}
	<g>
		<text class="bar-label"
					x={x(median)}
					y={0}
					transform={`translate(0, ${mounted ? -4 : y(0) - 10})`}
					text-anchor="middle" font-size="8px" font-weight="400"
					fill="#000"
					style="transition: transform 750ms">
			{`${median.toPrecision(2)}`}
		</text>
	</g>
	<AxisBottom bind:x={x} height={height} width={width} distribution={distribution}></AxisBottom>
	<AxisLeft bind:y={y} height={height} maxBarY={maxBarY} display={false} />
</g>


<script lang="ts">
	import * as d3 from 'd3';
	import { onMount } from 'svelte';

	import { defaultTransition } from '../../../animation/transition';
	import type { Characteristic } from '../../../types/network';
	import { calculateDistributionFill } from './calculateDistributionFill';
	import AxisBottom from './AxisBottom.svelte';
	import AxisLeft from './AxisLeft.svelte';

	export let characteristic: Characteristic;
	export let width: number;
	export let height: number;
	export let conditions: Record<string, number>;
	export let conditioned: boolean;
	export let posteriorDistributions: Record<string, number[]>;

	let mounted = false;
	let probabilityType: ProbabilityType;

	$: probabilityType = conditioned
		? (characteristic.name in conditions ? 'conditioned' : 'posterior')
		: 'prior';

	let distribution: number[];
	$: switch (probabilityType) {
		case 'posterior':
			distribution = posteriorDistributions[characteristic.name];
		case 'prior':
			distribution = characteristic.priorDistribution;
		case 'conditioned':
			distribution = [conditions[characteristic.name]];
	}

	$: minValue = d3.min(distribution)!;
	$: maxValue = d3.max(distribution)!;
	$: barWidth = d3.tickStep(0, maxValue - minValue, 20);
	$: binStart = Math.floor(minValue / barWidth) * barWidth;
	$: bins = Array.from({ length: Math.ceil((maxValue - minValue) / barWidth) }, (_, i) => [
		binStart + i * barWidth,
		binStart + (i + 1) * barWidth
	]);


	$: bars = bins.map(([start, end]) => {
		return {
			x: start,
			y: distribution.filter(d => d >= start && d < end).length
		};
	});

	$: maxBarY = Math.max(...bars.map((bar: Bar) => bar.y));

	let x: d3.ScaleLinear<number, number, never> = d3.scaleLinear().range([0, 0]).domain([0, 0]);
	let y: d3.ScaleLinear<number, number, never> = d3.scaleLinear().domain([0, 0]).range([0, 0]);

	$: median = d3.median(distribution)!;

	interface Bar {
		x: number,
		y: number
	}

	onMount(() => {
		setTimeout(() => {
			mounted = true;
		}, 0);
	});


</script>