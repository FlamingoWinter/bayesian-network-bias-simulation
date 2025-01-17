<button class="btn rounded-md variant-ghost-secondary ring-0 text-xl font-oswald font-light w-full"
				on:click={callback}>
	<slot />
</button>

<script lang="ts">
	export let callback = () => {
	};
</script>