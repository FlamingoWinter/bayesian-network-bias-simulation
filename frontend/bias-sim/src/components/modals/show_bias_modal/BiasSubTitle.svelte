<h3 class="text-sm">
	<span class="font-bold text-base">
		{title}
	</span>
	{toFixed ? value.toFixed(3) : value}
</h3>

<script lang="ts">
	export let title: string;
	export let value: number;
	export let toFixed: boolean = true;
</script>