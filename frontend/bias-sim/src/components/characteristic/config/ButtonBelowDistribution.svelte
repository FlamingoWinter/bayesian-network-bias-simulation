<script lang="ts">
	export let text: string;
	export let callback: () => void = () => {};
</script>

<button
	type="button"
	class="leading-0 variant-glass-primary btn btn-sm w-full px-2 pb-0.5 pt-0 font-oswald text-xs font-light"
	on:click={callback}
	on:mousedown|stopPropagation
	on:click|stopPropagation
>
	{text}
</button>
