{#if isHovered || isButtonHovered}


	<!-- svelte-ignore a11y-mouse-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div
		on:mouseover={() => isButtonHovered = true}
		on:mouseout={() => isButtonHovered = false}
		transition:fade={{ duration: 300 }}
	>
		<button
			type="button"
			class="btn-icon variant-filled p-2 w-6 h-6 flex items-center justify-center"
			on:mousedown|stopPropagation
			on:click={callbackFunction}

			on:click|stopPropagation
		>
			<ArrowsAngleExpand
				stroke="currentColor"
			/>
		</button>
	</div>
{/if}

<script lang="ts">
	import ArrowsAngleExpand from 'svelte-bootstrap-icons/lib/ArrowsAngleExpand.svelte';
	import { fade } from 'svelte/transition';


	export let isHovered: boolean;
	export let callbackFunction: () => void;

	let isButtonHovered: boolean = false;
</script>
