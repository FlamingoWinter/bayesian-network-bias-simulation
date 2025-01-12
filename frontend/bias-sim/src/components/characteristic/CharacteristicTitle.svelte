<text x={0} y={-rectHeight /2 - 7} text-anchor="middle" fill="#333333" font-weight="600" font-size="18px">
	{toTitleCase(nodeId)}
</text>

<script lang="ts">
	import { toTitleCase } from '../../utiliites/toTitleCase.js';

	export let nodeId: string;
	export let rectHeight: number;
</script>

