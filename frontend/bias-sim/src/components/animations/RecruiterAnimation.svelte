<script lang="ts">
	import { animate } from '../../animation/animate';
	import RecruiterBox from '../svgs/RecruiterBox.svelte';
	import PersonIcon from '../svgs/PersonIcon.svelte';
	import ApplicationIcon from '../svgs/ApplicationIcon.svelte';
	import { onMount } from 'svelte';
	import { gsap } from 'gsap';
	import { CaretDownFill, CaretLeftFill, CaretRightFill, CaretUpFill } from 'svelte-bootstrap-icons';

	export let showBias: boolean = false;
	export let showCompetence: boolean = false;

	type OnEnterViewportOptions = {
		callback: () => void
	}

	function onEnterViewport(node: Element, options: OnEnterViewportOptions) {
		let entered = false;
		const observer = new IntersectionObserver(([entry]) => {
			if (entry.isIntersecting && !entered) {
				options.callback();
				entered = true;
			}
		});

		observer.observe(node);

		return {
			destroy() {
				observer.disconnect();
			}
		};
	}

	type ApplicantInformation = {
		id: number
		hired: boolean
		competent: boolean
		indexInHireClass: number
		color: string
	}

	type ApplicationInformation = {
		id: number
		hired: boolean
	}

	let applicants: ApplicantInformation[] = [];
	let applications: ApplicationInformation[] = [];
	let applicantTimeline: gsap.core.Timeline | undefined;

	onMount(() => {
		applicantTimeline = gsap.timeline({ paused: false });

	});

	function startAnimation() {
		function addApplicant() {
			let color;
			let applicantIsHired;
			let competent = true;
			if (showBias) {
				color = (Math.random() > 0.5 ? 'gray' : 'purple');
				if (color == 'purple') {
					competent = Math.random() < 0.6;
					applicantIsHired = Math.random() < (competent ? 0.5 : 0);
				} else {
					competent = Math.random() < 0.7;
					applicantIsHired = Math.random() < (competent ? 0.8 : 0.47);
				}
			} else {
				color = 'black';
				applicantIsHired = Math.random() < 0.5;
			}
			applicants.push({
				id: applicants.length + 1,
				hired: applicantIsHired,
				indexInHireClass: !showCompetence
					? applicants.filter(a => a.hired === applicantIsHired).length
					: applicants.filter(a => a.hired === applicantIsHired && a.competent == competent).length,
				competent: competent,
				color: color
			});
			applicants = applicants;
		}

		addApplicant();
		applicantTimeline?.to({}, {
			duration: 4, repeat: showCompetence ? 40 : 25,
			onRepeat: addApplicant
		});
	}

	function addApplication(applicationIsHired: boolean) {
		applications.push({
			id: applications.length == 0 ? 0 : applications[applications.length - 1].id + 1,
			hired: applicationIsHired
		});
		applications = applications;

	}

</script>

<div class="min-h-40 flex items-center justify-center" use:onEnterViewport={{ callback: startAnimation }}>
	<div
		class="min-w-[60rem] h-[20rem]
			relative
		 flex justify-center items-center font-bold text-2xl "
	>
		<div class="absolute right-0 {showCompetence ? 'text-xs' : ''}">
			<div class="absolute right-0 bg-black rounded-xl w-64 h-1">
				<span class="absolute {showCompetence ? '-top-5' : '-top-8'} right-2 flex items-center gap-2"><CaretUpFill /> Hired</span>
				<span class="absolute top-1 right-2 flex items-center gap-2">Not Hired <CaretDownFill /></span>
			</div>
			{#if showCompetence}
				<div class="absolute right-[7.5rem] bg-black rounded-xl w-1 h-64  -translate-y-1/2">
					<span class="absolute -top-6 -right-8 flex items-center gap-2"><CaretLeftFill /> Competent</span>
					<span class="absolute -bottom-8 -left-12 min-w-[10rem] flex items-center gap-1">Not Competent <CaretRightFill /></span>
				</div>
			{/if}
		</div>


		<div class="absolute left-0">
			{#each applicants as applicant (applicant.id)}
				<div class="w-12 h-12 opacity-0 absolute -translate-y-2"
						 use:animate={{anims:[{
												type: 'to',
												xPercent: 80,
												opacity: 0.3,
												color: applicant.color,
												duration: 0.7,
												ease: 'ease-in-out',
											},
											{
												type: 'to',
												xPercent: 160,
												delay: 3.1,
												opacity: 0.6,
												duration: 0.7,
												ease: 'ease-in-out',
											},
											{
												type: 'to',
												xPercent: 240,
												delay: 3.1,
												opacity: 1,
												duration: 0.7,
												ease: 'ease-in-out',
											},
											{
												type: 'to',
												xPercent: 380,
												delay: 3.1,
												opacity: 1,
												duration: 0.7,
												ease: 'ease-in-out',
												onComplete: () => {addApplication(applicant.hired)}
											},
											{
													type: 'to',
													delay: 1,
													duration: 1,
													ease: 'power1.inOut',
													motionPath: {
														path:"M 0 0 C -52 59 135 159 278 117",
														align: "self",
													}
												},
												{
													type: 'to',
													delay: 2,
													scale: showCompetence ? 0.6 : 1,
													xPercent: !showCompetence
													? 850 + (applicant.indexInHireClass % 10) * 80
													: 820 + (applicant.indexInHireClass % 5) * 50 + (applicant.competent ? 0 : 340),
													yPercent: !showCompetence
													? (applicant.hired ? -434 : -117) + (applicant.hired ? -120 : 120) * Math.floor(applicant.indexInHireClass / 10)
													: (applicant.hired ? -510 : -200) + 60 * Math.floor(applicant.indexInHireClass / 5),
													duration: 1,
													ease: 'power1.inOut',
												}],
						}}>
					<PersonIcon />
				</div>
			{/each}


			{#each applications as application (application.id)}
				<div class="w-12 h-12 absolute translate-x-[420%] scale-50 translate-y-[-40%]"
						 use:animate={{anims:[{
													type: 'from',
													scale: 0,
													duration: 0.5,
													ease: 'ease-out',
												},
											{
												type: 'to',
												scale: 1,
												xPercent: 750,
												delay: 0.2,
												duration: 1.8,
												ease: 'ease-in-out',
											},
											{
												type: 'to',
												scale: 1,
												xPercent: 900,
												color: application.hired ? "green" : "red",
												delay: 0.6,
												duration: 0.3,
												ease: 'ease-in-out',

											},
											{
												type: 'to',
												scale: 1,
												opacity: 0,
												delay: 1.6,
												duration: 0.3,
												ease: 'ease-in-out',
											},
											],
											then: () => {
           applications = applications.filter(a => a.id !== application.id);
         }
						}}>
					<ApplicationIcon />
				</div>
			{/each}


		</div>
		<div class=" overflow-none flex items-center justify-center h-[20rem] w-[16rem]"
				 use:animate={{anims:[{
					type: 'from',
					scale: 1.04,
					duration: 0.3,
					repeat: -1,
					yoyo: true,
					ease: "none"
				}]}}>
			<div class="absolute pl-4">
				Recruiter
			</div>

			<RecruiterBox />

		</div>

	</div>
</div>