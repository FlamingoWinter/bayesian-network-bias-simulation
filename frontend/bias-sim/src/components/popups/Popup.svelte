<script lang="ts">
	export let content: string;
	export let dataPopup: string;
</script>

<div class="card variant-filled-primary rounded-xl p-4" data-popup={dataPopup}>
	<p class="max-w-72 whitespace-pre-line text-center">{content}</p>
	<div class="variant-filled-primary arrow" />
</div>
