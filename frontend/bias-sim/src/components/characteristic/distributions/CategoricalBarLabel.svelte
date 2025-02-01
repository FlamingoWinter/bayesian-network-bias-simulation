<text class="bar-label"
			x={(x(bar.category.toString())?? 0) + x.bandwidth() / 2}
			y={0}
			transform={`translate(0, ${mounted? (isBelowBar ? belowBarY : aboveBarY): y(0)+11})`}
			text-anchor="middle" font-size="{fontSize}px" font-weight="400"
			fill={isBelowBar ? '#d3effb' : '#000'}
			style="transition: transform 750ms">
	{`≈ ${bar.value.toFixed(2)}`}
</text>

<script lang="ts">
	export let x: any;
	export let y: any;
	export let bar: { category: string, value: number };
	export let fontSize: number;
	export let mounted;

	$: belowBarY = y(bar.value) + 11;
	$: aboveBarY = y(bar.value) - 4;
	$: isBelowBar = (belowBarY < y(0) - 5);

	function calculateBarY(barValue: number) {
		const belowBarY = y(barValue) + 11;
		const aboveBarY = y(barValue) - 4;
		return (belowBarY < y(0) - 5) ? belowBarY : aboveBarY;
	}
</script>