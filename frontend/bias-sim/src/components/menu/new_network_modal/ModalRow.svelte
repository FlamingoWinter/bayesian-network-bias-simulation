<div class="flex pt-2 pb-4 px-10 {center ? 'justify-evenly' : 'justify-between'} items-center gap-2">
	<slot />
</div>

<script lang="ts">
	export let center: boolean = true;
</script>