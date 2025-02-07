<text x={0} y={-rectHeight /2 - 7} text-anchor="middle" fill="#333333" font-weight="600" font-size="18px"
			class="max-w-1">
	{#each textWrappedTitle as line, i}
		<tspan x="0" dy="{i===0 ? (-20) * textWrappedTitle.length + 20 : 20}">{line}</tspan>
	{/each}
</text>

<script lang="ts">
	import { toTitleCase } from '../../utiliites/toTitleCase.js';

	export let nodeId: string;
	export let rectHeight: number;

	$: textWrappedTitle = textWrap(toTitleCase(nodeId), 20);

	function textWrap(text: string, n: number) {
		const words = text.split(' ');
		const wrappedWords: string[] = [words[0]];
		let lettersLeft = n - words[0].length;
		words.slice(1).forEach(word => {
			if (lettersLeft < word.length) {
				lettersLeft = n;
				wrappedWords.push(word);
			} else {
				wrappedWords[wrappedWords.length - 1] += ` ${word}`;
			}
			lettersLeft -= word.length + 1;
		});
		return wrappedWords;
	}
</script>

