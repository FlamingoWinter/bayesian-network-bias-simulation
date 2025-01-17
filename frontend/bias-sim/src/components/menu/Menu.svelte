<div class="absolute left-0 bottom-0">
	<button
		class="absolute btn left-5 bottom-5 card p-2 drop-shadow-md rounded-lg bg-surface-50-900-token"
		on:click={()=>{isOpen = !isOpen}}
	>
		<List width="28" height="28" />
	</button>

	{#if isOpen}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
		<div transition:fly={{ y: 50, duration: 400 } } on:click|stopPropagation role="alertdialog"
				 class="absolute bottom-20 left-4 p-4 card bg-surface-50-900-token w-52 min-h-80 drop-shadow-md rounded-lg flex flex-col items-center justify-start gap-2">

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


	let isOpen = false;

</script>