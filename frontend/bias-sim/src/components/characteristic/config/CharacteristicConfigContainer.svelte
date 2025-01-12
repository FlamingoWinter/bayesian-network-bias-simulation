<!--svelte-ignore a11y-mouse-events-have-key-events-->
<!--svelte-ignore a11y-no-static-element-interactions-->
<foreignObject height={expanded ? height * heightMultiplier : height}
							 width={width}
							 class="expand-button-container"
							 x={-width / 2}
							 y={-height / 2}
							 style="pointer-events: all;
											transition: height 500ms cubic-bezier(0.68, -0.55, 0.27, 1.55);
											z-index: 20"
							 on:mouseover={() => {isHovered = true}}
							 on:mouseleave={() => {isHovered = false}}>
	<slot />
</foreignObject>

<script lang="ts">
	export let height: number;
	export let width: number;
	export let heightMultiplier: number;
	export let expanded: boolean;
	export let isHovered: boolean;
</script>