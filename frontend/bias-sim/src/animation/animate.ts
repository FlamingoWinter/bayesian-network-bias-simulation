// From https://jasperclarke.com/blog/gsap-svelte

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { MotionPathPlugin } from 'gsap/MotionPathPlugin';

gsap.registerPlugin(ScrollTrigger);
gsap.registerPlugin(MotionPathPlugin);
type AnimationType = keyof typeof gsap;

export interface AnimationOptions extends GSAPTweenVars {
	type: AnimationType;
	scrollTrigger?: ScrollTrigger.Vars;
}

export type AnimateOptions = {
	anims: AnimationOptions[];
	then?: () => void;
};

export function animate(node: any, options: AnimateOptions): { destroy?: () => void } {
	gsap.registerPlugin(ScrollTrigger);

	const timeline = gsap.timeline({
		onComplete: () => {
			if (options.then !== undefined) {
				options.then();
			}
		}
	});

	for (let animationOption of options.anims) {
		const method = gsap[animationOption.type] as
			| ((target: gsap.TweenTarget, vars: GSAPTweenVars) => GSAPTween)
			| undefined;
		if (!method) {
			console.warn(`GSAP method "${animationOption.type}" does not exist.`);
			return {};
		}
		timeline.add(
			method(node, {
				...animationOption,
				scrollTrigger: animationOption?.scrollTrigger
					? {
							...animationOption?.scrollTrigger,
							trigger: animationOption?.scrollTrigger.trigger || node
						}
					: undefined,
				type: undefined
			})
		);
	}

	// Create the animation with ScrollTrigger if provided

	return {
		destroy() {
			timeline.kill();
			// If using ScrollTrigger, make sure to kill that instance too
			if (timeline?.scrollTrigger) {
				timeline.scrollTrigger.kill();
			}
		}
		// Kill the animation when the element is removed
	};
}
