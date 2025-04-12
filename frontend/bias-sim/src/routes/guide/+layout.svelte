<script>
	import LeftDrawerGuide from '../../components/menu/LeftDrawerGuide.svelte';
</script>

<div class="flex h-[100vh] overflow-y-scroll">
	<LeftDrawerGuide />
	<div class="pl-[20rem] w-full pt-8">
		<slot />
	</div>
</div>

