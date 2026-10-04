<script lang="ts">
	export let text: string;
	export let callback: () => void = () => {};
</script>

<!-- mousedown must propagate for d3.drag; see the .filter() in forceSimulation.ts -->
<button
	type="button"
	class="leading-0 variant-glass-primary btn btn-sm w-full px-2 pb-0.5 pt-0 font-oswald text-xs font-light"
	on:click={callback}
	on:click|stopPropagation
>
	{text}
</button>
