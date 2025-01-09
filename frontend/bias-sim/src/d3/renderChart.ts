import type { NodeDistribution } from '../types/nodeDistribution';
import * as d3 from 'd3';
import { renderCategoricalDistribution } from './renderCategoricalDistribution';
import { renderDiscreteDistribution } from './renderDiscreteDistribution';
import { renderContinuousDistribution } from './renderContinuousDistribution';

interface Margin {
	top: number,
	right: number,
	bottom: number,
	left: number
}

export function renderChart(nodeDistribution: NodeDistribution,
														g: d3.Selection<SVGGElement, unknown, null, undefined>,
														width: number,
														height: number,
														margin: Margin) {
	if (nodeDistribution.distributionType == 'categorical') {
		margin.left += 24;
	}


	const calculatedWidth = width - margin.left - margin.right;
	const calculatedHeight = height - margin.top - margin.bottom;

	g.attr('width', width)
		.attr('height', height)
		.attr('transform',
			'translate(' + (margin.left - width / 2) + ',' + (margin.top - height / 2) + ')');

	if (nodeDistribution.distributionType == 'categorical') {
		renderCategoricalDistribution(nodeDistribution.distribution,
			nodeDistribution.categoriesForCategoricalDistributions!,
			g,
			calculatedWidth, calculatedHeight);
	}

	if (nodeDistribution.distributionType == 'discrete') {
		renderDiscreteDistribution(nodeDistribution.distribution, g, calculatedWidth, calculatedHeight);
	}

	if (nodeDistribution.distributionType == 'continuous') {
		renderContinuousDistribution(nodeDistribution.distribution, g, calculatedWidth, calculatedHeight);
	}

}