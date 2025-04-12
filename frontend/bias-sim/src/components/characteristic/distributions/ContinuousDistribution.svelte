<g>
	<path fill={calculateDistributionFill(probabilityType)} opacity="0.4" stroke-width="1.5"
				stroke-opacity="1"
				bind:this={areaPath} d=""
				style="transition: fill {defaultTransition}" />
	<path stroke={calculateDistributionFill(probabilityType)} stroke-width="1.5"
				bind:this={strokePath} fill="none" d="" style="transition: stroke {defaultTransition}" />
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
	<AxisBottom bind:x={x} height={height} width={width} distribution={distribution} />
	<AxisBottom bind:x={fullX} extend={true} display={false} height={height} width={width} distribution={distribution} />

	<AxisLeft bind:y={y} height={height} maxBarY={maxBarY} display={false} />
</g>


<script lang="ts">
	import * as d3 from 'd3';
	import { onMount } from 'svelte';
	import type { Characteristic } from '../../../types/network';
	import { calculateDistributionFill } from './calculateDistributionFill';
	import AxisLeft from './AxisLeft.svelte';
	import AxisBottom from './AxisBottom.svelte';
	import { defaultTransition } from '../../../animation/transition';

	export let characteristic: Characteristic;
	export let width: number;
	export let height: number;
	export let conditions: Record<string, number>;
	export let conditioned: boolean;
	export let posteriorDistributions: Record<string, number[]>;

	let mounted = false;
	let axisBottom: SVGGElement;
	let areaPath: SVGPathElement;
	let strokePath: SVGPathElement;
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

	$: n = distribution.length;
	$: bandwidth = 1.4 * d3.deviation(distribution)! * Math.pow(n, -1 / 5);
	$: minValue = d3.min(distribution)!;
	$: maxValue = d3.max(distribution)!;

	$: xValues = d3.range(fullX.domain()[0], fullX.domain()[1], (fullX.domain()[1] - fullX.domain()[0]) / 100);
	$: density = kernelDensityEstimator(kernelEpanechnikov, xValues)(distribution)
		.filter((d) => d.x > minValue && d.x < maxValue);
	$: maxBarY = d3.max(density, d => d.y)!;

	let fullX = d3.scaleLinear()
		.domain([0, 0])
		.range([0, 0]);
	let x = d3.scaleLinear().domain([0, 0]).range([0, 0]);
	let y = d3.scaleLinear()
		.domain([0, 0])
		.range([0, 0]);

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