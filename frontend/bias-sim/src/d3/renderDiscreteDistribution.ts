import * as d3 from 'd3';

interface Bar {
	x: number,
	y: number
}


export function renderDiscreteDistribution(distribution: number[],
																					 g: d3.Selection<SVGGElement, unknown, null, undefined>,
																					 width: number,
																					 height: number,
																					 barWidth: number | null = null,
																					 useHistogram: boolean = true
) {
	const minValue = d3.min(distribution)!;
	const maxValue = d3.max(distribution)!;
	if (barWidth === null) {
		if (!useHistogram) {
			barWidth = 1;
		} else {
			barWidth = d3.tickStep(0, maxValue - minValue, 20);
		}
	}

	const binStart = Math.floor(minValue / barWidth) * barWidth;
	const bins = Array.from({ length: Math.ceil((maxValue - minValue) / barWidth) }, (_, i) => [
		binStart + i * barWidth,
		binStart + (i + 1) * barWidth
	]);

	let bars: Bar[];

	if (useHistogram) {
		bars = bins.map(([start, end]) => {
			return {
				x: start,
				y: distribution.filter(d => d >= start && d < end).length
			};
		});
	} else {
		bars = Array.from(new Set(distribution)).map(num => ({
			x: num,
			y: distribution.filter(d => d === num).length
		}));
	}


	const x = d3.scaleLinear()
		.range([0, width])
		.domain([Math.min(...distribution), Math.max(...distribution)]);

	const maxBarY = Math.max(...bars.map((bar: Bar) => bar.y));

	const y = d3.scaleLinear()
		.domain([0, maxBarY])
		.range([height, 0]);


	g.selectAll('.bar')
		.data(bars)
		.enter()
		.append('rect')
		.attr('rx', 2)
		.attr('x', (bar: Bar) => x(bar.x))
		.attr('width', (x(barWidth) - x(0)) * 0.9)
		.attr('y', y(0))
		.attr('height', 0)
		.attr('fill', '#0d3b68')
		.transition()
		.duration(750)
		.attr('y', (bar: Bar) => y(bar.y))
		.attr('height', (bar: Bar) => (height - y(bar.y)));

	g.append('g')
		.attr('transform', 'translate(0,' + height + ')')
		.call(d3.axisBottom(x).ticks(5))
		.selectAll('text');

	const median = d3.median(distribution)!;

	g.append('text')
		.attr('class', 'bar-label')
		.attr('x', x(median))
		.attr('y', y(0) - 10)
		.attr('text-anchor', 'middle')
		.style('font-size', '8px')
		.style('font-weight', '400')
		.attr('fill', '#000')
		.text(`${median.toPrecision(2)}`)
		.transition()
		.duration(750)
		.attr('y', -4);

}
