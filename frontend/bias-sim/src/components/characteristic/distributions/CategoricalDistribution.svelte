<g>
	{#each bars as bar}
		<g class="bar">
			<rect rx="2" x={x(bar.category.toString())??0} y={ mounted ? y(bar.value) : y(0)}
						width={x.bandwidth()} height={ mounted ? height - y(bar.value) : 0}
						style="transition: height 750ms cubic-bezier(0.68, -0.55, 0.27, 1.55),
															 y 750ms cubic-bezier(0.68, -0.55, 0.27, 1.55)"
						fill="#0d3b68">

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
	<g bind:this={axisLeft} />
</g>


<script lang="ts">
	import * as d3 from 'd3';
	import { distributionById, network } from '../../../stores/store';
	import { onMount } from 'svelte';

	export let nodeId: string;
	export let width: number;
	export let height: number;

	let mounted = false;
	let axisBottom: SVGGElement;
	let axisLeft: SVGGElement;

	$: distribution = $distributionById[nodeId].distribution;

	$: bars = Array.from(new Set(distribution)).map(categoryIndex => ({
		category: $network.characteristics[nodeId].categoryNames[categoryIndex],
		value: distribution.filter(d => d === categoryIndex).length / distribution.length
	}));

	$: maxBarY = Math.max(...bars.map((bar: Bar) => bar.value));


	$: x = d3.scaleBand().range([0, width]).domain(bars.map((bar: Bar) => bar.category.toString())).padding(0.2);
	$: y = d3.scaleLinear().domain([0, maxBarY]).range([height, 0]);

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
		d3.select(axisBottom).call(d3.axisBottom(x));
	}

	$: if (axisLeft) {
		d3.select(axisLeft).call(d3.axisLeft(y).ticks(2));
	}

	function calculateBarY(barValue: number) {
		const belowBarY = y(barValue) + 11;
		const aboveBarY = y(barValue) - 4;
		return (belowBarY < y(0)) ? belowBarY : aboveBarY;
	}

</script>