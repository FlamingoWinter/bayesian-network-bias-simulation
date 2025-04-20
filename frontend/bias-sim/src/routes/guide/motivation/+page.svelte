<script>
	import Citation from '../../../components/Citation.svelte';
</script>

<h3 class="text-6xl font-bold mt-2 pl-24">
	Motivation
</h3>
<div class="flex justify-center pt-10 pb-28">
	<div class="text-lg max-w-[48rem]">
		<p>
			The decisions made by machine learning systems may have significant
			consequences to the people they affect.
		</p>
		<p class="mt-6">
			Their use is becoming increasingly prevalent. Automated tools are finding use in
			resume-screening
			<Citation number={1}
								link="https://www.resumebuilder.com/7-in-10-companies-will-use-ai-in-the-hiring-process-in-2025-despite-most-saying-its-biased/#:~:text=About%2023%25%20use%20AI%20to,AI%20in%20their%20hiring%20practices." />
			<Citation number={2}
								link="https://www.youtube.com/watch?v=6nGM37ThEsU" />
			, predicting crime and recidivism
			<Citation number={3}
								link="https://www.theguardian.com/uk-news/2025/apr/08/uk-creating-prediction-tool-to-identify-people-most-likely-to-kill" />
			<Citation number={4}
								link="https://hdsr.mitpress.mit.edu/pub/7z10o269/release/7" />
			, loan approval
			<Citation number={5}
								link="https://link.springer.com/article/10.1007/s00146-023-01676-3" />
			, and medical diagnoses
			<Citation number={6}
								link="https://www.theguardian.com/society/2025/feb/04/nhs-to-launch-worlds-biggest-trial-of-ai-breast-cancer-diagnosis" />
			.
			Machine learning controls the products we buy, the entertainment recommended to us, and the information we see on
			search
			engines.
		</p>
		<p class="mt-6">
			There is a concern that these systems exhibit bias, whereby the decisions they make are unfair against
			certain groups of people. Indeed existing research has shown that many modern systems do
			systematically disadvantage certain groups
			<Citation number={7}
								link="https://www.bbc.co.uk/news/technology-54349538" />
			<Citation number={8}
								link="https://www.reuters.com/article/world/insight-amazon-scraps-secret-ai-recruiting-tool-that-showed-bias-against-women-idUSKCN1MK0AG/" />
			<Citation number={9}
								link="https://arxiv.org/abs/2310.05135" />
			.
			However, important questions remain largely unanswered:
		</p>
		<ul class="mt-6 pl-4 list-disc">
			<li>Why are these systems biased?</li>
			<li>Can we expect them to be more biased than the corresponding human systems?</li>
			<li>How can we work towards minimising these biases?</li>
		</ul>


		<p class="mt-6">
			For the remainder of this project, we focus on recruitment, whereby a
			<span class="text-surface-600 font-bold">Recruiter</span> classifies <span class="text-surface-600 font-bold">Applicants</span>,
			into
			the classes <span class="text-success-800 font-bold">Hired</span> or <span class="text-error-600 font-bold">Not Hired</span>,
			based on an <span class="text-surface-600 font-bold">Application</span>.

			We define bias as <span class="text-surface-600 font-bold">Unfairness Towards a Protected Group</span>.
		</p>
		<p class="mt-6">
			In order to answer the questions above, we need a rigorous and scientific approach to bias.
			Ultimately, this is a difficult requirement.
		</p>
		<p class="mt-6">
			For example, one could make the claim that a
			recruiting system is biased against group A,
			because an applicant from group A is less likely to get a job when they apply.
			However, a commentator could argue that such an observation is to be expected,
			because that group comprises less-qualified candidates.
		</p>
		<p class="mt-6">
			Indeed, in many domains, there are differences in competency between groups.

			This doesn't mean that a person is more or less competent only because of their group membership,
			instead it may be due to a combination of different education opportunities, differing access to networking,
			different exposure to role models, and so on.
			Different backgrounds may be associated with different economic status, and a lifetime influenced by
			stereotypes may lead to eventual change.
		</p>
		<p class="mt-6">
			In this case, a person's membership of the protected group and a person's competence in performing a job
			are related features. In a statistical sense, they are dependent variables.
		</p>
		<p class="mt-6">
			If group membership were independent to the inputs and outputs of a decision-making
			algorithm, the decisions made by any model will be unbiased by most measurements, so this isn't an interesting
			case to consider.
		</p>
		<p class="mt-6">
			In many instances, it may be desirable to ensure two random members of different groups have
			the same likelihood of receiving a job, regardless of differences in competence to promote diversity or
			mitigate systemic biases. We limit the scope of this project to
			largely consider competence-based hiring.
		</p>
		<p class="mt-6">
			Since protected group membership and competence are not statistically independent,
			most investigations into the bias exhibited by a decision-making system involve some
			notion of what decisions the system should have made.
			We then compare the deviation between these and the decisions the system did make, and whether that deviation
			is dependent on the group membership of the person it was classifying.
		</p>
		<p class="mt-6">
			Unfortunately, our notion of the "decisions the systems should have made" is influenced by our own biases as well.
			So any attempt to measure the bias within a system will be influenced by our own preconceptions.
		</p>
		<p class="mt-6">
			In this project, we take a different approach.
		</p>
		<p class="mt-6">
			The understanding of bias we can attain from existing systems is limited because the "correct" decisions
			are shaped by human assumptions.
			But, the same limitation doesn't exist in simulated systems.

			Instead, as simulators we are able to define ground truth
			and provide it directly to recruiters during training.

			If recruiters exhibit bias in this instance of unbiased training data, we can presume they will continue to
			exhibit that bias when extrapolating to the real world.
		</p>
		<p class="mt-6">
			By simulating this recruiting scenario thousands of times with randomised applicant generation,
			we can see which patterns in bias are prevalent throughout the results.

			This controlled environment also means we can perform experiments,
			systematically modifying parts of the simulation and seeing the effects of our actions.

			Under the assumptions we've made in the simulation we can then extrapolate these results to real-world systems.
		</p>
		<p class="mt-6">
			While we focus on recruiting, this is for ease of communication and conceptualisation. The simulation
			generalises to all fields of automated decision-making.
		</p>
	</div>
</div>