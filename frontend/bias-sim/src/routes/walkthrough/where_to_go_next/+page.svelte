<script>
	import VisualisationButton from '../../../components/home/VisualisationButton.svelte';
</script>

<h3 class="mt-2 p-8 text-6xl font-bold">Where to Go Next</h3>
<div class="flex justify-center pb-10 pt-4 text-center">
	<div class="flex max-w-[40rem] flex-col items-center text-lg">
		<div class="mb-8">
			<p>Thanks for reading!</p>
			<p class="mt-8">You can try out the simulation for yourself here:</p>
		</div>

		<VisualisationButton center={true} />

		<div class="mb-8 mt-16">
			<p>
				If you have some technical background and want to get into some of the details, take a look
				at:
			</p>
		</div>
	</div>
</div>
