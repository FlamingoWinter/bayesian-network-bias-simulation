import * as d3 from 'd3';

interface Bar {
	category: string,
	value: number
}


export function renderCategoricalDistribution(distribution: number[],
																							categories: string[],
																							g: d3.Selection<SVGGElement, unknown, null, undefined>,
																							width: number,
																							height: number
) {
	const bars: Bar[] = Array.from(new Set(distribution)).map(num => ({
		category: categories[num],
		value: distribution.filter(d => d === num).length / distribution.length
	}));

	const x = d3.scaleBand().range([0, width]).domain(bars.map((bar: Bar) => bar.category.toString())).padding(0.2);

	const maxBarY = Math.max(...bars.map((bar: Bar) => bar.value));

	const y = d3.scaleLinear()
		.domain([0, maxBarY])
		.range([height, 0]);


	g.selectAll('.bar')
		.data(bars)
		.enter()
		.append('rect')
		.attr('rx', 2)
		.attr('x', (bar: Bar) => x(bar.category.toString()) ?? 0)
		.attr('width', x.bandwidth())
		.attr('y', y(0))
		.attr('height', 0)
		.attr('fill', '#0d3b68')
		.transition()
		.duration(750)
		.attr('y', (bar: Bar) => y(bar.value))
		.attr('height', (bar: Bar) => (height - y(bar.value)));

	g.append('g')
		.attr('transform', 'translate(0,' + height + ')')
		.call(d3.axisBottom(x))
		.selectAll('text');
	g.append('g')
		.call(d3.axisLeft(y).ticks(2));


	g.selectAll('.bar-label')
		.data(bars)
		.enter()
		.append('text')
		.attr('class', 'bar-label')
		.attr('x', (bar: Bar) => (x(bar.category.toString()) ?? 0) + x.bandwidth() / 2)
		.attr('y', y(0) + 11)
		.attr('text-anchor', 'middle')
		.style('font-size', '8px')
		.style('font-weight', '400')
		.attr('fill', (bar: Bar) => {
			const belowBarY = y(bar.value) + 11;
			return (belowBarY < y(0)) ? '#d3effb' : '#000';
		})
		.text((bar: Bar) => `≈ ${bar.value.toFixed(2)}`)
		.transition()
		.duration(750)
		.attr('y', (bar: Bar) => {
			const belowBarY = y(bar.value) + 11;
			const aboveBarY = y(bar.value) - 4;
			return (belowBarY < y(0)) ? belowBarY : aboveBarY;
		});


}
