<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	export let isLoading: boolean;
	export let loadingText: string = 'Loading';
</script>

{#if isLoading}
	<div
		class="absolute flex h-[100vh] w-[100vw] items-center justify-center bg-surface-800 bg-opacity-80"
	>
		<div class="flex flex-col items-center">
			<ProgressRadial
				value={undefined}
				width="w-[10rem]"
				meter="stroke-primary-200"
				track="stroke-primary-400"
			/>
			<h3 class="mt-16 text-center text-[4rem] font-bold text-surface-100">{loadingText}...</h3>
		</div>
	</div>
{/if}
