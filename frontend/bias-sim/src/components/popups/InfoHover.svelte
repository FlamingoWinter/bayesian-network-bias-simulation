<script lang="ts">
	import { InfoLg } from 'svelte-bootstrap-icons';
	import { popup } from '@skeletonlabs/skeleton';

	export let target: string;
	export let link: string | undefined = undefined;
</script>

<button
	class="variant-outline-surface btn btn-icon w-8 [&>*]:pointer-events-none"
	use:popup={{
		event: 'hover',
		target: target,
		placement: 'top'
	}}
	on:click={() => {
		if (link !== undefined) window.open(`${link}`, '_blank');
	}}
>
	<InfoLg />
</button>
