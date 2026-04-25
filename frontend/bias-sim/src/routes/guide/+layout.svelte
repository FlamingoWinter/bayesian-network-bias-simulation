<script>
	import LeftDrawerGuide from '../../components/menu/LeftDrawerGuide.svelte';
</script>

<div class="flex h-[100vh] overflow-y-scroll">
	<LeftDrawerGuide />
	<div class="w-full pl-[20rem] pt-8">
		<slot />
	</div>
</div>
