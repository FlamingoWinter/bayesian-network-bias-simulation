<!--Adapted from a ui element from here https://uiverse.io/nikk7007/chatty-bulldog-58-->

<script lang="ts">
	export let center: boolean = false;
</script>

<button
	class="relative z-10 block h-fit cursor-pointer select-none overflow-hidden
							rounded-2xl border-none bg-white px-10 py-10
							text-2xl font-semibold text-tertiary-700 {center
		? ''
		: 'ml-auto flex-grow basis-0'} drop-shadow-2xl"
	on:click={() => (window.location.href = '/visualisation')}
>
	Visualisation
	<span
		class="absolute left-0 top-0 -z-10 h-full w-full rounded-2xl border-4 border-solid border-tertiary-700
							bg-transparent"
	></span>
</button>

<style>
	button span::before {
		content: '';
		display: block;
		position: absolute;
		width: 0;
		height: 500%;
		background: var(--lightgray);
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%) rotate(-60deg);
		transition: all 0.3s;
	}

	button:hover span::before {
		transform: translate(-50%, -50%) rotate(-90deg);
		width: 100%;
		background: rgb(var(--color-tertiary-700));
	}

	button:hover {
		transition: all 0.3s;
		color: white;
	}

	button:active span::before {
		background: black;
	}
</style>
