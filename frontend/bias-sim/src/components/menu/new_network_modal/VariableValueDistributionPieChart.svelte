<script lang="ts">
	import * as d3 from 'd3';


	export let data: DataItem[];
	const width = 120;
	const height = 120;
	const radius = Math.min(width, height) / 2 - 20;
	$: color = d3.scaleOrdinal([
		'rgb(158, 177, 195)',
		'rgb(86, 118, 149)',
		'rgb(13, 59, 104)',
		'rgb(10, 44, 78)',
		'rgb(6, 29, 51)'
	]);

	$: pie = d3.pie<DataItem>().value(function(d) {
		return d.value;
	}).padAngle(0.085).sort((a, b) => d3.ascending(a.name, b.name));

	$: arcGenerator = d3.arc<d3.PieArcDatum<DataItem>>().innerRadius(20).outerRadius(radius);
	$: preparedData = pie(data);

</script>

<script lang="ts" context="module">
	export interface DataItem {
		name: string;
		value: number;
	}
</script>

<div class="flex justify-center items-center">
	<svg id="pieChart" width={width} height={height}>
		<g transform="translate({width / 2},{height / 2})">


			{#each preparedData as d, i}
				{#if d.data.value > 0.0001}
					<path d={arcGenerator(d)} fill={color(i.toString())} stroke={"#000"} stroke-width="1" />
					<text font-size="12" text-anchor="middle" class="text-center" font-family="system-ui"
								transform="translate({arcGenerator.centroid(d)[0] * 1.7}, {arcGenerator.centroid(d)[1] * 1.7})">{d.data.name}</text>
				{/if}
			{/each}
		</g>
	</svg>
</div>
