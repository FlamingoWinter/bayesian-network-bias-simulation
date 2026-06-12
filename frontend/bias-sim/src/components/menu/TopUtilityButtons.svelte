<script lang="ts">
	type UtilityButtonInfo = {
		name: string;
		callback: () => void;
		inset?: string;
		textSize?: string;
	};

	export let utilityButtonInfos: UtilityButtonInfo[];
</script>

{#each utilityButtonInfos as utilityButtonInfo, index}
	<div class="{utilityButtonInfo.inset ?? ''} w-full">
		<button
			class="variant-ghost-secondary btn rounded-none ring-0 {index % 2 === 0
				? 'bg-primary-900'
				: 'bg-primary-800'}
								{utilityButtonInfo.textSize ??
				'text-xl'} w-full justify-start py-3 pl-4 text-left font-semibold text-white"
			on:click={utilityButtonInfo.callback}
		>
			<div class="flex w-full flex-row items-center justify-between">
				{utilityButtonInfo.name}
			</div>
		</button>
	</div>
{/each}
