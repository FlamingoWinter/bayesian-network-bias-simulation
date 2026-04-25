<script lang="ts">
	import DecisionTree from '../../../components/animations/DecisionTree.svelte';
	import { CaretRightFill } from 'svelte-bootstrap-icons';
</script>

<h3 class="mt-2 p-8 text-6xl font-bold">What's a Recruiter, Exactly?</h3>
<div class="flex justify-center pb-10 pt-10 text-center">
	<div class="flex max-w-[40rem] flex-col items-center text-lg">
		<p>
			In the first page of the walkthrough, we said that a
			<span class="font-bold text-surface-600">Recruiter</span>
			was a machine which produces a <span class="font-bold text-surface-600">Decision</span> for
			each
			<span class="font-bold text-surface-600">Application</span>.
		</p>
		<p class="mt-16">
			Because we're using <span class="font-bold text-surface-600">Machine Learning</span>, we train
			each of our recruiters on a list of
			<span class="font-bold text-surface-600">Training Examples</span>. Each training example is an
			application and corresponding decision.
		</p>
		<p class="mt-16">
			In total, in this project, we implement seven different recruiters based on modern machine
			learning algorithms.
		</p>
		<p class="mt-4">
			Most of these require quite a background in computer science to understand. However, it's
			difficult to understand this project fully unless you have some sort of idea on how exactly
			they make decisions.
		</p>
		<p class="mt-4">
			So, I'm, going to explain one of the simpler architectures here, the
			<span class="font-bold text-surface-600">Random Forest</span> recruiter.
		</p>

		<h3 class="mt-16 text-3xl font-bold">Decision Trees</h3>
		<p class="mt-4">
			In order to talk about those we have to talk about a simpler model, the
			<span class="font-bold text-surface-600">Decision Tree</span> recruiter.
		</p>
		<p class="mb-4 mt-4">Below is an example of a decision tree:</p>
		<div class="rounded-md border-2 border-black">
			<DecisionTree useAnimation={false} />
		</div>
		<p class="mt-4">
			We can see it's a set of questions to ask about an application which eventually leads a
			recruiter to make a decision.
		</p>
		<p class="mt-4">
			A <span class="font-bold text-surface-600">Tree</span> is a concept in computer science for the
			structure of this object, because it branches out, just like a tree might.
		</p>
		<p class="mb-4 mt-16">
			Once we have our decision tree, it's fairly easy to see how we might build a recruiter. We
			just use this decision tree on each application we get:
		</p>
		<div class="rounded-md border-2 border-black">
			<DecisionTree useAnimation={true} />
		</div>
		<p class="mt-8">But how do we build that decision tree in the first place?</p>
		<p class="mt-12">
			This happens in the recruiter's training stage. When we give the recruiter the training
			examples, it looks through every possible question it could ask about the data and then
			chooses the question which is most <span class="font-bold text-surface-600">useful</span> to ask
			first.
		</p>
		<p class="mt-12">
			It works out which question is most useful, by calculating which one splits the training
			examples into classes it can label <span class="font-bold text-success-800">Hired</span> and
			<span class="font-bold text-error-600">Not Hired</span>
			such that the fewest examples are in the wrong class as possible.
		</p>
		<p class="mt-12">
			After that it chooses the next best question, until it's fully created a decision tree.
		</p>
		<p class="mt-12">
			So when <span class="font-bold text-surface-600">Training</span> the recruiter, we build a
			decision tree, and when <span class="font-bold text-surface-600">Using</span> the recruiter, we
			use that to make a decision on each of the applications.
		</p>

		<h3 class="mt-16 text-3xl font-bold">The Random Forest Recruiter</h3>
		<p class="mt-8">Unfortunately, this doesn't work too well in practice.</p>
		<p class="mt-12">
			What happens is that these decision trees end up memorising all the training examples, rather
			than actually finding patterns. When we use the recruiter in practice, it makes the same
			decision that was made on the closest training example, even if that decision doesn't match
			the rest of the data.
		</p>
		<p class="mt-12">
			To fix this, we don’t rely on just one decision tree. Instead, we build lots of them, each
			trained on a different slice of the data.
		</p>
		<p class="mt-12">
			Lots of trees make a forest, so we call this the the <span class="font-bold text-surface-600"
				>Random Forest recruiter</span
			>. Let's take a look at how it works now:
		</p>
		<p class="mt-12">
			During <span class="font-bold text-surface-600">Training</span>, we create multiple
			<span class="font-bold text-surface-600">Decision Tree Subrecruiters</span>, each with a
			slightly different version of the training examples.
		</p>
		<p class="mt-6">
			For each subrecruiter, We randomly remove some of the training examples and remove the same
			random parts of every application. Then, we train the subrecruiter on these training examples.
		</p>
		<p class="mt-12">
			When <span class="font-bold text-surface-600">Using</span> the recruiter, we ask each of the decision
			tree sub-recruiters for a decision and select the most common decision.
		</p>

		<h3 class="mt-16 text-3xl font-bold">Next Steps</h3>
		<p class="mt-4">
			So we've seen how to generate candidates, and what a machine-learning recruiter might look
			like in practice.
		</p>
		<p class="mt-4">
			The final question we need to answer is how to measure how biased a recruiter is, based on the
			decisions it makes. We'll see that in the next section.
		</p>
		<p class="mt-4">Finally we'll be able to put everything together and run our simulation.</p>

		<button
			type="button"
			class="variant-filled btn btn-xl z-[5] mt-12 min-w-32 rounded-full px-4 py-4 text-2xl"
			on:click={() => (window.location.href = '/walkthrough/how_do_we_measure_bias')}
		>
			Next
			<CaretRightFill class="ml-2" width={20} height={20} />
		</button>
	</div>
</div>
