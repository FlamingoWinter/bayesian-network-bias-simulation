<!--Adapted from a ui element from here https://uiverse.io/nikk7007/chatty-bulldog-58-->

<script lang="ts">
	export let center: boolean = false;
</script>

<button class="rounded-2xl border-none block relative bg-white cursor-pointer select-none
							py-6 px-10 text-2xl font-semibold h-fit
							overflow-hidden text-warning-600 z-10 {center ? '' : 'mr-auto flex-grow basis-0'} drop-shadow-2xl"
				on:click={() => window.location.href = '/guide'}>
	More Information
	<span class="rounded-2xl absolute left-0 top-0 w-full h-full bg-transparent -z-10 border-4 border-solid
							border-warning-600"></span>
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
        background: rgb(var(--color-warning-600));
    }

    button:hover {
        transition: all 0.3s;
        color: white;
    }


    button:active span::before {
        background: black;
    }

</style>
