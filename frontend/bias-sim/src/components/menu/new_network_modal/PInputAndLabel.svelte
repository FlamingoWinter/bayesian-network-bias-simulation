<script lang="ts">
	import PInput from './PInput.svelte';

	export let p: number;
	export let label: string;
	export let onChange: () => void;

</script>

<div class="flex flex-col items-center">
	<h3 class="text-md text-center font-bold">{label}:</h3>
	<PInput bind:p={p} onChange={onChange} />
</div>