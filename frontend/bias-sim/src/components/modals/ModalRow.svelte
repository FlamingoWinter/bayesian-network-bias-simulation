<div class="flex pt-4 pb-4 px-10 {center ? 'justify-evenly' : 'justify-between'} items-center gap-4 gap-{gap}">
	<slot />
</div>

<script lang="ts">
	export let center: boolean = true;
	export let gap: number = 4;
</script>