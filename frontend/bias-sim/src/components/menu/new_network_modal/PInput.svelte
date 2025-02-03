<input class=" p-2 rounded-container-token w-[5rem] {error ? 'variant-ringed-error':'variant-ringed'}"
			 type="number" placeholder="Max..."
			 min={0} max={1}
			 bind:value={p}
			 step={0.01}
			 on:input={()=>{validateInput()}}
			 on:change={onChange} />

<script lang="ts">
	export let p: number | '';
	export let onChange: () => void;


	let error: boolean;

	const validateInput = () => {
		if (p != '') {
			error = !(0 <= p && p <= 1);
		}
	};
</script>