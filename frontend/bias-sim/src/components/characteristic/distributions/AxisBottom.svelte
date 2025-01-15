<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import * as d3 from 'd3';


	export let width: number;
	export let height: number;
	export let distribution: number[];

	export let x: d3.ScaleLinear<number, number, never> = d3.scaleLinear().range([0, width]).domain([Math.min(...distribution), Math.max(...distribution)]);

	let axisBottom: SVGGElement;

	const minDistribution = new Tween(Math.min(...distribution), {
		duration: 750,
		easing: cubicOut
	});
	const maxDistribution = new Tween(Math.max(...distribution), {
		duration: 750,
		easing: cubicOut
	});


	const updating = { min: false, max: false };

	function updateAxis(minOrMax: 'min' | 'max') {
		if (!updating[minOrMax]) return;
		x = d3.scaleLinear().range([0, width]).domain([minDistribution.current, maxDistribution.current]);
		requestAnimationFrame(() => updateAxis(minOrMax));
	}

	$: {
		updating.min = true;
		minDistribution.set(Math.min(...distribution)).then(() => {
			setTimeout(() => updating.min = false, 200);
		});
		updateAxis('min');
	}

	$: {
		updating.max = true;
		maxDistribution.set(Math.max(...distribution)).then(() => {
			setTimeout(() => updating.max = false, 200);
		});
		updateAxis('max');
	}

	$: if (axisBottom && x) {
		d3.select(axisBottom).call(d3.axisBottom(x).ticks(5));
	}
</script>

<g bind:this={axisBottom} transform={`translate(0, ${height})`} />
