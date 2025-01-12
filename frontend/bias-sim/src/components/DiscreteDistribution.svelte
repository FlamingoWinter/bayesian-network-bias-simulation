<g>
	{#each bars as bar}
		<g class="bar">
			<rect rx="2" x={x(bar.x)} y={ mounted ? y(bar.y) : y(0)}
						width={(x(barWidth) - x(0)) * 0.9} height={ mounted ? height - y(bar.y) : 0}
						fill="#0d3b68"
						style="transition: height 750ms cubic-bezier(0.68, -0.55, 0.27, 1.55),
															 y 750ms cubic-bezier(0.68, -0.55, 0.27, 1.55)">

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
	<g bind:this={axisBottom} transform={`translate(0, ${height})`} />
</g>


<script lang="ts">
	import * as d3 from 'd3';
	import { distributionById } from '../stores/store';
	import { onMount } from 'svelte';

	export let nodeId: string;
	export let width: number;
	export let height: number;

	let mounted = false;
	let axisBottom: SVGGElement;
	let axisLeft: SVGGElement;

	$: distribution = $distributionById[nodeId].distribution;
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

	$: x = d3.scaleLinear().range([0, width]).domain([Math.min(...distribution), Math.max(...distribution)]);
	$: y = d3.scaleLinear().domain([0, maxBarY]).range([height, 0]);
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

	$: if (axisBottom) {
		d3.select(axisBottom).call(d3.axisBottom(x).ticks(5));
	}

	function calculateBarY(barValue: number) {
		const belowBarY = y(barValue) + 11;
		const aboveBarY = y(barValue) - 4;
		return (belowBarY < y(0)) ? belowBarY : aboveBarY;
	}

</script>