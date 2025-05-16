<script>
	import Citation from '../../../components/Citation.svelte';
</script>

<h3 class="text-6xl font-bold mt-2 pl-24">
	Motivation
</h3>

<div class="flex justify-center pt-10 pb-10">
	<div class="text-lg max-w-[40rem] flex flex-col items-center">

		<p class="mt-2">
			Machine learning (ML) is becoming increasingly prevalent in decision‑making, finding use in
			resume screening,
			<Citation number={1}
								link="https://www.resumebuilder.com/7-in-10-companies-will-use-ai-in-the-hiring-process-in-2025-despite-most-saying-its-biased/" />
			<Citation number={2} link="https://www.youtube.com/watch?v=6nGM37ThEsU" />
			predicting crime and recidivism,
			<Citation number={3} link="https://doi.org/10.1162/99608f92.6ed64b30" />
			<Citation number={4}
								link="https://www.theguardian.com/uk-news/2025/apr/08/uk-creating-prediction-tool-to-identify-people-most-likely-to-kill" />
			loan approval,
			<Citation number={5} link="https://doi.org/10.1007/s00146-023-01676-3" />
			and medical diagnoses.
			<Citation number={6}
								link="https://www.theguardian.com/society/2025/feb/04/nhs-to-launch-worlds-biggest-trial-of-ai-breast-cancer-diagnosis" />
			It influences the products we buy,
			<Citation number={7} link="https://doi.org/10.2139/ssrn.4245401" />
			the entertainment recommended to us,
			<Citation number={8} link="https://doi.org/10.1016/j.gltp.2022.03.012" />
			and the information we see on search engines.
			<Citation number={9} link="https://doi.org/10.1007/978-0-387-30164-8_744" />
			Existing research has shown that many modern ML systems exhibit bias,
			<Citation number={10} link="https://doi.org/10.1145/3457607" />
			<Citation number={11} link="https://doi.org/10.1007/s42001-025-00386-8" />
			such that the decisions they make are unfair towards certain groups.
		</p>

		<p class="mt-8">
			For ease of communication and conceptualisation, I narrow our focus to recruitment, whereby an ML recruiter
			classifies applicants into the classes “<i>hire</i>” or “<i>reject</i>”, based on their applications.
			If I were to investigate this scenario using real data, I would be likely to suffer three difficulties:
		</p>

		<ol class="list-decimal list-inside mt-6 text-left space-y-2">
			<li>It is difficult to gather sufficient data to assess bias across many decision‑making scenarios.</li>
			<li>Some metrics for bias require some notion of ground truth
				<Citation number={12} link="https://fairmlbook.org/pdf/fairmlbook.pdf" />
				(how competent or meritorious an applicant actually is), but this is influenced by who measures it.
			</li>
			<li>The training set is likely to be biased, so it is difficult to isolate the bias which emerges from the
				recruiter’s decision‑making.
			</li>
		</ol>

		<p class="mt-8">
			By using simulated data, I avoid these problems. I can quickly synthesise a sufficiently‑sized dataset, and ground
			truth can be explicitly generated. However, this approach presents an additional requirement. The simulated data
			needs to be drawn from a distribution which approximates that of reality. A Bayesian network is a model for a
			joint probability distribution which encodes causality between variables.
			<Citation number={13} link="https://www.cambridge.org/core/books/causality/B0046844FAE10CBF274D4ACBDAEB5F5B" />
			I justify why this is a suitable distribution for applicants in <a href="#applicant-dist">Section&nbsp;4</a>.
		</p>

		<p class="mt-8">
			A standard causal explanation for machine unfairness is that bias in a training set is propagated to bias in a
			model’s output.
			<Citation number={14} link="https://developers.google.com/machine-learning/crash-course/fairness/types-of-bias" />
			<Citation number={15} link="https://www.weforum.org/stories/2021/07/ai-machine-learning-bias-discrimination/" />
			This would imply that bias can be fully mitigated by debiasing the training dataset,
			<Citation number={16}
								link="https://news.mit.edu/2024/researchers-reduce-bias-ai-models-while-preserving-improving-accuracy-1211" />
			<Citation number={17} link="https://www.sap.com/swiss/blogs/how-ai-can-end-bias" />
			,
			and that a model is only as biased as its input data. In this dissertation, I show that this is an incomplete
			interpretation.
			Bias can exist when training datasets are fully representative of the underlying true distribution (Result&nbsp;1).
		</p>

		<p class="mt-8">
			Additionally, I demonstrate that two standard fairness criteria exhibit high disagreement in practice (Result&nbsp;2),
			a problem compounded by the fact that many existing systems use an unsuitable fairness metric.
			<Citation number={18} link="https://arxiv.org/abs/2108.02497" />
			<Citation number={19}
								link="https://www.researchgate.net/publication/385721402_A_Review_of_Fairness_and_A_Practical_Guide_to_Selecting_Context-Appropriate_Fairness_Metrics_in_Machine_Learning" />
			Given then that this dissertation offers a robust criticism of current working practices, its contributions have
			the potential to meaningfully inform and improve the field.
		</p>

		<p class="mt-8">
			I investigate these findings and related phenomena by measuring bias across many simulations in which a recruiter
			makes hiring decisions on sampled applicants, systematically varying recruiter models, application generation
			conditions, and post‑training bias mitigations. As with any simulation, the value of these results depends on
			whether they extrapolate to real‑world recruiting. I evaluate this by analysing each assumption made in the
			simulation’s design.
		</p>

		<p class="mt-8">
			While I focus on recruiting, this largely doesn’t affect the implementation of the simulation. To an extent, the
			results generalise across the field of ML classification.
		</p>

		<p class="mt-8">
			Finally, I think the findings presented in this dissertation are valuable to a wider audience, including one of
			policy‑makers, recruiters and casual readers. However, they require some context to fully understand. Therefore, I
			also developed a website to host a visualisation and walkthrough of the research at
			<a href="https://www.modelling-bias.com" class="underline">modelling-bias.com</a>. Markers are strongly encouraged
			to visit this website.
		</p>

	</div>
</div>
