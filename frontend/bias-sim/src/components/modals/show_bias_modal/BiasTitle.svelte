<script lang="ts">
	export let subtitle: string | undefined = undefined;
</script>

<div>
	<h3 class="inline text-2xl font-bold">
		<slot />
	</h3>
	{#if subtitle !== undefined}
		<span class="text-md text-primary-500-400-token pl-2">({subtitle})</span>
	{/if}
</div>
