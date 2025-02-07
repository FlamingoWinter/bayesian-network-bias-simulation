<script lang="ts">
	import { getModalStore, type ModalComponent, type ModalSettings } from '@skeletonlabs/skeleton';
	import MenuButton from '../menu/MenuButton.svelte';

	const modalStore = getModalStore();

	export let component;

	const modalComponent: ModalComponent = { ref: component };

	const modal: ModalSettings = {
		type: 'component',
		component: modalComponent
	};
</script>


<MenuButton callback={()=>{	modalStore.trigger(modal)}}>
	<slot />
</MenuButton>

