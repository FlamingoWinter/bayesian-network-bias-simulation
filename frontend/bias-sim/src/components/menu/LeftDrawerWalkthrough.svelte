<script lang="ts">
	import BottomHrefButtons from './BottomHrefButtons.svelte';
	import TopUtilityButtons from './TopUtilityButtons.svelte';

	let showBias: boolean = false;

	const menu = [
		'1) What are we Doing Here?',
		'2) How do we Simulate Candidates?',
		'3) What\'s a Recruiter, Exactly?',
		'4) How do we Measure Bias?',
		'5) Putting it all Together!',
		'6) Where to Go Next'
	];

	function toSlug(str: string) {
		if (str.substring(0, 1) == '1') {
			return '';
		}
		return str.toLowerCase().replace(/\s+/g, '_').substring(3).replace(/[^\w\s]/g, '');
	}

	const utilityButtonInfos = menu.map((title) =>
		({
			name: title, callback: () => window.location.href = '/walkthrough/' + toSlug(title), textSize: 'text-md'
		}));
</script>
<div class="pt-16 flex flex-col justify-between items-start  h-full">
	<div class="flex flex-col justify-start items-start w-full pr-4 gap-1">
		<TopUtilityButtons utilityButtonInfos={utilityButtonInfos} />
	</div>
	<BottomHrefButtons buttonInfos={[
			{name: "Visualisation", slug: "/visualisation"},
			{name: "Guide", slug: "/guide"},
		]} />
</div>
