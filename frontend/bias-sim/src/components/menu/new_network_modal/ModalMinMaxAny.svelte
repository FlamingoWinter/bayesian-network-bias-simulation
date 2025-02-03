<div class="flex flex-row items-center gap-10 justify-start flex-grow">
	<div class="flex flex-row items-center gap-4 justify-start">
		<h3 class="text-md font-bold">Min:</h3>
		<input class="p-2 rounded-container-token w-[6rem] {minError ? 'variant-ringed-error':'variant-ringed'}"
					 type="number" placeholder="Min..."
					 min={minBound} max={maxBound}
					 bind:value={min}
					 bind:this={minField}
					 step={step}
					 on:input={()=>{validateInput(); any = false}} />
	</div>
	<div class="flex flex-row items-center gap-4 justify-start">
		<h3 class="text-md font-bold ">Max:</h3>
		<input class=" p-2 rounded-container-token w-[6rem] {maxError ? 'variant-ringed-error':'variant-ringed'}"
					 type="number" placeholder="Max..."
					 min={minBound} max={maxBound}
					 bind:value={max}
					 bind:this={maxField}
					 step={step}
					 on:input={()=>{validateInput(); any = false}} />
	</div>
</div>
<RadioGroup rounded="rounded-container-token">
	<RadioItem bind:group={any} name="justify"
						 value={true}
						 on:click={()=>{if(!any){minField.value=""; maxField.value = ""}}}>Any
	</RadioItem>
</RadioGroup>

<script lang="ts">

	import { RadioGroup, RadioItem } from '@skeletonlabs/skeleton';

	let minField: HTMLInputElement;
	let maxField: HTMLInputElement;

	let minError: boolean;
	let maxError: boolean;


	export let minBound: number;
	export let maxBound: number;
	export let step: number = 1;

	export let min: number | '' = '';
	export let max: number | '' = '';
	export let any: boolean;


	const validateInput = () => {
		if (min != '') {
			minError = !(minBound <= min && min <= maxBound);
		}
		if (max != '') {
			maxError = !(minBound <= max && max <= maxBound);
		}
	};

</script>