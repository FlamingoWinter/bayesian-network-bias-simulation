<rect rx="2" ry="2" width={width} height={expanded ? height * heightMultiplier : height}
			stroke="#333333" stroke-width="0.7"
			x={-width/2} y={-height/2}
			fill={fill}
			style="transition: height {defaultTransition}" />


<script lang="ts">
	import { defaultTransition } from '../../animation/transition';
	import type { Network } from '../../types/network';

	export let width: number;
	export let height: number;
	export let expanded: boolean;
	export let nodeId: string;
	export let heightMultiplier: number;
	export let network: Network;
	export let scoreAndApplication: boolean = false;

	let fill: string;

	$: if (network) {
		fill = calculateRectangleFill(nodeId, network.scoreCharacteristic, network.applicationCharacteristics);
	}

	function calculateRectangleFill(characteristic: string,
																	scoreCharacteristic: string,
																	applicationCharacteristics: string[]) {
		if (!scoreAndApplication) {
			return '#ffffff';

		}

		if (characteristic == scoreCharacteristic) {
			return '#fff1a1';
		}
		if (applicationCharacteristics.includes(characteristic)) {
			return '#ffa5e9';
		}
		return '#ffffff';
	}
</script>

