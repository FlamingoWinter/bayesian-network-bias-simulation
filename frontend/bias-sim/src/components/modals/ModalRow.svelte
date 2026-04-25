<script lang="ts">
	export let center: boolean = true;
	export let gap: number = 4;
</script>

<div
	class="flex px-10 pb-4 pt-4 {center
		? 'justify-evenly'
		: 'justify-between'} items-center gap-4 gap-{gap}"
>
	<slot />
</div>
