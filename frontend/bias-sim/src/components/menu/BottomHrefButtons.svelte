<script lang="ts">
	import { BoxArrowUpRight } from 'svelte-bootstrap-icons';

	type HrefButtonInfo = {
		name: string
		slug: string
	}

	export let buttonInfos: HrefButtonInfo[];
</script>

<div class="w-full">
	{#each buttonInfos as buttonInfo, index}
		<button
			class="btn rounded-none variant-ghost-secondary ring-0 { (index % 2 === 0) ? 'bg-primary-900' : 'bg-primary-800'}
								text-2xl py-6 text-left font-semibold text-white w-full justify-start"
			on:click={() => window.location.href = buttonInfo.slug}>
			<div class="flex flex-row justify-between w-full items-center">
				{buttonInfo.name}
				<BoxArrowUpRight width={24} height={24} />
			</div>
		</button>
	{/each}
</div>