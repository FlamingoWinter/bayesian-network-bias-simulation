<button class="rounded-2xl border-none block relative bg-white cursor-pointer select-none
							py-12 px-14 text-5xl font-semibold
							overflow-hidden text-secondary-500 z-10 drop-shadow-2xl"
				on:click={() => window.location.href = '/walkthrough'}>
	Walkthrough
	<span class="rounded-2xl absolute left-0 top-0 w-full h-full bg-transparent -z-10 border-4 border-solid
							border-secondary-500"></span>
</button>

<style>
    button span::before {
        content: "";
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
