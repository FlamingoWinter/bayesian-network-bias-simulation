<script lang="ts">
	export let title: string;
	export let value: number;
	export let toFixed: boolean = true;
</script>

<h3 class="text-sm">
	<span class="text-base font-bold">
		{title}
	</span>
	{toFixed ? value.toFixed(3) : value}
</h3>
