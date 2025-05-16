<script lang="ts">
	import RecruiterAnimation from '../../../components/animations/RecruiterAnimation.svelte';
	import { CaretRightFill } from 'svelte-bootstrap-icons';
	import Citation from '../../../components/Citation.svelte';
</script>

<h3 class="text-6xl font-bold mt-2 p-8">
	How do we Measure Bias?
</h3>
<div class="flex justify-center pt-10 pb-10 text-center">
	<div class="text-lg max-w-[40rem] flex flex-col items-center">
		<p class="mt-2">
			What does it mean for a recruiter to be fair?
		</p>


		<p class="mt-16">
			Suppose every applicant is from one of two groups, <i>Group A</i> and <i>Group B</i>.
		</p>
		<p class="mt-16">
			Below, I give three definitions of an "unbiased" recruiter.
			Think about which one makes the most sense:
		</p>


		<ol class="list-decimal list-inside ml-10 text-lg space-y-8 mt-12 text-left min-w-[48rem]">
			<li class="bg-surface-200 p-4 rounded-lg drop-shadow-lg">
				An applicant from group A is just as likely to get a job as an applicant from group B.
			</li>
			<li class="bg-surface-200 p-4 rounded-lg drop-shadow-lg">
				A <i>competent</i> applicant from group A is just as likely to be hired as a <i>competent</i> applicant from
				group B.
				<p class="mt-2">
					And an applicant who <i>isn't competent</i> from group A is just as likely to be hired as an
					applicant who <i>isn't competent</i> from group B.
				</p>
			</li>
			<li class="bg-surface-200 p-4 rounded-lg drop-shadow-lg">
				Of the applicant's <i>hired</i> by the recruiter, an applicant from group A is just as likely to
				be competent as an applicant from group B.
				<p class="mt-2">
					And of the applicant's <i>rejected</i> by the recruiter, an applicant from group A
					is just as likely to be competent as an applicant from group B.
				</p>
			</li>
		</ol>

		<p class="mt-8">
			Of people I've asked, most have said that the 2nd definition is most fitting.
			But, each of these are reasonable definitions of bias under some circumstances, and each of
			these have been used before in machine learning.
		</p>

		<p class="mt-16">
			The first definition is for a recruiter which satisfies
			<span class="text-surface-600 font-bold">Demographic Parity</span>.
		</p>
		<p class="mt-4">
			Where group A and group B are such that they don't carry inherent differences in merit,
			we know that in a fair society those groups would have enjoyed the same privileges
			and advantages.
		</p>
		<p class="mt-4">
			Therefore, any fair recruiter will treat those groups equally.
			If there are differences in merit between the two groups,
			then those differences are the result of systemic unfairness. Treating
			those groups equally corrects for those deeper unfair advantages.
		</p>

		<p class="mt-16">
			The second definition is for a recruiter which satisfies
			<span class="text-surface-600 font-bold">Equalised Odds</span>.
		</p>
		<p class="mt-4">
			Being treated fairly means being judged on merit only, and not based
			on irrelevant criteria like a protected characteristic.
			Therefore, if you're being judged by a fair recruiter you should have the same chance of
			being hired as everyone else at your level of competency.
		</p>

		<p class="mt-16">
			The third definition is for a recruiter which satisfies
			<span class="text-surface-600 font-bold">Predictive Parity</span>.
		</p>
		<p class="mt-4">
			A fair recruiter is one which results in fair outcomes.
			If it appears that hired members of group A are in general less competent,
			then the intuitive conclusion is that the process is more lenient towards group A.
		</p>
		<p class="mt-4">
			An outside observer might interpret this as favoritism and this could instead lead to long-term
			negative consequences for group A.
		</p>
		<p class="mt-16">
			So it seems that all these definitions have some validity as preconditions for unbiasedness.
			Unfortunately, it's
			mathematically impossible for even two of these conditions to be true at the same time.
			<Citation number={1} link="https://fairmlbook.org/classification.html#relationships-between-criteria" />
		</p>
		<p class="mt-16">
			In the context of recruiting, we can think of failing to satisfy
			<span class="text-surface-600 font-bold">Predictive Parity</span>
			as <i>bias from the outside</i>.
			A recruiter which fails to satisfy this produces decisions which <i>appear</i> to be biased.
			Those decisions perpetuate inequality.
		</p>
		<p class="mt-16">
			We can think of failing to satisfy <span class="text-surface-600 font-bold">Equalised Odds</span>
			as <i>bias from the inside</i>.
			An applicant classified by this recruiter is treated differently to how they would have been if
			they were in a different group.
		</p>


		<h3 class="text-3xl font-bold mt-16">
			Measuring Bias
		</h3>

		<p class="mt-8">
			We derive a way to measure bias based on each of these definitions.
		</p>

		<p class="mt-16">
			Let's take another look at our recruiting scenario.
		</p>

		<RecruiterAnimation showBias={true} showCompetence={true} />

		<p class="mt-12">
			In machine learning, we call decisions in the top-left quadrant
			<span class="text-success-800 font-bold">True Positives</span>,
			because the model decided "positive" (it decided to hire the person), and this decision was true
			(that person was indeed competent).
		</p>
		<p class="mt-4">
			We call decisions in the bottom-right quadrant
			<span class="text-error-700 font-bold">True Negatives</span> for the same reason.
		</p>

		<p class="mt-12">
			<span class="text-emerald-700 font-bold">False Negatives</span> are decisions in the bottom-left
			quadrant.
		</p>
		<p>
			<span class="text-cyan-800 font-bold">False Positives</span> are decisions in the top-left
			quadrant.
		</p>


		<h3 class="text-3xl font-bold mt-16">
			False Negative Rate and False Positive Rate
		</h3>
		<p class="mt-8">
			The <span class="text-emerald-700 font-bold">False Negative Rate</span> is the chance that a competent candidate
			isn't hired. </p>
		<p class="mt-2">
			You can check for yourself that we can calculate this as:
		</p>

		<div class="mt-16">
			<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				<mfrac>
					<mrow>
						<mi><span class="text-emerald-700 font-bold font-roboto">False&nbsp;Negatives</span></mi>
					</mrow>
					<mrow>
						<mi><span class="text-emerald-700 font-bold font-roboto">False&nbsp;Negatives</span>&nbsp;+&nbsp;<span
							class="text-success-800 font-bold font-roboto">True&nbsp;Positives</span>
						</mi>
					</mrow>
				</mfrac>
			</math>
		</div>

		<p class="mt-16">
			The <span class="text-cyan-800 font-bold">False Positive Rate</span> is the chance that a non-competent
			candidate
			is hired.
		</p>
		<p class="mt-2">
			We can calculate this as:
		</p>

		<div class="mt-16">
			<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				<mfrac>
					<mrow>
						<mi><span class="text-cyan-800 font-bold font-roboto">False&nbsp;Positives</span></mi>
					</mrow>
					<mrow>
						<mi><span class="text-cyan-800 font-bold font-roboto">False&nbsp;Positives</span>&nbsp;+&nbsp;<span
							class="text-error-700 font-bold font-roboto">True&nbsp;Negatives</span>
						</mi>
					</mrow>
				</mfrac>
			</math>
		</div>


		<p class="mt-16">
			We can calculate these metrics for each individual group.
		</p>
		<p class="mt-16">
			If the <span class="text-cyan-800 font-bold">FPR</span> and
			<span class="text-emerald-700 font-bold">FNR</span> are the same for each group, we
			can be sure that the recruiter satisfies
			<span class="text-surface-600 font-bold">Equalised Odds</span>.
		</p>

		<p class="mt-16">
			However, we also care about exactly how biased a recruiter is.
		</p>
		<p class="mt-16">
			For this, we can use <span class="text-emerald-700 font-bold">FNR Difference</span>
			which is the difference in <span class="text-emerald-700 font-bold">FNR</span>
			between the two groups.
		</p>
		<p class="mt-4">
			This corresponds approximately to <i>the chance of a qualified applicant being rejected,
			where they would have been hired if they belonged to the other group</i>.
		</p>

		<p class="mt-16">
			Similarly, <span class="text-cyan-800 font-bold">FPR Difference</span> is the difference
			in <span class="text-cyan-800 font-bold">FPR</span> between the two groups.
		</p>
		<p class="mt-4">
			This corresponds approximately to <i>the chance of an unqualified applicant being hired,
			where they would have been rejected if they belonged to the other group</i>.
		</p>

		<h3 class="text-3xl font-bold mt-16">
			False Discovery Rate and False Omission Rate
		</h3>

		<p class="mt-8">
			The <span class="text-yellow-700 font-bold">False Discovery Rate</span> is the proportion of
			hired candidates
			which aren't competent.
		</p>
		<p class="mt-2">
			We can calculate this as:
		</p>

		<div class="mt-16">
			<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				<mfrac>
					<mrow>
						<mi><span class="text-cyan-800 font-bold font-roboto">False&nbsp;Positives</span></mi>
					</mrow>
					<mrow>
						<mi>
							<span class="text-cyan-800 font-bold font-roboto">False&nbsp;Positives</span>
							&nbsp;+&nbsp;
							<span class="text-success-800 font-bold font-roboto">True&nbsp;Positives</span>
						</mi>
					</mrow>
				</mfrac>
			</math>
		</div>

		<p class="mt-16">
			The <span class="text-purple-700 font-bold">False Omission Rate</span> is the chance that a rejected
			candidate was actually competent.
		</p>
		<p class="mt-2">
			We can calculate this as:
		</p>

		<div class="mt-16">
			<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				<mfrac>
					<mrow>
						<mi><span class="text-emerald-700 font-bold font-roboto">False&nbsp;Negatives</span></mi>
					</mrow>
					<mrow>
						<mi>
							<span class="text-emerald-700 font-bold font-roboto">False&nbsp;Negatives</span>
							&nbsp;+&nbsp;
							<span class="text-error-700 font-bold font-roboto">True&nbsp;Negatives</span>
						</mi>
					</mrow>
				</mfrac>
			</math>
		</div>

		<p class="mt-16">
			If the <span class="text-yellow-700 font-bold">FDR</span> and
			<span class="text-purple-700 font-bold">FOR</span> are the same for each group, we
			can be sure that the recruiter satisfies
			<span class="text-surface-600 font-bold">Predictive Parity</span>.
		</p>

		<p class="mt-16">
			As above, we can ask how we would quantify how biased a recruiter is.
		</p>
		<p class="mt-4">
			For this, we can use
			<span class="text-yellow-700 font-bold">FDR Difference</span>,
			which is the difference in <span class="text-yellow-700 font-bold">FDR</span>
			between the two groups, and
			<span class="text-purple-700 font-bold">FOR Difference</span>,
			which is the difference in <span class="text-purple-700 font-bold">FOR</span>
			between the two groups.

		</p>
		<p class="mt-16">
			These are a little less intuitive than
			<span class="text-emerald-700 font-bold">
			FNR Difference
				</span>
			and
			<span class="text-cyan-800 font-bold">
			FPR Difference
				</span>,
			but they do have the main features we'd want in a metric.
			They increase with bias, and if they are zero, there isn't any bias by that metric.
		</p>

		<h3 class="text-3xl font-bold mt-24">
			Outcome-Based Fairness
		</h3>

		<p class="mt-4">
			We've made the assumption that we should try to define bias based
			only on the outcome of a decision.
		</p>

		<p class="mt-12">
			If we were to apply this approach to investigating bias in a real scenario,
			it would be an oversimplification:
		</p>

		<p class="mt-4">
			We could discuss bias in a system in terms of the intention of the person who created the system,
			in terms of the actual consequences the system has, or in terms of the broader context
			in which the system is used.
		</p>
		<p class="mt-12">
			However, defining it only based on outcomes means it's easier to measure, and isn't influenced on our own biases.
			In a simulated context, it still allows us to make meaningful conclusion about what bias looks like in the real
			world.
		</p>


		<h3 class="text-3xl font-bold mt-24">
			Next Steps
		</h3>
		<p class="mt-4">
			We've identified three definitions of bias and associated metrics.
		</p>
		<p class="mt-4">
			Those are:
		</p>
		<p>
			<span class="text-surface-600 font-bold">Hiring Rate Difference</span> for Demographic Parity,
		</p>
		<p>
			<span class="text-emerald-700 font-bold">FNR Difference</span> and
			<span class="text-cyan-800 font-bold">FPR Difference</span> for Equalised Odds,
		</p>
		<p>
			and <span class="text-purple-700 font-bold">FOR Difference</span> and
			<span class="text-yellow-700 font-bold">FDR Difference</span> for Predictive Parity.
		</p>


		<p class="mt-16">
			We now have enough scaffolding to completely explain the simulation performed in this project.
		</p>
		<p class="mt-12">
			We'll do that in the next section!
		</p>

		<button type="button"
						class="btn btn-xl text-2xl variant-filled py-4 px-4 rounded-full min-w-32 z-[5] mt-20"
						onclick={() => window.location.href = '/walkthrough/putting_it_all_together'}>
			Next
			<CaretRightFill class="ml-2" width={20} height={20} />
		</button>


	</div>
</div>