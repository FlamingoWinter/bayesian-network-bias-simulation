<button class="btn rounded-none variant-ghost-secondary ring-0 {classList}
								text-2xl py-2 text-left font-semibold text-white w-full justify-start"
				on:click={callback}>
	<slot />
</button>

<script lang="ts">
	export let callback = () => {
	};
	export let classList: string = '';
</script>