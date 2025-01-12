import * as d3 from 'd3';

export function applyZoom(svg: SVGElement, zoomGroup: SVGGElement) {
	d3.select(svg).call(d3.zoom<SVGElement, unknown>()
		.scaleExtent([0.5, 5])
		.on('zoom', (event) => {
			d3.select(zoomGroup).attr('transform', event.transform);
		}));
}