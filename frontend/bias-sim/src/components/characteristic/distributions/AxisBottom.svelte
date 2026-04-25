<script lang="ts">
	import { tweened } from 'svelte/motion';
	import { get } from 'svelte/store';

	import * as d3 from 'd3';

	export let width: number;
	export let height: number;
	export let distribution: number[] = [0];
	export let extend = false;
	export let display = true;

	export let x: d3.ScaleLinear<number, number, never> = d3
		.scaleLinear()
		.range([0, width])
		.domain([Math.min(...distribution), Math.max(...distribution)]);

	const duration = 200;

	let axisBottom: SVGGElement;

	const minDistribution = tweened(Math.min(...distribution), { duration });
	const maxDistribution = tweened(Math.max(...distribution), { duration });

	const updating = { min: false, max: false };

	function updateAxis(minOrMax: 'min' | 'max') {
		if (!updating[minOrMax]) return;
		const minVal = get(minDistribution);
		const maxVal = get(maxDistribution);
		const extendAmount = extend ? (maxVal - minVal) * 0.05 : 0;
		x = d3
			.scaleLinear()
			.range([0, width])
			.domain([minVal - extendAmount, maxVal + extendAmount]);
		requestAnimationFrame(() => updateAxis(minOrMax));
	}

	$: {
		updating.min = true;
		minDistribution.set(Math.min(...distribution));
		updateAxis('min');
		setTimeout(() => {
			updating.min = false;
		}, duration + 20);
	}

	$: {
		updating.max = true;
		maxDistribution.set(Math.max(...distribution));
		updateAxis('max');
		setTimeout(() => {
			updating.max = false;
		}, duration + 20);
	}

	$: if (axisBottom && x) {
		d3.select(axisBottom).call(d3.axisBottom(x).ticks(5));
	}
</script>

{#if display}
	<g bind:this={axisBottom} transform={`translate(0, ${height})`} />
{/if}
