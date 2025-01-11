import type { Link, Network, Node } from '../types/network';
import type { D3DragEvent } from 'd3';
import * as d3 from 'd3';
import type { NodeDistribution } from '../types/nodeDistribution';
import { toTitleCase } from '../utiliites/toTitleCase';
import { renderChart } from './renderChart';
import { mount } from 'svelte';
import NodeComponent from '../components/NodeComponent.svelte';
import { updateNodeColour } from './updateNodeColour';

export function renderGraph(network: Network, nodeDistributionByName: Record<string, NodeDistribution>,
														g: d3.Selection<SVGGElement, unknown, null, undefined>,
														width: number, height: number) {
	const graph = network.graph;
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

	const innerNodeByNodeIndex: Record<number, SVGGElement> = {};
	const rectNodeByNodeIndex: Record<number, SVGRectElement> = {};


	const node = g.append('g')
		.selectAll('.node')
		.data(graph.nodes)
		.enter().append('g')
		.attr('class', 'node');


	const innerNode = node.append('g')
		.attr('class', 'innerNode')
		.each(function(_, index) {
			innerNodeByNodeIndex[index] = this as SVGGElement;
		})
		.style('transition', 'transform 500ms cubic-bezier(0.68, -0.55, 0.27, 1.55)');


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

	innerNode.append('svg:rect')
		.attr('rx', 2)
		.attr('ry', 2)
		.attr('width', rectWidth)
		.attr('height', rectHeight)
		.attr('stroke', '#333333')
		.attr('stroke-width', 0.7)
		.attr('x', -rectWidth / 2)
		.attr('y', -rectHeight / 2)
		.each(function(_, index) {
			rectNodeByNodeIndex[index] = this as SVGRectElement;
		})
		.each(function(node) {
			updateNodeColour(
				this as SVGRectElement, network, node.id
			);
		})
		.style('transition', 'height 500ms cubic-bezier(0.68, -0.55, 0.27, 1.55), fill 300ms');
	;


	innerNode.append('svg:text')
		.attr('x', 0)
		.attr('y', -rectHeight / 2 - 7)
		.attr('text-anchor', 'middle')
		.attr('fill', '#333333')
		.style('font-weight', '600')
		.style('font-size', '18px')
		.text(d => toTitleCase(d.id));


	innerNode.each(function(d: Node) {
		const container = d3.select(this);

		const nodeDistribution = nodeDistributionByName[d.id];
		const g = container.append('g');

		const margin = {
			top: 15,
			right: 14,
			bottom: 25,
			left: 14
		};

		renderChart(nodeDistribution, g, rectWidth, rectHeight, margin);

	});


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

	const foreignObjectWidth = rectWidth * 1.1;
	const foreignObjectHeight = rectHeight * 1.2;
	innerNode.append('foreignObject')
		.attr('class', 'expand-button-container')
		.attr('x', -foreignObjectWidth / 2)
		.attr('y', -foreignObjectHeight / 2)
		.attr('width', foreignObjectWidth)
		.attr('height', foreignObjectHeight)
		.style('pointer-events', 'all')
		.style('z-index', 20)
		.style('transition', 'height 500ms cubic-bezier(0.68, -0.55, 0.27, 1.55)')
		.each(function(node, index) {
			const nodeComponent = mount(NodeComponent, {
				target: this,
				props: {
					'foreignObjectElement': this,
					'innerNode': innerNodeByNodeIndex[index],
					'rect': rectNodeByNodeIndex[index],
					'nodeName': node.id
				}
			});
		});

	return simulation;
}