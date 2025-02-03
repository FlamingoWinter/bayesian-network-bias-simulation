<script lang="ts">
	import { InfoLg } from 'svelte-bootstrap-icons';
	import { popup } from '@skeletonlabs/skeleton';

	// The popup itself needs to be declared in ModalPopups
	export let target: string;
	export let link: string | undefined = undefined;
</script>

<button class="btn btn-icon variant-outline-surface [&>*]:pointer-events-none w-8" use:popup={{
						event: 'hover',
						target: target,
						placement: 'top',
					}}
				on:click={()=>{if (link!==undefined) window.open(`${link}`, "_blank");}}>
	<InfoLg />
</button>

