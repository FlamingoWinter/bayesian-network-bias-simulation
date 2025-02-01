<div class="absolute left-0 bottom-0">
	<!-- svelte-ignore a11y-mouse-events-have-key-events -->
	<button
		class="absolute btn left-5 bottom-5 card p-2 drop-shadow-md rounded-lg bg-surface-50-900-token"
		on:click={()=>{isOpen = !isOpen}}
		on:mouseover={() => {isHovered = true}}
		on:mouseleave={() => {isHovered = false}}
	>
		<List width="28" height="28" />
	</button>

	{#if isOpen}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
		<!-- svelte-ignore a11y-mouse-events-have-key-events -->
		<div transition:fly={{ y: 50, duration: 400 } } on:click|stopPropagation role="alertdialog"
				 on:mouseover={() => {isHovered = true}}
				 on:mouseleave={() => {isHovered = false}}
				 class="absolute bottom-20 left-4 p-4 card bg-surface-50-900-token w-52 min-h-80 drop-shadow-md rounded-lg flex flex-col items-center justify-start gap-2">

			<MenuButton callback={()=>{}}>
				New Network...
			</MenuButton>
			{#if $conditioned}
				<MenuButton callback={$deconditionAll}>
					Decondition all
				</MenuButton>

			{/if}


		</div>
	{/if}
</div>

<script lang="ts">
	import List from 'svelte-bootstrap-icons/lib/List.svelte';
	import { fly } from 'svelte/transition';
	import MenuButton from './MenuButton.svelte';
	import { conditioned } from '../../stores/store';
	import { deconditionAll } from '../../stores/functions';
	import { onDestroy, onMount } from 'svelte';

	let isHovered: boolean = false;
	let isOpen = false;

	const handleClickOutside = (event: MouseEvent) => {
		if (!isHovered && isOpen) {
			isOpen = false;
		}

	};

	onMount(() => {
		document.addEventListener('click', handleClickOutside);
	});
	onDestroy(() => {
		document.removeEventListener('click', handleClickOutside);
	});

</script>