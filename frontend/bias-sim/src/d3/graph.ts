import type { Graph, Link, Node } from '../types/network';
import type { D3DragEvent } from 'd3';
import * as d3 from 'd3';
import { renderCategoricalDistribution } from './categoricalDistribution';
import type { NodeDistribution } from '../types/nodeDistribution';

export function renderGraph(graph: Graph, nodeDistributionByName: Record<string, NodeDistribution>,
														g: d3.Selection<SVGGElement, unknown, null, undefined>,
														width: number, height: number) {

	const simulation = d3.forceSimulation(graph.nodes)
		.force('link', d3.forceLink(graph.links).id((d: any) => d.id).distance(200).strength(0.25))
		.force('charge', d3.forceManyBody().strength(-800))
		.force('center', d3.forceCenter(width / 2, height / 2).strength(1000))
		.force('left-right', leftRightForce);

	function leftRightForce(alpha: number) {
		const strength = 30;

		graph.links.forEach((link: Link) => {
			const sourceNode = link.source as Node;
			const targetNode = link.target as Node;

			if (sourceNode.x && targetNode.x) {
				sourceNode.x -= alpha * strength;

				targetNode.x += alpha * strength;
			}
		});
	}

	const link = g.append('g')
		.selectAll('.link')
		.data(graph.links)
		.enter().append('line')
		.attr('class', 'link')
		.attr('stroke', '#aaa');

	const node = g.append('g')
		.selectAll('.node')
		.data(graph.nodes)
		.enter().append('g')
		.attr('class', 'node');

	const markers = g.append('defs').selectAll('marker')
		.data(graph.links)
		.enter().append('marker')
		.attr('id', d => `arrowhead-${d.index}`)
		.attr('viewBox', '0 -5 10 10')
		.attr('refY', 0)
		.attr('markerWidth', 15)
		.attr('markerHeight', 15)
		.attr('orient', 'auto');


	markers.append('path')
		.attr('d', 'M0,-5L10,0L0,5')
		.attr('fill', '#aaa');

	link.attr('marker-start', d => `url(#arrowhead-${d.index})`);


	const rectWidth = 160;
	const rectHeight = 120;
	node.append('svg:rect')
		.attr('rx', 2)
		.attr('ry', 2)
		.attr('width', rectWidth)
		.attr('height', rectHeight)
		.attr('fill', '#ffffff')
		.attr('stroke', '#333333')
		.attr('stroke-width', 0.7)
		.attr('x', -rectWidth / 2)
		.attr('y', -rectHeight / 2);

	node.append('svg:text')
		.attr('x', 0)
		.attr('y', -rectHeight / 2 - 10)
		.attr('text-anchor', 'middle')
		.attr('fill', '#333333')
		.attr('font-size', '12px')
		.style('font', '16px \'Helvetica Neue\'')
		.attr('font-weight', 'bold')
		.text(d => d.id);


	node.each(function(d: Node) {
		const container = d3.select(this);

		const nodeDistribution = nodeDistributionByName[d.id];
		const g = container.append('g');
		const margin = {
			top: 15,
			right: 10,
			bottom: 25,
			left: 35
		};

		if (nodeDistribution.isCategoricalVariable) {
			renderCategoricalDistribution(nodeDistribution.distribution, nodeDistribution.categoriesForCategoricalDistributions, g, rectWidth, rectHeight, margin);

		}

	});


	// node.append('foreignObject')
	// 	.attr('width', rectWidth)
	// 	.attr('height', rectHeight)
	// 	.attr('x', -rectWidth / 2)
	// 	.attr('y', -rectHeight / 2)
	// 	.append('xhtml:body')
	// 	.style('font', '14px \'Helvetica Neue\'')
	// 	.style('text-align', 'center')
	// 	.style('padding', '10px')
	// 	.html((d: Node) => `<p>${nodeDistributionByName[d.id][0]}</p>`);


	node
		.call(d3.drag<SVGGElement, Node>()
			.on('start', dragStarted)
			.on('drag', dragged)
			.on('end', dragEnded));


	simulation
		.nodes(graph.nodes)
		.on('tick', () => {
			link
				.attr('x1', (d: Link) => (d.source as Node).x!)
				.attr('y1', (d: Link) => (d.source as Node).y!)
				.attr('x2', (d: Link) => (d.target as Node).x!)
				.attr('y2', (d: Link) => (d.target as Node).y!);


			markers
				.attr('refX', d => {
					const x1 = (d.source as Node).x!;
					const y1 = (d.source as Node).y!;
					const x2 = (d.target as Node).x!;
					const y2 = (d.target as Node).y!;


					return -Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2)) / 3.3;
				});


			node
				.attr('transform', d => `translate(${d.x},${d.y})`);
		});


	function dragStarted(event: D3DragEvent<SVGRectElement, Node, Node>, d: Node) {
		if (!event.active) simulation.alphaTarget(0.3).restart();
		d.fx = d.x;
		d.fy = d.y;
	}

	function dragged(event: D3DragEvent<SVGRectElement, Node, Node>, d: Node) {
		d.fx = event.x;
		d.fy = event.y;
	}

	function dragEnded(event: D3DragEvent<SVGRectElement, Node, Node>, d: Node) {
		if (!event.active) simulation.alphaTarget(0);
		d.fx = null;
		d.fy = null;
	}

	return simulation;
}