<g>
	{#each bars as bar}
		<g class="bar">
			<rect rx="2" x={x(bar.category.toString())??0} y={ mounted ? y(bar.value) : y(0)}
						width={x.bandwidth()} height={ mounted ? height - y(bar.value) : 0}
						style="transition: height {defaultTransition},
															 y {defaultTransition}"
						fill={calculateDistributionFill(probabilityType)}>
			</rect>
		</g>
		<g>
			<text class="bar-label"
						x={(x(bar.category.toString())?? 0) + x.bandwidth() / 2}
						y={0}
						transform={`translate(0, ${mounted? calculateBarY(bar.value): y(0)+11})`}
						text-anchor="middle" font-size="8px" font-weight="400"
						fill={y(bar.value) + 11 < y(0) ? '#d3effb' : '#000'}
						style="transition: transform 750ms">
				{`≈ ${bar.value.toFixed(2)}`}
			</text>
		</g>
	{/each}
	<g bind:this={axisBottom} transform={`translate(0, ${height})`} />
	<AxisLeft height={height} display={true} maxBarY={maxBarY} bind:y={y} />
</g>


<script lang="ts">
	import * as d3 from 'd3';
	import { onMount } from 'svelte';
	import { conditioned, conditions, posteriorDistributions } from '../../../stores/store';
	import type { Characteristic } from '../../../types/network';
	import { defaultTransition } from '../../../animation/transition';
	import { calculateDistributionFill } from './calculateDistributionFill';
	import AxisLeft from './AxisLeft.svelte';

	export let characteristic: Characteristic;
	export let width: number;
	export let height: number;

	let mounted = false;
	let axisBottom: SVGGElement;
	let axisLeft: SVGGElement;
	let probabilityType: ProbabilityType;

	$: probabilityType = $conditioned
		? (characteristic.name in $conditions ? 'conditioned' : 'posterior')
		: 'prior';

	$: distribution = (probabilityType == 'posterior') ? $posteriorDistributions[characteristic.name] : characteristic.priorDistribution;
	$: bars = Array.from(new Set(distribution)).map(categoryIndex => ({
		category: characteristic.categoryNames[categoryIndex],
		value: distribution.filter(d => d === categoryIndex).length / distribution.length
	}));

	$: maxBarY = Math.max(...bars.map((bar: Bar) => bar.value));


	$: x = d3.scaleBand().range([0, width]).domain(characteristic.categoryNames).padding(0.2);
	let y = d3.scaleLinear().domain([0, maxBarY]).range([height, 0]);

	interface Bar {
		category: string,
		value: number
	}

	onMount(() => {
		setTimeout(() => {
			mounted = true;
		}, 0);
	});

	$: if (axisBottom) {
		d3.select(axisBottom).transition().call(d3.axisBottom(x));
	}

	function calculateBarY(barValue: number) {
		const belowBarY = y(barValue) + 11;
		const aboveBarY = y(barValue) - 4;
		return (belowBarY < y(0)) ? belowBarY : aboveBarY;
	}


</script>