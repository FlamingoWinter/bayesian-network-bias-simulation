<rect rx="2" ry="2" width={width} height={expanded ? height * heightMultiplier : height}
			stroke="#333333" stroke-width="0.7"
			x={-width/2} y={-height/2}
			fill={calculateRectangleFill(nodeId, $network.scoreCharacteristic, $network.applicationCharacteristics)}
			style="transition: height {defaultTransition}" />


<script lang="ts">
	import { defaultTransition } from '../../animation/transition';
	import { network } from '../../stores/store';

	export let width: number;
	export let height: number;
	export let expanded: boolean;
	export let nodeId: string;
	export let heightMultiplier: number;


	function calculateRectangleFill(characteristic: string,
																	scoreCharacteristic: string,
																	applicationCharacteristics: string[]) {
		if (characteristic == scoreCharacteristic) {
			return '#fffade';
		}
		if (applicationCharacteristics.includes(characteristic)) {
			return '#fff3fc';
		}
		return '#ffffff';
	}
</script>

