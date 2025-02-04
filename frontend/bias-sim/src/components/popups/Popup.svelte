<div class="card p-4 variant-filled-primary rounded-xl" data-popup={dataPopup}>

	<p class="max-w-72 text-center whitespace-pre-line">{content}</p>
	<div class="arrow variant-filled-primary" />
</div>

<script lang="ts">
	export let content: string;
	export let dataPopup: string;
</script>