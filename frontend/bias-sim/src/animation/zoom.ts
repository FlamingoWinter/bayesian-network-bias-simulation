import * as d3 from 'd3';

type Point = {
	x: number;
	y: number;
};

export function applyZoom(
	svg: SVGElement,
	zoomGroup: SVGGElement,
	initialScale: number = 1,
	initialTranslate: Point | null = null,
	noPan: boolean = false
) {
	const zoom = d3
		.zoom<SVGElement, unknown>()
		.scaleExtent([0.2, 10])
		.on('zoom', (event) => {
			d3.select(zoomGroup).attr('transform', event.transform);
		});

	if (noPan) {
		zoom.translateExtent([
			[-800, -800],
			[2000, 1000]
		]);
	}

	const svgSelection = d3.select(svg);

	svgSelection.call(zoom);

	let initialTransform = d3.zoomIdentity.scale(initialScale);
	if (noPan) {
		initialTransform = initialTransform.translate(135, 100);
	} else if (initialTranslate !== null) {
		initialTransform = initialTransform.translate(initialTranslate.x, initialTranslate.y);
	}
	svgSelection.call(zoom.transform, initialTransform);
}
