<script lang="ts">
	import WalkthroughButton from '../components/home/WalkthroughButton.svelte';
	import VisualisationButton from '../components/home/VisualisationButton.svelte';
	import MoreInfoButton from '../components/home/MoreInfoButton.svelte';
	import { onMount } from 'svelte';
	import type { Network } from '../types/network';
	import GraphVisualisation from '../components/GraphVisualisation.svelte';

	let initialised = false;

	let innerWidth: number;
	let innerHeight: number;

	let network: undefined | Network;

	$: width = innerWidth;
	$: height = innerHeight - 4;

	onMount(async () => {
		network = await (await fetch('/example_network.json')).json() as unknown as Network;
		console.log(network);
		initialised = true;
	});
</script>

<svelte:window bind:innerWidth bind:innerHeight />


<div class="h-[100vh] w-[100vw] bg-white relative">
	<div class="relative">
		<div class="absolute h-[100vh] w-[100vw] bg-black opacity-50 z-20 pointer-events-none">
		</div>
		<div class="relative">
			{#if initialised}
				<GraphVisualisation width={width} height={height} disableInteraction={true} network={network} />
			{/if}
		</div>
	</div>

	<div
		class="absolute top-0 left-0 h-full w-full flex flex-col items-center justify-between pointer-events-none z-30">
		<div class="flex flex-col items-center">


			<div class="text-6xl font-bold text-center py-14 px-30 ">
				<h3>
					<span class="bg-white px-6 align-top pointer-events-auto rounded-t-lg">
						Using
						<span class="text-tertiary-700">Bayesian Networks</span>
						to
					</span>
				</h3>
				<h3 class="mt-5">
					<span class="bg-white px-6 pb-3 align-top pointer-events-auto rounded-lg drop-shadow-2xl">
						<span class="text-warning-600">Simulate Bias</span>
						in
						<span class="text-secondary-700">Algorithmic Recruiting</span>
					</span>
				</h3>
			</div>
			<div class="text-lg text-center max-w-[50rem] bg-white  p-4 pointer-events-auto rounded-lg drop-shadow-2xl">
				<p class="mb-2">
					Welcome!
				</p>
				<p>
					This is the accompanying visualisation and guide to a dissertation
					I wrote in my third year of undergraduate computer science for the University of
					Cambridge.
				</p>
				<p>
					This website is currently anonymised while it's marked.
				</p>
				<p class="mt-4">
					If you're unfamiliar with Bayesian Networks or fairness in machine learning, then I explain everything in the
					<span class="text-secondary-600 font-bold">Walkthrough</span> below.
				</p>
				<p class="mt-4">
					If you're looking to jump straight into trying the simulation discussed in the dissertation,
					select <span class="text-tertiary-700 font-bold">Visualisation</span>.
				</p>
			</div>
		</div>
		<div
			class="flex justify-center items-center gap-4 mb-6 pointer-events-auto  p-2 px-4">

			<MoreInfoButton />
			<WalkthroughButton />
			<VisualisationButton />
		</div>
	</div>
</div>


