<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	export let isLoading: boolean;
	export let loadingText: string = 'Loading';
</script>

{#if isLoading}
	<div
		class="absolute w-[100vw] h-[100vh] flex justify-center items-center bg-surface-800 bg-opacity-80">
		<div class="flex flex-col items-center">
			<ProgressRadial value={undefined} width="w-[10rem]" meter="stroke-primary-200" track="stroke-primary-400" />
			<h3 class="text-[4rem] font-bold mt-16 text-center text-surface-100">{loadingText}...</h3>
		</div>
	</div>
{/if}