<script lang="ts">

	import GraphVisualisation from '../../../components/GraphVisualisation.svelte';
	import { onMount } from 'svelte';
	import type { Network } from '../../../types/network.js';
	import ConditionLogic from '../../../components/ConditionLogic.svelte';
	import { CaretRightFill } from 'svelte-bootstrap-icons';


	let sprinklerNetwork: Network;
	let sharkNetwork: Network;
	let randomSeededNetwork: Network;
	let namedSeededNetwork: Network;

	onMount(async () => {
		sprinklerNetwork = await (await fetch('/sprinkler_network.json')).json() as unknown as Network;
		sharkNetwork = await (await fetch('/shark_sighting.json')).json() as unknown as Network;
		randomSeededNetwork = await (await fetch('/seeded_network.json')).json() as unknown as Network;
		namedSeededNetwork = await (await fetch('/named_seeded.json')).json() as unknown as Network;
	});
</script>

<ConditionLogic />

<h3 class="text-6xl font-bold mt-2 p-8">
	How do we Simulate Candidates?
</h3>
<div class="flex justify-center pt-10 pb-10 text-center">
	<div class="text-lg max-w-[40rem] flex flex-col items-center">
		<p class="mb-8">
			This is a <span class="text-surface-600 font-bold">Bayesian Network</span>:
		</p>
		{#if sprinklerNetwork}
			<div class="border-black border-2 rounded-md">
				<GraphVisualisation
					width={1000} height={450} network={sprinklerNetwork} initialZoom={0.8} noPan={true}
					scoreAndApplication={false} predefinedModel="sprinkler" />
			</div>
		{/if}
		<p class="mt-8">
			Each node represents a <span class="text-surface-600 font-bold">Random Variable</span>.
		</p>
		<p class="mt-4">
			For example, there's a 50% chance of it being cloudy and a 50% chance of it being not cloudy.
		</p>
		<p class="mt-4">
			An arrow from the node <span class="text-surface-600 font-bold">Cloudy</span> to the node <span
			class="text-surface-600 font-bold">Rain</span> means that
			whether it's raining <span class="text-surface-600 font-bold">depends</span> on whether it's cloudy.
		</p>
		<p class="mt-12">
			This example comes from a scenario where the Sprinkler is solar-powered.
			So the chance of the Sprinkler being on depends
			on whether there are Clouds in the sky.
		</p>
		<p class="mt-4">
			Whether it's Raining or not also depends on whether there are clouds in the sky, and whether
			the Grass is wet depends on both the Rain and the Sprinkler.
		</p>
		<p class="mt-20">
			What's interesting here is that all the variables are related to each other.
			Learning the value of any variable gives us information about all the other variables
			, and therefore changes our expectation
			of all the other variables.
		</p>
		<p class="mt-20">
			You can test this out for yourself!
		</p>
		<p class="mt-4">
			Click a node to expand it and "condition" the network on a certain value.
		</p>
		<p class="mt-4">
			For example, if we "condition" the <span class="text-surface-600 font-bold">Cloudy</span>
			variable to be <span class="text-success-800 font-bold">Yes</span>, we can see that it's more likely to be rainy.
		</p>
		<p class="mt-20">
			If we wanted to <span class="text-surface-600 font-bold">Sample</span> this network
			(get a random value for each variable),
			it wouldn't be enough to use the initial probabilities to sample each variable at once.
		</p>
		<p class="mt-8">
			To see why this is, consider that this would result in a reasonable chance of
			both the Sprinkler being
			off and there being
			no Rain.
			But you can test for yourself that it's very unlikely for this combination to actually appear.
		</p>
		<p class="mt-4">
			Instead, we can get a random value for the <span class="text-surface-600 font-bold">Cloudy</span>
			variable.
			Then we use that to get a random value for the <span class="text-surface-600 font-bold">Rain</span>
			and <span class="text-surface-600 font-bold">Sprinkler</span> variable.
			Finally, we use those to get a random value for the
			<span class="text-surface-600 font-bold">Wet Grass</span> variable.
		</p>
		<p class="mt-20">
			Bayesian networks are a great way to represent interacting systems of random variables.
			Let's look at one more example of how this might work.
		</p>
		<h3 class="text-3xl font-bold mt-16">
			Correlation and Causation
		</h3>
		<p class="mt-6">
			We're often told that "correlation does not imply causation" and
			Bayesian Networks are a great tool for explaining this.
			Take a look at the following comic.
		</p>
		<img src="https://www.causeweb.org/cause/sites/default/files/resources/fun/cartoons/shark_ice_cream.jpg" alt=""
				 class="mt-12" width="400" />
		<p class="text-xs mt-2">
			Credit: <a href="https://www.causeweb.org/cause/resources/fun/cartoons/ice-cream-sales-and-shark-sightings">
			CauseWEB </a>
		</p>
		<p class="mt-12">
			If there are more ice cream sales in the UK, there also tend to be more shark sightings,
			and if there are fewer ice cream sales in the UK, there tend to be fewer.
			Therefore, we say that ice cream sales and shark sightings are correlated.
		</p>
		<p class="mt-8">
			We might naively think that this is because sharks like ice cream,
			or because seeing a shark makes a person want to buy an ice cream.
		</p>
		<p class="mt-6 mb-6">
			Of course, we know that instead, there's a common cause. This is what the situation actually looks like:

		</p>
		{#if sharkNetwork}
			<div class="border-black border-2 rounded-md">
				<GraphVisualisation
					width={1000} height={450} network={sharkNetwork} initialZoom={0.8} noPan={true}
					scoreAndApplication={false} predefinedModel="shark_sighting" />
			</div>
		{/if}
		<h3 class="text-3xl font-bold mt-16">
			Simulating Candidates
		</h3>
		<p class="mt-8">
			Let's go back to the problem we're trying to solve.
			We know that whether a person is in a protected group has some correlation
			to all their other characteristics, including competence.
		</p>
		<p class="mt-8">
			But that correlation is not directly causal and would be unfair to rely upon.
		</p>
		<p class="mt-16 font-bold text-xl">
			It happens that Bayesian networks are exactly what we're looking for here!
		</p>
		<p class="mt-12">
			The majority of protected characteristics aren't something the person themselves can control,
			so we assume that these aren't causally dependent on anything.
		</p>
		<p class="mt-8">
			Job competency will depend directly on many variables (perhaps problem-solving skills,
			team-working skills, domain knowledge and so on).
		</p>
		<p class="mt-4">
			Each of these variables will depend on other variables, and each of those variables will depend on other
			variables.
		</p>
		<p class="mt-4">
			Eventually, some of these variables might be dependent on the protected characteristic,
			which results in the correlation we might see.
		</p>
		<p class="mt-8 mb-6">
			Overall, our situation looks something like this:
		</p>

		{#if randomSeededNetwork}
			<div class="border-black border-2 rounded-md">
				<GraphVisualisation
					width={1000} height={450} network={randomSeededNetwork} initialZoom={0.8} noPan={true}
					scoreAndApplication={false} predefinedModel="random_seeded" />
			</div>
		{/if}

		<p class="mt-8 mb-8">
			We could provide some example names (and we provide a way to do this in the
			<a href="/visualisation" class="font-bold text-tertiary-700 underline">Visualisation</a>),
			but they don't make a difference to the simulation we run:
		</p>

		{#if namedSeededNetwork}
			<div class="border-black border-2 rounded-md">
				<GraphVisualisation
					width={1000} height={450} network={namedSeededNetwork} initialZoom={0.8} noPan={true}
					scoreAndApplication={false} predefinedModel="named_seeded" />
			</div>
		{/if}

		<p class="mt-12">
			So this is how we generate our candidates.
			At the start of each simulation, we build a random <span
			class="text-surface-600 font-bold">Bayesian Network</span>, like above, and each
			<span class="text-surface-600 font-bold">Applicant</span>
			is a sample from that network.
		</p>

		<p class="mt-12">
			We assume that all applicants tell the truth so each <span class="text-surface-600 font-bold">Application</span>
			is a selection of some of the information about an applicant.
		</p>

		<h3 class="text-3xl font-bold mt-16">
			Next Steps
		</h3>
		<p class="mt-4">
			Let's look back at the questions we asked ourselves at the start of the project:
		</p>

		<ol class="list-decimal list-inside ml-10 text-lg space-y-4 mt-4 text-left">
			<li>
				How do we generate applicants and applications in a way that mirrors the real world?
			</li>
			<li>
				How do we build and run these Machine Learning recruiters?
			</li>
			<li>
				How do we go about measuring bias?
			</li>
		</ol>

		<p class="mt-12">
			Hopefully, we've motivated the answer to the first question.
		</p>
		<p class="mt-4">
			The second question requires quite a bit of knowledge on machine learning,
			so I'll only give an example in the next section.
		</p>
		<p class="mt-4">
			We'll talk about the recruiter which is most successful in this specific domain,
			the <span class="text-surface-600 font-bold">Random Forest</span> recruiter.
			See you there!
		</p>

		<button type="button"
						class="btn btn-xl text-2xl variant-filled py-4 px-4 rounded-full min-w-32 z-[5] mt-12"
						onclick={() => window.location.href = '/walkthrough/whats_a_recruiter_exactly'}>
			Next
			<CaretRightFill class="ml-2" width={20} height={20} />
		</button>


	</div>
</div>