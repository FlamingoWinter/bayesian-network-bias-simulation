<script lang="ts">
	export let number: number;
	export let link: string;
</script>
<a href={link} target="_blank" class="font-bold text-secondary-600 underline">
	<sup class="-ml-1">[{number}]</sup>
</a>