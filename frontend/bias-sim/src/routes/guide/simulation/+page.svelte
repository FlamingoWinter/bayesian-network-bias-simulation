<h3 class="text-6xl font-bold mt-2 pl-24">
	The Simulation
</h3>
<div class="flex justify-center pt-10 pb-28">
	<div class="text-lg max-w-[48rem]">
		<p>
			A
			<span class="text-surface-600 font-bold">Recruiter</span> classifies <span class="text-surface-600 font-bold">Applicants</span>,
			into
			the classes <span class="text-success-800 font-bold">Hired</span> or <span class="text-error-600 font-bold">Not Hired</span>,
			based on an <span class="text-surface-600 font-bold">Application</span>.
		</p>
		<p class="mt-4">
			An Applicant is a set of instanced random variables, drawn from a joint distribution given by a Bayesian network.
			One of those variables, the <span class="text-surface-600 font-bold">Protected Characteristic</span>,
			corresponds to protected group membership. That is, whether or not the applicant is a member of the protected
			group.
			Another of those variables, <span class="text-surface-600 font-bold">Competence</span> corresponds to the
			ground truth.
			That is, whether the applicant should be hired.
		</p>
		<p class="mt-4">
			Each run of the simulation works as follows:
		</p>
		<ol class="list-decimal list-inside ml-10 text-lg space-y-4 mt-4">
			<li>Generate a random Bayesian Network
				(See <a href="/guide/generating_a_random_network" class="font-bold text-secondary-600 underline">Generating a
					Random Network</a>).
			</li>
			<li>Generate a set of applicants as samples from that Bayesian network
				(See <a href="/guide/sampling_from_a_network" class="font-bold text-secondary-600 underline">Sampling from a
					Network</a>).
			</li>
			<li>Split the applicants into a set for training and a set for validation.</li>
			<li>Train each recruiter using the training set. The applicants' application is the features and the applicants'
				competence
				is the target variable. (See <a href="/guide/training_recruiters"
																				class="font-bold text-secondary-600 underline">Training Recruiters</a>)
			</li>
			<li>
				Use the trained recruiter to assign each applicant in the validation set a label, <span
				class="text-success-800 font-bold">Hired</span>
				or <span class="text-error-600 font-bold">Not Hired</span>.
			</li>
			<li>
				Measure the bias in those decisions (See <a href="/guide/measuring_bias"
																										class="font-bold text-secondary-600 underline">Measuring Bias</a>).
			</li>
		</ol>
		<p class="mt-4">
			Each step of this process can be visualised in the <a href="/guide/measuring_bias"
																														class="font-bold text-tertiary-700 underline">Visualisation</a>
		</p>

	</div>
</div>