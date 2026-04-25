<script lang="ts">
	import { tweened } from 'svelte/motion';
	import * as d3 from 'd3';

	export let height: number;
	export let maxBarY: number = 0;
	export let display: boolean;

	export let y: d3.ScaleLinear<number, number, never> = d3
		.scaleLinear()
		.domain([0, maxBarY])
		.range([height, 0]);

	const duration = 200;

	let axisLeft: SVGGElement;

	const maxBarYTween = tweened(maxBarY, { duration });

	let updating = false;

	function updateAxis() {
		if (!updating) return;
		y = d3.scaleLinear().domain([0, maxBarY]).range([height, 0]);
		requestAnimationFrame(updateAxis);
	}

	$: {
		updating = true;
		maxBarYTween.set(maxBarY);
		updateAxis();
		setTimeout(() => {
			updating = false;
		}, duration + 20);
	}

	$: if (axisLeft && y) {
		d3.select(axisLeft).transition().call(d3.axisLeft(y).ticks(2));
	}
</script>

{#if display}
	<g bind:this={axisLeft} />
{/if}
