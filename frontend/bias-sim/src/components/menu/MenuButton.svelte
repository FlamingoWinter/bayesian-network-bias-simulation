<script lang="ts">
	export let callback = () => {};
	export let classList: string = '';
</script>

<button
	class="variant-ghost-secondary btn rounded-none ring-0 {classList}
								w-full justify-start py-2 text-left text-2xl font-semibold text-white"
	on:click={callback}
>
	<slot />
</button>
