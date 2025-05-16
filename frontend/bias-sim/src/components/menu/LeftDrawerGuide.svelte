<script lang="ts">
	import BottomHrefButtons from './BottomHrefButtons.svelte';
	import TopUtilityButtons from './TopUtilityButtons.svelte';


	const menu = {
		'Motivation': [],
		'Related Work': [],
		'Tools Used': [],
		'Preliminaries': [
			'Binary Classification',
			'Fairness Criteria',
			'Directed Acyclic Graphs',
			'Bayesian Networks'
		],
		'The Simulation': [
			'Mathematical Design',
			'The Applicant Distribution',
			'A Run of the Simulation',
			'Generating a Bayesian Network',
			'Generating Applications',
			'Recruiters',
			'Measuring Bias',
			'Applying Post-Training Mitigations'
		],
		'The Experiment': [],
		'Results and Findings': [
			'Assumptions Analysis',
			'Research Implications'
		]
	};

	function toSnakeCase(str: string) {
		return str.toLowerCase().replace(/\s+/g, '_');
	}

	const utilityButtonInfos = Object.entries(menu).flatMap(([title, children]) => [
		{
			name: title, callback: () => window.location.href = '/guide/' + toSnakeCase(title), textSize: 'text-xl',
			inset: 'pr-4'
		},
		...children.map(child => ({
			name: child,
			callback: () => window.location.href = '/guide/' + toSnakeCase(child),
			inset: 'pl-8',
			textSize: 'text-sm font-medium'
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