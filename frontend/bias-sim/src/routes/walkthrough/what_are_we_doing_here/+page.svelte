<script>
	import Citation from '../../../components/Citation.svelte';
	import RecruiterAnimation from '../../../components/animations/RecruiterAnimation.svelte';
	import ApplicationIcon from '../../../components/svgs/ApplicationIcon.svelte';
	import { CaretRightFill } from 'svelte-bootstrap-icons';
</script>

<h3 class="text-6xl font-bold mt-2 p-8">
	What are we Doing Here?
</h3>
<div class="flex justify-center pt-10 pb-10 text-center">
	<div class="text-lg max-w-[40rem]">
		<p>
			<span class="text-surface-600 font-bold">Machine Learning</span> systems make decisions for us every day.
		</p>
		<p class="mt-12">
			Today, such a system might decide the diagnosis you receive for a medical condition
			<Citation number={1}
								link="https://www.theguardian.com/society/2025/feb/04/nhs-to-launch-worlds-biggest-trial-of-ai-breast-cancer-diagnosis" />
			,
			whether you're approved for a loan
			<Citation number={2}
								link="https://link.springer.com/article/10.1007/s00146-023-01276-3" />
			,
			whether you might be likely to commit a crime
			<Citation number={3}
								link="https://www.theguardian.com/uk-news/2025/apr/08/uk-creating-prediction-tool-to-identify-people-most-likely-to-kill" />
			,
			or even whether you're hired to a company
			<Citation number={4}
								link="https://www.youtube.com/watch?v=6nGM37ThEsU" />
			.
		</p>
		<p class="mt-12">
			One major concern is that these systems may be biased. That is, they're
			<span class="text-surface-600 font-bold">Unfair Towards a Particular Group of People</span>.
		</p>

		<p class="mt-12">
			Let's consider that final example, of a machine-learning tool deciding who does or doesn't get hired.
			Such a system looks something like this:
		</p>


		<RecruiterAnimation />

		<p class="mt-6">
			A
			<span class="text-surface-600 font-bold">Recruiter</span> classifies <span class="text-surface-600 font-bold">Applicants</span>,
			into
			the classes <span class="text-success-800 font-bold">Hired</span> or <span class="text-error-600 font-bold">Not Hired</span>,
			based on an <span class="text-surface-600 font-bold">Application</span> it receives from each applicant.
		</p>
		<p class="mt-12 mb-4">
			If we look at that application in a little more detail, we see that it's a list of facts about the applicant in
			question:
		</p>
		<div class="min-h-40 flex items-center justify-center">
			<div class="flex min-w-[30rem] justify-center items-center gap-4">
				<div class="h-24 w-24">
					<ApplicationIcon />
				</div>
				<div class="text-left">
					<p class="text-surface-600 font-bold">Scored 10 in Interview</p>
					<p class="text-orange-600 font-bold">Went to Cambridge University</p>
					<p class="text-cyan-600 font-bold">A* in GCSE Maths</p>
					<p class="text-amber-600 font-bold">Can Play Piano</p>
					<p class="text-tertiary-600 font-bold">Poor Social Skills</p>
				</div>
			</div>
		</div>
		<p class="mt-12">
			This might be gleamed from a resume or a LinkedIn Profile, so it could contain some irrelevant information.
			Usually it's structured in a way which makes it easy for the recruiter to read.
		</p>
		<p class="mt-4 mb-4">
			Here's another example:
		</p>
		<div class="min-h-40 flex items-center justify-center">
			<div class="flex min-w-[30rem] justify-center items-center gap-4">
				<div class="h-24 w-24">
					<ApplicationIcon />
				</div>
				<div class="text-left">
					<p class="text-surface-600 font-bold">Scored 4 in Interview</p>
					<p class="text-orange-600 font-bold">Went to Oxford University</p>
					<p class="text-cyan-600 font-bold">C in GCSE Maths</p>
					<p class="text-amber-600 font-bold">Can't Play Piano</p>
					<p class="text-tertiary-600 font-bold">Average Social Skills</p>
				</div>
			</div>
		</div>

		<p class="mt-12">
			So, a recruiter is a machine which converts an application into a decision.
		</p>

		<p class="mt-24">
			The recruiters we're interested in use <span class="text-surface-600 font-bold">Machine Learning</span>.
			That means instead of telling the recruiter exactly how to make decisions,
			we train it on lots of examples.
		</p>

		<p class="mt-12">
			Each <span class="text-surface-600 font-bold">Training Example</span> consists of an application and a
			corresponding hiring decision.
			We could generate those from previous decisions a company has made,
			or by asking humans to make decisions. We'll discuss what this might look in practice a bit later.
		</p>

		<p class="mt-24">
			So, how can we tell whether such a system is biased?
		</p>
		<p class="mt-12">
			When we talk about bias, we usually do so in terms of protected groups
			(for example, age, gender, race, religion, sexuality, and so on).
			Let's consider one of those protected groups, and track how they're handled by our recruiter.
		</p>
		<p class="mt-12">
			Purple applicants are in the protected group, and gray applicants aren't:
		</p>

		<RecruiterAnimation showBias={true} />

		<p class="mt-12">
			It certainly seems like this recruiter is biased. In fact, purple has only a 30% chance of being hired
			while gray has a 70% chance.
		</p>

		<p class="mt-12">
			But in some cases, we might expect this.
		</p>

		<p class="mt-12">
			If the protected characteristic is <span class="text-amber-600 font-bold">Age</span>, and the job is something
			like firefighting, we would
			expect there to be an actual difference in average competency between the two groups.
		</p>

		<p class="mt-12">
			Also, on average, men are more likely to apply for jobs they're under-qualified for
			<Citation number={5} link="https://hbr.org/2014/08/why-women-dont-apply-for-jobs-unless-theyre-100-qualified" />
			,
			so we might expect there to be some competency differences among applicants,
			if this were the protected characteristic too.
		</p>

		<p class="mt-12">
			Often these links between competency and the protected characteristic aren't causal but correlational.
			Humans are very complicated systems, shaped by entire lifetimes,
			and many of our characteristics are deeply related to all our other characteristics.
		</p>

		<p class="mt-12">
			In fact, that's often why these models are biased in the first place.
			Usually we don't include the protected characteristic in the application,
			but because those characteristics are so deeply related to everything else,
			a recruiter can effectively "guess" what they might be.
		</p>

		<p class="mt-12">
			We'll discuss this all later.
			For now, we still care about whether this recruiter is treating people fairly.
		</p>

		<p class="mt-12">
			Another thing we can try is thinking about what decisions a hypothetical unbiased recruiter might make.
			That recruiter would hire everyone who's actually competent and ignore everyone else.
		</p>
		<p class="mt-4 mb-6">
			Maybe we could measure how biased a recruiter is by comparing the decisions it makes to those
			unbiased decisions?
		</p>

		<RecruiterAnimation showBias={true} showCompetence={true} />

		<p class="mt-8">
			And now we see that a competent purple only has a 50% chance of being hired, whereas a competent gray has an
			80% chance of being hired.
		</p>
		<p class="mt-8">
			So we can be a bit more convinced that it isn't treating the two groups fairly.
		</p>

		<p class="mt-12">
			One problem remains. Who gets to decide which applicants are actually competent?
		</p>
		<p class="mt-4">
			If our understanding of bias depends on being able to produce an unbiased decision, then
			it's going to be very difficult indeed to investigate these models!
		</p>

		<h3 class="text-3xl font-bold mt-16">
			What we've been Building Towards
		</h3>

		<p class="mt-4">
			In this project, we investigate bias within simulated models of recruitment.
		</p>
		<p class="mt-12">

			Of course that means that any of our findings are limited to these simulated scenarios.

			But by repeating the simulation 1000s of times with random scenarios, we can find consistent patterns across
			those randomised experiments.

			And it's likely that those findings will generalise to real-world recruiting.
		</p>

		<p class="mt-12">
			This means we can sidestep the problem we've just discussed.
			We can decide which candidates should actually be fired or hired, since they're all hypothetical anyway.
		</p>
		<p class="mt-12">
			In fact, we go one step further.
			We give that information directly to our recruiters during training.
			That is, <span class="text-surface-600 font-bold">the Training Examples are Completely Unbiased</span>.
		</p>
		<p class="mt-12">
			If we find that bias still exists in the simulation, we can be fairly sure it will exist
			in the real-world where the data provided to recruiters already contains bias.
		</p>

		<h3 class="text-3xl font-bold mt-16">
			Next Steps
		</h3>
		<p class="mt-4">
			We've made a good start. But we still have some critical questions to answer:
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
			We'll discuss all these in later parts of the walkthrough.
			For now, let's jump into <span class="text-surface-600 font-bold">Bayesian Networks</span>!
		</p>

		<button type="button"
						class="btn btn-xl text-2xl variant-filled py-4 px-4 rounded-full min-w-32 z-[5] mt-12"
						onclick={() => window.location.href = '/walkthrough/how_do_we_simulate_candidates'}>
			Next
			<CaretRightFill class="ml-2" width={20} height={20} />
		</button>

	</div>
</div>