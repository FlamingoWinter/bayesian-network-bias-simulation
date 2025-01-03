<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<script lang="ts">
	import { onMount } from 'svelte';


	onMount(async () => {
		const response = await fetch('http://localhost:8000/');
		console.log(await (response.json()));
	});

</script>


<svg id="graph"></svg>
