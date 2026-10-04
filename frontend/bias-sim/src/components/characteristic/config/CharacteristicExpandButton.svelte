<script lang="ts">
	import ArrowsAngleExpand from 'svelte-bootstrap-icons/lib/ArrowsAngleExpand.svelte';
	import { fade } from 'svelte/transition';

	export let isHovered: boolean;
	export let callbackFunction: () => void;

	let isButtonHovered: boolean = false;
</script>

{#if isHovered || isButtonHovered}
	<div class="absolute bottom-1 right-0">
		<!-- svelte-ignore a11y-mouse-events-have-key-events -->
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<div
			on:mouseover={() => (isButtonHovered = true)}
			on:mouseout={() => (isButtonHovered = false)}
			transition:fade={{ duration: 300 }}
		>
			<!-- mousedown must propagate for d3.drag; see the .filter() in forceSimulation.ts -->
			<button
				type="button"
				class="variant-filled btn-icon flex h-6 w-6 items-center justify-center p-2"
				on:click={callbackFunction}
				on:click|stopPropagation
			>
				<ArrowsAngleExpand stroke="currentColor" />
			</button>
		</div>
	</div>
{/if}
