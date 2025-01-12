<g>
	<path fill='#0d3b68' opacity="0.4" stroke="#0d3b68" stroke-width="1.5" stroke-opacity="1"
				bind:this={areaPath} d="" />
	<path stroke="#0d3b68" stroke-width="1.5"
				bind:this={strokePath} fill="none" d="" />
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
	import { distributionById } from '../../../stores/store';
	import { onMount } from 'svelte';

	export let nodeId: string;
	export let width: number;
	export let height: number;

	let mounted = false;
	let axisBottom: SVGGElement;
	let areaPath: SVGPathElement;
	let strokePath: SVGPathElement;

	$: distribution = $distributionById[nodeId].distribution;
	$: n = distribution.length;
	$: bandwidth = 1.4 * d3.deviation(distribution)! * Math.pow(n, -1 / 5);
	$: minValue = d3.min(distribution)!;
	$: maxValue = d3.max(distribution)!;
	$: range = maxValue - minValue;

	$: fullX = d3.scaleLinear()
		.domain([minValue - range * 0.05, maxValue + range * 0.05])
		.range([0, width]);

	$: x = d3.scaleLinear().domain([minValue, maxValue]).range([0, width]);

	$: xValues = d3.range(fullX.domain()[0], fullX.domain()[1], (fullX.domain()[1] - fullX.domain()[0]) / 100);
	$: density = kernelDensityEstimator(kernelEpanechnikov, xValues)(distribution)
		.filter((d) => d.x > minValue && d.x < maxValue);
	$: y = d3.scaleLinear()
		.domain([0, d3.max(density, d => d.y)!])
		.range([height, 0]);
	$: area = d3.area<{ x: number, y: number }>()
		.curve(d3.curveBasis).x(d => x(d.x)).y0(height).y1(d => y(d.y));
	$: line = d3.line<{ x: number, y: number }>()
		.curve(d3.curveBasis).x(d => x(d.x)).y(d => y(d.y));

	$: median = d3.median(distribution)!;


	onMount(() => {
		setTimeout(() => {
			mounted = true;
		}, 50);

		d3.select(areaPath).transition()
			.duration(1000)
			.attrTween('d', function() {
				const interpolator = d3.interpolate(
					density.map(d => ({ x: d.x, y: 0 })),
					density
				);

				return function(t) {
					return area(interpolator(t))!;
				};
			});

		d3.select(strokePath).transition()
			.duration(1000)
			.attrTween('d', function() {
				const interpolator = d3.interpolate(
					density.map(d => ({ x: d.x, y: 0 })),
					density
				);

				return function(t) {
					return area(interpolator(t))!;
				};
			});
	});

	$: if (axisBottom) {
		d3.select(axisBottom).call(d3.axisBottom(x).ticks(5));
	}

	const kernelDensityEstimator = (kernel: (u: number) => number, xValues: number[]) => {
		return (sample: number[]) =>
			xValues.map(x => ({
				x: x,
				y: d3.mean(sample, v => kernel((x - v) / bandwidth)!)!
			}));
	};

	const kernelEpanechnikov = (u: number) => {
		return Math.abs(u) <= 1 ? 0.75 * (1 - u * u) : 0;
	};

</script>