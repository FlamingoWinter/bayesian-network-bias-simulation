<script lang="ts">
	import { biasAnalysis } from '../../stores/store';
	import BottomHrefButtons from './BottomHrefButtons.svelte';
	import TopUtilityButtons from './TopUtilityButtons.svelte';
	import type { Network } from '../../types/network';

	let showBias: boolean = false;
	export let network: Network;

	$: if (network.characteristics) {
		showBias = ($biasAnalysis !== undefined);
	}

	const menu = {
		'Motivation': [],
		'Simulation': [],
		'Bayesian Networks': [
			'Generating a Random Network',
			'Sampling from a Network',
			'Labelling Networks'
		],
		'Training Recruiters': [
			'Random Forest',
			'Logistic Regression',
			'Support Vector Machine',
			'Shallow MLP',
			'Deep MLP',
			'Encoder-Only Transformer',
			'Bayesian Recruiter'
		],
		'Measuring Bias': [
			'Demographic Parity',
			'Equalised Odds',
			'Predictive Parity'
		],
		'Recruiter Mitigations': [
			'Satisfy Demographic Parity',
			'Satisfy Proportional Parity',
			'Optimise for Predictive Parity',
			'Optimise for Equalised Odds'
		],
		'Experiments': [
			'Comparing Input Conditions',
			'Comparing Recruiter Mitigations'
		],
		'Results': [
			'Comparing Input Conditions',
			'Effect of Competence Disparity',
			'Comparing Recruiters',
			'Accuracy and Bias',
			'Agreement between Bias Metrics',
			'Affect of Mitigations'
		],
		'Tools Used': [
			'Backend',
			'Frontend'
		]
	};

	function toSnakeCase(str: string) {
		return str.toLowerCase().replace(/\s+/g, '_');
	}

	const utilityButtonInfos = Object.entries(menu).flatMap(([title, children]) => [
		{
			name: title, callback: () => window.location.href = '/guide/' + toSnakeCase(title), textSize: 'text-2xl'
		},
		...children.map(child => ({
			name: child,
			callback: () => window.location.href = '/guide/' + toSnakeCase(child),
			inset: 'pl-8',
			textSize: 'text-md font-medium'
		}))
	]);

</script>
<div class="absolute bg-black w-[20rem] h-full pt-2">
	<div class="flex flex-col justify-between items-start h-full">


		<div class="w-full pr-4 overflow-y-auto pl-2 hide-scrollbar flex flex-col gap-2">
			<button
				class="btn text-white w-full justify-start text-5xl font-bold p-4"
				on:click={() => window.location.href = '/guide'}>
				Guide
			</button>
			<TopUtilityButtons utilityButtonInfos={utilityButtonInfos} />
		</div>

		<div class="pt-2">
			<BottomHrefButtons buttonInfos={[
			{name: "Walkthrough", slug: "/walkthrough"},
			{name: "Visualisation", slug: "/visualisation"},
		]} />
		</div>
	</div>
</div>