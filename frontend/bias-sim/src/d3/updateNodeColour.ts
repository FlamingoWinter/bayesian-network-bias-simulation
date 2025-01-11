import * as d3 from 'd3';
import type { Network } from '../types/network';

export function updateNodeColour(rect: SVGRectElement, network: Network, nodeName: string) {
	d3.select(rect)
		.attr('fill', () => {
			if (network.scoreCharacteristic == nodeName) {
				return '#fffade';
			}
			if (network.applicationCharacteristics.includes(nodeName)) {
				return '#fff3fc';
			}
			return '#ffffff';
		});
}
