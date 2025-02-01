<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { onMount } from 'svelte';

	import * as d3 from 'd3';


	export let width: number;
	export let height: number;
	export let distribution: number[] = [0];
	export let extend = false;
	export let display = true;

	export let x: d3.ScaleLinear<number, number, never> = d3.scaleLinear().range([0, width]).domain([Math.min(...distribution), Math.max(...distribution)]);

	const duration = 200;

	let axisBottom: SVGGElement;

	let minDistribution: Tween<number>;
	let maxDistribution: Tween<number>;

	onMount(() => {
		minDistribution = new Tween(Math.min(...distribution), {
			duration: duration
		});
		maxDistribution = new Tween(Math.max(...distribution), {
			duration: duration
		});
	});


	const updating = { min: false, max: false };

	function updateAxis(minOrMax: 'min' | 'max') {
		if (!updating[minOrMax]) return;
		const extendAmount = extend ? (maxDistribution.current - minDistribution.current) * 0.05 : 0;
		x = d3.scaleLinear().range([0, width]).domain([minDistribution.current - extendAmount, maxDistribution.current + extendAmount]);
		requestAnimationFrame(() => updateAxis(minOrMax));
	}

	$: if (minDistribution) {
		updating.min = true;
		minDistribution.target = Math.min(...distribution);
		updateAxis('min');
		setTimeout(() => {
			updating.min = false;
		}, duration + 20);
	}

	$: if (maxDistribution) {
		updating.max = true;
		maxDistribution.target = Math.max(...distribution);
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