import type { Graph, Link, Node } from '../types/network';
import type { D3DragEvent } from 'd3';
import * as d3 from 'd3';

export function applyForceSimulation(graph: Graph,
																		 width: number, height: number,
																		 nodeGroup: SVGGElement,
																		 linkGroup: SVGGElement,
																		 markerGroup: SVGDefsElement) {
	function leftRightForce(alpha: number) {
		const strength = 20;

		graph.links.forEach((link: Link) => {
			const sourceNode = link.source as Node;
			const targetNode = link.target as Node;


			if (sourceNode.x && targetNode.x) {
				sourceNode.x -= alpha * strength;

				targetNode.x += alpha * strength;
			}
		});
	}

	function startForce(alpha: number) {
		const strength = 10 * Math.sqrt(graph.nodes.length);

		const predecessors = new Set(graph.links.map((l: Link) => l.target));

		graph.nodes.forEach((node: Node) => {
			if (!predecessors.has(node)) {
				node.x! -= alpha * strength;
			}
		});
	}


	const simulation = d3.forceSimulation(graph.nodes)
		.force('link', d3.forceLink(graph.links).id((d: any) => d.id).distance(8 * Math.sqrt(graph.nodes.length)).strength(0.1))
		.force('charge', d3.forceManyBody().strength(-300 * graph.nodes.length))
		.force('center', d3.forceCenter(width / 2, height / 2).strength(120 * graph.nodes.length))
		.force('left-right', leftRightForce)
		.force('start-force', startForce);

	simulation
		.nodes(graph.nodes)
		.on('tick', () => {
			d3.select(linkGroup)
				.selectAll('.link')
				.data(graph.links)
				.attr('x1', (d: Link) => (d.source as Node).x!)
				.attr('y1', (d: Link) => (d.source as Node).y!)
				.attr('x2', (d: Link) => (d.target as Node).x!)
				.attr('y2', (d: Link) => (d.target as Node).y!);


			d3.select(markerGroup).selectAll('.marker').data(graph.links)
				.attr('refX', d => {
					const x1 = (d.source as Node).x!;
					const y1 = (d.source as Node).y!;
					const x2 = (d.target as Node).x!;
					const y2 = (d.target as Node).y!;

					const distance = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));


					return -distance / 5.1;
				});


			d3.select(nodeGroup).selectAll('.node').data(graph.nodes)
				.attr('transform', d => `translate(${d.x},${d.y})`);
		});

	(d3.select(nodeGroup).selectAll('.node').data(graph.nodes) as d3.Selection<Element, Node, SVGGElement, unknown>)
		.call(d3.drag<Element, Node>()
			.on('start', dragStarted)
			.on('drag', dragged)
			.on('end', dragEnded));

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

function createRepelForce(selectedNode: Node, graph: Graph, strength: number, yOffset: number) {
	return (alpha: number) => {
		for (const node of graph.nodes) {
			if (node.id !== selectedNode.id) {
				const dx = node.x! - selectedNode.x!;
				const dy = node.y! - (selectedNode.y! + yOffset);
				const distance = Math.sqrt(dx * dx + dy * dy) || 1;
				const force = alpha * strength * 10_000 / (distance * distance);
				node.vx! += (dx / distance) * force;
				node.vy! += (dy / distance) * force;
			}
		}
	};
}

export function addRepelForceFromNode(selectedNode: Node, simulation: d3.Simulation<Node, undefined>, graph: Graph, strength: number, yOffset: number) {
	const repelForce = createRepelForce(selectedNode, graph, strength, yOffset);
	simulation.force(`repel-${selectedNode.id}`, repelForce);

	simulation.alpha(0.1).restart();
}

export function removeRepelForce(selectedNode: Node, simulation: d3.Simulation<Node, undefined>) {
	simulation.force(`repel-${selectedNode.id}`, null);

	simulation.alpha(0.1).restart();
}