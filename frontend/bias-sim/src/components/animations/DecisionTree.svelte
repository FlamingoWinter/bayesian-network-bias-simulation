<script lang="ts">
	import { onMount } from 'svelte';
	import { gsap } from 'gsap';

	import { animate, type AnimationOptions } from '../../animation/animate';
	import ApplicationIcon from '../svgs/ApplicationIcon.svelte';

	export let useAnimation: boolean = false;

	type RawTree = {
		label: string;
		child1?: RawTree;
		child2?: RawTree;
	};

	type PositionedTree = RawTree & {
		x: number;
		y: number;
	};

	const tree: RawTree = {
		label: 'Did they score 4,5 or 6 on the interview?',
		child1: {
			label: 'Did they go to Oxford?',
			child1: {
				label: 'Don\'t Hire'
			},
			child2: {
				label: 'Hire'
			}
		},
		child2: {
			label: 'Do they have above a B in GCSE maths?',
			child1: {
				label: 'Do they play piano?',
				child1: {
					label: 'Hire'
				},
				child2: {
					label: 'Don\'t Hire'
				}
			},
			child2: {
				label: 'Do they have good social skills?',
				child1: {
					label: 'Hire'
				},
				child2: {
					label: 'Don\'t Hire'
				}
			}
		}
	};

	type ApplicationInformation = {
		id: number
		firstLeft: boolean;
		secondLeft: boolean;
		thirdLeft: boolean;
	}

	let nodes: PositionedTree[] = [];
	let links: { x1: number; y1: number; x2: number; y2: number, isLeft: boolean }[] = [];
	let applications: ApplicationInformation[] = [];
	let applicantTimeline: gsap.core.Timeline | undefined;

	const horizontalSpacing = 200;
	const verticalSpacing = 400;
	let currentX = 1.5;

	function layout(node: RawTree, depth = 0): PositionedTree {

		const y = depth * verticalSpacing;

		let left: PositionedTree | undefined;
		let right: PositionedTree | undefined;

		if (node.child1) {
			left = layout(node.child1, depth + 1);
		}
		if (node.child2) {
			right = layout(node.child2, depth + 1);
		}

		let x: number;
		if (left && right) {
			x = (left.x + right.x) / 2;
		} else if (left) {
			x = left.x;
		} else if (right) {
			x = right.x;
		} else {
			x = currentX * horizontalSpacing;
			currentX++;
		}

		const positioned = { ...node, x, y };
		nodes.push(positioned);

		if (left)
			links.push({ x1: x - 20, y1: y + 30, x2: left.x, y2: left.y - 40, isLeft: true });
		if (right)
			links.push({ x1: x + 20, y1: y + 30, x2: right.x, y2: right.y - 40, isLeft: false });

		return positioned;
	}

	layout(tree);

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

	onMount(() => {
		applicantTimeline = gsap.timeline({ paused: false });

	});

	function startAnimation() {
		function addApplication() {
			applications.push({
				id: applications.length + 1,
				firstLeft: Math.random() < 0.5,
				secondLeft: Math.random() < 0.5,
				thirdLeft: Math.random() < 0.5
			});
			applications = applications;
		}

		addApplication();
		applicantTimeline?.to({}, {
			duration: 10, repeat: -1,
			onRepeat: addApplication
		});
	}

	function finalAnimation(application: ApplicationInformation) {
		return {
			type: 'to',
			scale: 1,
			xPercent: application.secondLeft
				? application.thirdLeft ? -330 : -20
				: application.thirdLeft ? 150 : 430,
			yPercent: 1060,
			delay: 2,
			duration: 1,
			ease: 'ease-in-out'
		} as AnimationOptions;
	}
</script>

<div class="flex items-center" use:onEnterViewport={{ callback: startAnimation }}>
	<div class="flex justify-center w-[40rem] h-full">
		<svg class="w-full h-full" viewBox="-100 -100 1600 1400">
			{#if useAnimation}
				{#each applications as application (application.id)}
					<g transform={`translate(960, -10)`}
						 use:animate={{anims: [
								{ type: 'from', scale: 0, duration: 0.5, ease: 'ease-out' },
								{
									type: 'to',
									scale: 1,
									xPercent: application.firstLeft ? -330 : 280,
									yPercent: 400,
									delay: 2,
									duration: 1,
									ease: 'ease-in-out',
								},
								{
									type: 'to',
									scale: 1,
									xPercent: application.firstLeft
										? application.secondLeft ? -690 : -480
										: application.secondLeft ? -300 : 470,
									yPercent: application.firstLeft
										? 900
										: application.secondLeft ? 660 : 800,
									delay: 2,
									duration: 1,
									ease: 'ease-in-out',
								},
								...(!application.firstLeft
									? [finalAnimation(application)]
									: []),
									{
									type: 'to',
									scale: 1,
									delay: 0,
									color: application.firstLeft
									? application.secondLeft ? "red" : "green"
									: application.thirdLeft ? "green" : "red",
									duration: 1,
									ease: 'ease-in-out',
								},
								{
									type: 'to',
									scale: 1,
									opacity: 0,
									delay: 1,
									duration: 1,
									ease: 'ease-in-out',
								},
							]

						}}>
						<foreignObject x="-25" y="-25" width="100" height="100">
							<ApplicationIcon />
						</foreignObject>
					</g>
				{/each}
			{/if}

			<!-- Lines -->
			{#each links as { x1, y1, x2, y2, isLeft }}
				<line x1={x1} y1={y1} x2={x2} y2={y2} stroke="gray" stroke-width="2" />
				<g transform={`translate(${(x1 + x2) / 2}, ${(y1 + y2) / 2})`}>
					<foreignObject x="-200" y="-40" width="400" height="400">
						<div>
							<p class="text-3xl font-bold text-center flex justify-center ">
						<span class="w-fit p-2 rounded-xl bg-white">
							{isLeft ? 'Yes' : 'No'}
						</span>
							</p>

						</div>
					</foreignObject>
				</g>
			{/each}

			<!-- Nodes -->
			{#each nodes as { x, y, label }}
				<g transform={`translate(${x}, ${y})`}>
					<foreignObject x="-200" y="-40" width="400" height="400">
						<div>
							{#if label === "Hire" || label === "Don\'t Hire"}
								<p class="text-3xl font-bold text-center {label === 'Hire' ? 'text-success-200'
																										: 'text-error-200'} flex justify-center ">
							<span class="w-fit border-4 p-4 rounded-xl bg-gray-600">
							{label}
							</span>
								</p>
							{:else}
								<p class="text-3xl font-bold text-center text-surface-600  flex justify-center bg-white">
							<span class="w-fit border-4 p-4 rounded-xl">
							{label}
							</span>
								</p>
							{/if}
						</div>
					</foreignObject>
				</g>
			{/each}
		</svg>
	</div>
</div>