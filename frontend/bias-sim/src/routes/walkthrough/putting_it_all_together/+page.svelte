<script lang="ts">
	import { Tab, TabGroup } from '@skeletonlabs/skeleton';
	import type { Network } from '../../../types/network';
	import { onMount } from 'svelte';
	import GraphVisualisation from '../../../components/GraphVisualisation.svelte';
	import { CaretRightFill } from 'svelte-bootstrap-icons';

	type TabInfo = {
		network: Network;
	}
	let tabInfos: Record<string, TabInfo> | undefined = undefined;
	let tabSet: string = '1 - Omit Protected Characteristic';

	let innerWidth: number;
	let innerHeight: number;

	$: width = innerWidth - 200;
	$: height = innerHeight - 100;

	onMount(async () => {
		tabInfos = {
			'1 - Omit Protected Characteristic': { network: await (await fetch('/condition_1.json')).json() as unknown as Network },
			'2 - Include Protected Characteristic': { network: await (await fetch('/condition_2.json')).json() as unknown as Network },
			'3 - Include Proxy Characteristics': { network: await (await fetch('/condition_3.json')).json() as unknown as Network },
			'4 - Omit Distant Proxy Characteristics': { network: await (await fetch('/condition_4.json')).json() as unknown as Network }
		};
	});


</script>

<svelte:window bind:innerWidth bind:innerHeight />


<h3 class="text-6xl font-bold mt-2 p-8">
	Putting it all Together!
</h3>
<div class="flex justify-center pt-10 pb-10 text-center">
	<div class="text-lg max-w-[40rem] flex flex-col items-center">
		<p class="mt-12">
			Now we've motivated each part of the project, we can explain what happens on each run of the simulation.
			This whole process is repeated thousands of times.
		</p>

		<ol class="list-decimal list-inside ml-10 text-lg text-left space-y-4 mt-16 min-w-[40rem]">
			<li>
				We generate a random <span class="text-surface-600 font-bold">Bayesian Network</span> with 80 nodes.
				This will be our <span class="text-surface-600 font-bold">Applicant Distribution</span> for this run.
			</li>
			<li>
				One of those characteristics is labelled as the
				<span class="text-surface-600 font-bold">Protected Characteristic</span>, and a distant characteristic
				is labelled as the
				<span class="text-surface-600 font-bold">Competency Characteristic</span>.
			</li>
			<li>
				We generate a list of 10,000 <span class="text-surface-600 font-bold">Applicants</span> as
				samples from that Bayesian network.
			</li>
			<li>
				Each applicant reveals only some of its characteristics
				to form an <span class="text-surface-600 font-bold">Application</span>.
			</li>
			<li>
				We split the Applicants into a <span class="text-surface-600 font-bold">Training Set</span> and a
				<span class="text-surface-600 font-bold">Testing Set</span>.
			</li>
			<li>
				We train each recruiter on the training examples. Each example includes
				the application and the applicant's actual competence.
			</li>
			<li>
				We ask each trained recruiter to use each application in the testing set to make a decision.
			</li>
			<li>
				For each recruiter, we measure and record how biased those decisions are.
			</li>
		</ol>

		<p class="mt-24">
			There are some things we can modify in this simulation.
		</p>

		<p class="mt-24">
			First, we can modify the <span class="text-surface-600 font-bold">
			Recruiter
			</span>. We discussed how we could apply the
			Random Forest machine-learning model to this problem,
			but there are many models we can try.
		</p>
		<p class="mt-4">
			In this project, we're not so concerned with demonstrating which ones are absolutely less biased,
			as we can guess that this will depend on the specific problem we're trying to solve.
			Rather, we are concerned if there <i>are</i> differences in the amount of bias exhibited
			by different recruiters.
		</p>

		<p class="mt-24">
			Next, we can modify <span class="text-surface-600 font-bold">
			How an Application is Created from an Applicant
			</span>.
			There are four different ideas we try here:
		</p>

		<p class="mt-8 text-left">
			Each Applicant reveals the same set of 10 randomly selected characteristics, where...
		</p>
		<ol class="list-decimal list-inside ml-10 text-lg text-left space-y-4 min-w-[40rem] mt-4">
			<li>
				...this <i>doesn't</i> include the <span class="text-surface-600 font-bold">Protected Characteristic</span>.
			</li>
			<li>
				...this <i>does</i> include the Protected Characteristic.
			</li>
			<li>
				...this includes five <span class="text-surface-600 font-bold">Proxy Characteristics</span>
				(characteristics which are <i>directly</i>
				linked to the Protected Characteristic on the Bayesian Network).
			</li>
			<li>
				...this doesn't include <i>any</i> <span
				class="text-surface-600 font-bold">Distant Proxy Characteristics</span>
				(characteristics
				linked to the Protected Characteristic <i>by one or two edges</i> on the Bayesian Network).
			</li>
		</ol>
		<p class="mt-8">
			Here's an example of what this looks like.
			<span
				class="text-pink-500 font-bold">Pink characteristics are the only characteristics included in the application:
			</span>
		</p>
		{#if tabInfos !== undefined}

			<TabGroup class="px-8 flex-grow mt-8" justify="flex-wrap">
				{#each Object.keys(tabInfos) as tabName}
					<Tab bind:group={tabSet} name="{tabName}" value={tabName}>
						{tabName}
					</Tab>
				{/each}
				<svelte:fragment slot="panel">
					<div class="border-2 rounded-lg border-black">
						<GraphVisualisation width={width} height={height} network={tabInfos[tabSet].network} initialZoom={0.2}
																disableInteraction={true}
																initialTranslate={{x: 2800, y: 1200}} />
					</div>
				</svelte:fragment>
			</TabGroup>
		{/if}

		<p class="mt-24">
			We also experiment with different <span class="text-surface-600 font-bold">Post-Training Recruiter Bias Mitigations</span>:
		</p>
		<p class="mt-4">
			We've assumed that each recruiter simply <i>makes a decision</i> on each applicant, but they're easy to
			change such that they <i>rank</i> each applicant instead.
		</p>
		<p class="mt-16">
			One idea we could try is to hire the same proportion of applicants from both groups,
			while still hiring the highest-ranked applicants first.
		</p>
		<p class="mt-4">
			For example
			we might hire the highest-ranked half of group A and the highest-ranked half of group B.
		</p>
		<p class="mt-8">
			This satisfies <span class="text-surface-600 font-bold">Demographic Parity</span>,
			but we could ask if there ways we could satisfy the other definitions of unbiasedness.
		</p>
		<p class="mt-16">
			It turns out that we can, but it's a little more difficult.
		</p>
		<ol class="list-decimal list-inside ml-10 text-lg text-left space-y-4 min-w-[40rem] mt-16">
			<li>
				As well as the training examples and testing examples, we create another set of applicants,
				we'll call the <span class="text-surface-600 font-bold">Mitigation Applicants</span>
			</li>
			<li>
				After training each recruiter, we look for <span class="text-surface-600 font-bold">Hiring Proportions</span>,
				(the proportion of people to hire from each group), which minimise some measure of bias on the
				set of <span class="text-surface-600 font-bold">Mitigation Applicants</span>.
			</li>
			<li>
				When using that recruiter, we hire the highest-ranked specified proportion of people from each group.
			</li>
		</ol>

		<p class="mt-8">
			Remember we're not allowed to use the competence of our testing applicants.
			If we had access to this, we wouldn't need to make decisions about them in the first place!
		</p>

		<p class="mt-16">
			For this reason, we usually can't completely satisfy these definitions of unbiasedness.
		</p>

		<h3 class="text-3xl font-bold mt-16">
			Next Steps
		</h3>
		<p class="mt-4">
			We've now collected lots of data on how bias changes with
			<span class="text-surface-600 font-bold">Different Recruiters</span>,
			<span class="text-surface-600 font-bold">Different Mitigations</span>
			and
			<span class="text-surface-600 font-bold">Different Applications</span>.
			All that's left is to find patterns and draw conclusions.
		</p>
		<p class="mt-12">
			We're almost done! In the next section we'll be putting the results we presented in the first section
			into context.
		</p>

		<button type="button"
						class="btn btn-xl text-2xl variant-filled py-4 px-4 rounded-full min-w-32 z-[5] mt-12"
						onclick={() => window.location.href = '/walkthrough/the_results'}>
			Next
			<CaretRightFill class="ml-2" width={20} height={20} />
		</button>


	</div>
</div>