<script>
	import MoreInfoButton from '../../../components/home/MoreInfoButton.svelte';
	import VisualisationButton from '../../../components/home/VisualisationButton.svelte';
</script>

<h3 class="text-6xl font-bold mt-2 p-8">
	Where to Go Next
</h3>
<div class="flex justify-center pt-4 pb-10 text-center">
	<div class="text-lg max-w-[40rem] flex flex-col items-center">
		<div class="mb-8">
			<p>
				Thanks for reading!
			</p>
			<p class="mt-8">
				You can try out the simulation for yourself here:
			</p>
		</div>

		<VisualisationButton center={true} />

		<div class="mb-8 mt-16">
			<p>
				If you have some technical background and want to get into some of the details, take a look at:
			</p>
		</div>
		<MoreInfoButton center={true} />

	</div>
</div>