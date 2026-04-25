<script lang="ts">
	import BottomHrefButtons from './BottomHrefButtons.svelte';
	import TopUtilityButtons from './TopUtilityButtons.svelte';

	const menu = {
		Motivation: [],
		'Related Work': [],
		'Tools Used': [],
		Preliminaries: [
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
		'Results and Findings': ['Assumptions Analysis', 'Research Implications']
	};

	function toSnakeCase(str: string) {
		return str.toLowerCase().replace(/\s+/g, '_');
	}

	const utilityButtonInfos = Object.entries(menu).flatMap(([title, children]) => [
		{
			name: title,
			callback: () => (window.location.href = '/guide/' + toSnakeCase(title)),
			textSize: 'text-xl',
			inset: 'pr-4'
		},
		...children.map((child) => ({
			name: child,
			callback: () => (window.location.href = '/guide/' + toSnakeCase(child)),
			inset: 'pl-8',
			textSize: 'text-sm font-medium'
		}))
	]);
</script>

<div class="absolute h-full w-[20rem] bg-black pt-2">
	<div class="flex h-full flex-col items-start justify-between">
		<div class="hide-scrollbar flex w-full flex-col gap-2 overflow-y-auto pl-2 pr-4">
			<button
				class="btn w-full justify-start p-4 text-5xl font-bold text-white"
				on:click={() => (window.location.href = '/guide')}
			>
				Guide
			</button>
			<TopUtilityButtons {utilityButtonInfos} />
		</div>

		<div class="pt-2">
			<BottomHrefButtons
				buttonInfos={[
					{ name: 'Walkthrough', slug: '/walkthrough' },
					{ name: 'Visualisation', slug: '/visualisation' }
				]}
			/>
		</div>
	</div>
</div>
