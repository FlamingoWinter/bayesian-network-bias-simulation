<script lang="ts">

	type UtilityButtonInfo = {
		name: string
		callback: () => void,
		inset?: string
		textSize?: string
	}

	export let utilityButtonInfos: UtilityButtonInfo[];
</script>

{#each utilityButtonInfos as utilityButtonInfo, index}
	<div class="{utilityButtonInfo.inset ?? ''} w-full">
		<button
			class="btn rounded-none variant-ghost-secondary ring-0 { (index % 2 === 0) ? 'bg-primary-900' : 'bg-primary-800'}
								{utilityButtonInfo.textSize ?? 'text-xl'} pl-4 py-5 text-left font-semibold text-white w-full justify-start"
			on:click={utilityButtonInfo.callback}>
			<div class="flex flex-row justify-between w-full items-center">
				{utilityButtonInfo.name}

			</div>
		</button>
	</div>
{/each}