import * as d3 from 'd3';

interface Bar {
	category: string,
	value: number
}

interface Margin {
	top: number,
	right: number,
	bottom: number,
	left: number
}


export function renderCategoricalDistribution(distribution: number[],
																							categories: string[],
																							g: d3.Selection<SVGGElement, unknown, null, undefined>,
																							width: number,
																							height: number,
																							margin: Margin = { top: 20, right: 10, bottom: 25, left: 35 }
) {
	const bars: Bar[] = Array.from(new Set(distribution)).map(num => ({
		category: categories[num],
		value: distribution.filter(d => d === num).length / distribution.length
	}));


	const calculatedWidth = width - margin.left - margin.right;
	const calculatedHeight = height - margin.top - margin.bottom;

	g.attr('width', width)
		.attr('height', height)
		.attr('transform',
			'translate(' + (margin.left - width / 2) + ',' + (margin.top - height / 2) + ')');


	const x = d3.scaleBand().range([0, calculatedWidth]).domain(bars.map((bar: Bar) => bar.category.toString())).padding(0.2);
	g.append('g')
		.attr('transform', 'translate(0,' + calculatedHeight + ')')
		.call(d3.axisBottom(x))
		.selectAll('text');

	const y = d3.scaleLinear()
		.domain([0, Math.max(...bars.map((bar: Bar) => bar.value))])
		.range([calculatedHeight, 0]);
	g.append('g')
		.call(d3.axisLeft(y).ticks(5));

	g.selectAll('.bar')
		.data(bars)
		.enter()
		.append('rect')
		.attr('x', (bar: Bar) => x(bar.category.toString()) ?? 0)
		.attr('y', (bar: Bar) => y(bar.value))
		.attr('width', x.bandwidth())
		.attr('height', (bar: Bar) => (calculatedHeight - y(bar.value)))
		.attr('fill', '#69b3a2');
}
