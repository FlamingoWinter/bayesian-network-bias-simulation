<script lang="ts">
	export let text: string;
	export let callback: () => void = () => {
	};
</script>


<button
	type="button"
	class="btn btn-sm variant-ghost w-full px-2 pt-0 pb-0.5 text-xs font-oswald font-light leading-0"
	on:mousedown|stopPropagation
	on:click|stopPropagation
	on:click={callback}
>
	{text}
</button>