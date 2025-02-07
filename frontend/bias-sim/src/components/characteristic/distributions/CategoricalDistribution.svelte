<g>
	{#each bars as bar}
		<g class="bar">
			<rect rx="2" x={x(bar.category.toString())??0} y={ mounted ? y(bar.value) : y(0)}
						width={x.bandwidth()} height={ mounted ? height - y(bar.value) : 0}
						style="transition: height {defaultTransition},
															 y {defaultTransition},
															fill {defaultTransition}"
						fill={calculateDistributionFill(probabilityType)}>
			</rect>
		</g>
		<g>
			<CategoricalBarLabel x={x} y={y} bar={bar} mounted={mounted}
													 fontSize={characteristic.categoryNames.length > 2 ? 6 : 8} />

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
	import CategoricalBarLabel from './CategoricalBarLabel.svelte';

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

	$: distribution = (probabilityType === 'posterior')
		? $posteriorDistributions[characteristic.name]
		: (probabilityType === 'prior')
			? characteristic.priorDistribution
			: [$conditions[characteristic.name]];

	$: bars = Array.from(characteristic.categoryNames).map((categoryName, index) => ({
		category: categoryName,
		value: distribution.filter(d => d === index).length / distribution.length
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
		d3.select(axisBottom).selectAll('.tick text')
			.attr('font-size', `${characteristic.categoryNames.join('').length > 15 ? 7 : 10}`);
	}


</script>