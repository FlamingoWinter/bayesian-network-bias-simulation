<!--Adapted from a ui element from here https://uiverse.io/nikk7007/chatty-bulldog-58-->

<button
	class="relative z-10 block cursor-pointer select-none overflow-hidden rounded-2xl
							border-none bg-white px-14 py-12
							text-5xl font-semibold text-secondary-500 drop-shadow-2xl"
	on:click={() => (window.location.href = '/walkthrough')}
>
	Walkthrough
	<span
		class="absolute left-0 top-0 -z-10 h-full w-full rounded-2xl border-4 border-solid border-secondary-500
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
		background: rgb(var(--color-secondary-500));
	}

	button:hover {
		transition: all 0.3s;
		color: white;
	}

	button:active span::before {
		background: black;
	}
</style>
