<div>
	<h3 class="text-2xl font-bold inline">
		<slot />
	</h3>
	{#if subtitle !== undefined}
		<span class="text-md text-primary-500-400-token pl-2">({subtitle})</span>
	{/if}

</div>

<script lang="ts">
	export let subtitle: string | undefined = undefined;
</script>