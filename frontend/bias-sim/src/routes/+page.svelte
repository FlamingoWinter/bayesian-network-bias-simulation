<script lang="ts">
	import WalkthroughButton from '../components/home/WalkthroughButton.svelte';
	import VisualisationButton from '../components/home/VisualisationButton.svelte';
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
		network = (await (await fetch('/example_network.json')).json()) as unknown as Network;
		initialised = true;
	});
</script>

<svelte:window bind:innerWidth bind:innerHeight />

<div class="relative h-[100vh] w-[100vw] bg-white">
	<div class="relative">
		<div class="pointer-events-none absolute z-20 h-[100vh] w-[100vw] bg-black opacity-50"></div>
		<div class="relative">
			{#if initialised}
				<GraphVisualisation {width} {height} disableInteraction={true} {network} />
			{/if}
		</div>
	</div>

	<div
		class="pointer-events-none absolute left-0 top-0 z-30 flex h-full w-full flex-col items-center justify-between"
	>
		<div class="flex flex-col items-center">
			<div class="px-30 py-14 text-center text-6xl font-bold">
				<h3>
					<span class="pointer-events-auto rounded-t-lg bg-white px-6 align-top">
						Using
						<span class="text-tertiary-700">Bayesian Networks</span>
						to
					</span>
				</h3>
				<h3 class="mt-5">
					<span class="pointer-events-auto rounded-lg bg-white px-6 pb-3 align-top drop-shadow-2xl">
						<span class="text-warning-600">Simulate Bias</span>
						in
						<span class="text-secondary-700">Algorithmic Recruiting</span>
					</span>
				</h3>
			</div>
			<div
				class="pointer-events-auto max-w-[50rem] rounded-lg bg-white p-4 text-center text-lg drop-shadow-2xl"
			>
				<p class="mb-2">Welcome!</p>
				<p>
					This is the accompanying visualisation and guide to a dissertation I wrote in my third
					year of undergraduate computer science for the University of Cambridge.
				</p>
				<p>This website is currently anonymised while it's marked.</p>
				<p class="mt-4">
					If you're unfamiliar with Bayesian Networks or fairness in machine learning, then I
					explain everything in the
					<span class="font-bold text-secondary-600">Walkthrough</span> below.
				</p>
				<p class="mt-4">
					If you're looking to jump straight into trying the simulation discussed in the
					dissertation, select <span class="font-bold text-tertiary-700">Visualisation</span>.
				</p>
			</div>
		</div>
		<div class="pointer-events-auto mb-6 flex items-center justify-center gap-4 p-2 px-4">
			<WalkthroughButton />
			<VisualisationButton />
		</div>
	</div>
</div>
