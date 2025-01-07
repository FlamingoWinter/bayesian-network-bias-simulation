import type { Component } from 'svelte';

function renderSvelteComponentToString(component: Component) {
	const tempContainer = document.createElement('div');
	new component({
		target: tempContainer,
		props: {}
	});

	return tempContainer.innerHTML;
}