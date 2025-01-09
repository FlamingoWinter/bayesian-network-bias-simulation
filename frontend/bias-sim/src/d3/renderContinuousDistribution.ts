import * as d3 from 'd3';

export function renderContinuousDistribution(distribution: number[],
																						 g: d3.Selection<SVGGElement, unknown, null, undefined>,
																						 width: number,
																						 height: number,
																						 bandwidth: number | null = null
) {
	const n = distribution.length;
	if (bandwidth === null) {
		bandwidth = 1.4 * d3.deviation(distribution)! * Math.pow(n, -1 / 5);
	}

	const minValue = d3.min(distribution)!;
	const maxValue = d3.max(distribution)!;
	const range = maxValue - minValue;

	const fullX = d3.scaleLinear()
		.domain([minValue - range * 0.05, maxValue + range * 0.05])
		.range([0, width]);

	const x = d3.scaleLinear()
		.domain([minValue, maxValue])
		.range([0, width]);

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


	const xValues = d3.range(fullX.domain()[0], fullX.domain()[1], (fullX.domain()[1] - fullX.domain()[0]) / 100);
	const density = kernelDensityEstimator(kernelEpanechnikov, xValues)(distribution)
		.filter((d) => d.x > minValue && d.x < maxValue);

	const y = d3.scaleLinear()
		.domain([0, d3.max(density, d => d.y)!])
		.range([height, 0]);

	const area = d3.area<{ x: number, y: number }>()
		.curve(d3.curveBasis)
		.x(d => x(d.x))
		.y0(height)
		.y1(d => y(d.y));

	const areaPath = g.append('path')
		.datum(density.map(d => ({ x: d.x, y: 0 })))
		.attr('fill', '#0d3b68')
		.attr('opacity', 0.4)
		.attr('d', area);

	areaPath.transition()
		.duration(750)
		.attrTween('d', function() {
			const interpolator = d3.interpolate(
				density.map(d => ({ x: d.x, y: 0 })),
				density
			);

			return function(t) {
				return area(interpolator(t))!;
			};
		});

	const median = d3.median(distribution)!;

	g.append('text')
		.attr('class', 'bar-label')
		.attr('x', x(median))
		.attr('y', y(0) + 11)
		.attr('text-anchor', 'middle')
		.style('font-size', '8px')
		.style('font-weight', '400')
		.attr('fill', '#000')
		.text(`${median.toPrecision(2)}`)
		.transition()
		.duration(750)
		.attr('y', -4);


	const line = d3.line<{ x: number, y: number }>()
		.curve(d3.curveBasis)
		.x(d => x(d.x))
		.y(d => y(d.y));

	const linePath = g.append('path')
		.datum(density.map(d => ({ x: d.x, y: 0 })))
		.attr('fill', 'none')
		.attr('stroke', '#0d3b68')
		.attr('stroke-width', 1.5)
		.attr('d', line);

	linePath.transition()
		.duration(750)
		.attrTween('d', function() {
			const interpolator = d3.interpolate(
				density.map(d => ({ x: d.x, y: 0 })),
				density
			);

			return function(t) {
				return area(interpolator(t))!;
			};
		});


	g.append('g')
		.attr('transform', 'translate(0,' + height + ')')
		.call(d3.axisBottom(x).ticks(5));


}
