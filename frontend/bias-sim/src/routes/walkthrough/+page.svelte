<script>
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import { CaretRightFill } from 'svelte-bootstrap-icons';
</script>
<h3 class="text-6xl font-bold mt-2 p-8">
	Welcome to the Walkthrough!
</h3>
<div class="flex justify-center pt-10 pb-10 text-center">
	<div class="text-lg max-w-[48rem] flex items-center flex-col">
		<div class="max-w-[40rem]">

			<p>
				In this project, I investigate bias in machine learning by performing thousands of
				simulations of a machine learning recruitment scenario.
			</p>
			<p class="mt-12 font-bold">
				We can learn a lot from these simulations.
			</p>
			<p class="mt-12 mb-8">
				Under sensible assumptions, we find the following:
			</p>
		</div>

		<div class="text-left p-4  card rounded-4 drop-shadow-xl text-base">
			<Accordion autocollapse>
				<AccordionItem open>
					<svelte:fragment slot="summary"><span class="font-bold text-2xl">1) Bias is Common</span></svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4">
							Bias is likely to exist in <i>any</i> machine learning process, even when input data is completely
							unbiased,
							and bias isn't introduced in other areas of the process.
						</div>

					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-2xl">2) Established Metrics for Bias Disagree</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4">
							Two of the most commonly used metrics for defining bias in machine learning
							rarely agree. Under certain common
							conditions, they even <i>contradict</i> each other on which group the bias is against.
						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-2xl">3) Bias Exacerbates Existing Differences</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4">

							If group A tends to be worse at the role than group B on average,
							this makes group A <i>more</i> likely to face unfair treatment in hiring.
							In other words, existing performance differences can lead to even stronger bias.
							<p class="mt-8">
								However, by only looking at the selection of people who were hired,
								and the selection of people who weren't, we are likely to conclude that the bias is
								actually in <i>favour</i> of group A.
							</p>
							<p class="mt-8">
								If both groups are just as good at the role on average, bias is <i>lower</i>
								but is still usually significant.
							</p>
						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-2xl">4) We can Reduce Bias by Hiding Information</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4">
							<p>
								We can reduce bias by hiding which group each applicant belongs to.
							</p>
							<p class="mt-8">
								We can reduce it even more by removing any information that hints at group membership,
								although this might slightly reduce accuracy.
							</p>
						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span class="font-bold text-2xl">5) Different ML Models lead to Different Levels of Bias</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4">
							Different machine learning architectures show significant difference in the level of bias in the
							decisions they make.
						</div>
					</svelte:fragment>
				</AccordionItem>
				<AccordionItem>
					<svelte:fragment slot="summary"><span
						class="font-bold text-2xl">6) Post-Training Mitigations can Reduce Bias</span>
					</svelte:fragment>
					<svelte:fragment slot="content">
						<div class="rounded-md bg-surface-200 p-4">
							Simple post-training bias mitigations can reduce levels of bias in machine learning recruiters, at
							a slight cost to accuracy.
						</div>
					</svelte:fragment>
				</AccordionItem>
			</Accordion>
		</div>

		<div class="max-w-[40rem]">

			<p class="mt-8">
				If they are true, these findings have enormous implications for machine learning across domains.
			</p>
			<p class="mt-16">
				But they'll take some time to explain.

			</p>
			<p class="mt-16">
				With that context, these findings may appear more or less impressive. Indeed you'll be able to
				judge whether the assumptions I've made are sensible.
			</p>
			<p class="mt-16">
				This walkthrough goes through each aspect of the simulation to explain how it works,
				and is aimed for the general audience.
			</p>
			<p class="mt-8">
				I'll introduce the recruiting scenario we're modelling,
				discuss how we generate applicants and applications with something called a
				<span class="text-surface-600 font-bold">Bayesian Network</span>,
				discuss how we measure bias, and finally bring everything together
				to talk about the simulation we perform.
			</p>
			<p class="mt-16 font-bold">
				Enjoy!
			</p>
		</div>

		<button type="button"
						class="btn btn-xl text-2xl variant-filled py-4 px-4 rounded-full min-w-32 z-[5] mt-16"
						onclick={() => window.location.href = '/walkthrough/what_are_we_doing_here'}>
			Next
			<CaretRightFill class="ml-2" width={20} height={20} />
		</button>

	</div>
</div>