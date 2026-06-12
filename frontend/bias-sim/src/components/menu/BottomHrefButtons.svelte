<script lang="ts">
	import { BoxArrowUpRight } from 'svelte-bootstrap-icons';

	type HrefButtonInfo = {
		name: string;
		slug: string;
	};

	export let buttonInfos: HrefButtonInfo[];
</script>

<div class="w-full">
	{#each buttonInfos as buttonInfo, index}
		<button
			class="variant-ghost-secondary btn rounded-none ring-0 {index % 2 === 0
				? 'bg-primary-900'
				: 'bg-primary-800'}
								w-full justify-start py-6 text-left text-2xl font-semibold text-white"
			on:click={() => (window.location.href = buttonInfo.slug)}
		>
			<div class="flex w-full flex-row items-center justify-between">
				{buttonInfo.name}
				<BoxArrowUpRight width={24} height={24} />
			</div>
		</button>
	{/each}
</div>
