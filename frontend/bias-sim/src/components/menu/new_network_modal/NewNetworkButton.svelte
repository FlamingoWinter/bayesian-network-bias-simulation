<script lang="ts">
	import MenuButton from '../MenuButton.svelte';
	import { getModalStore, type ModalComponent, type ModalSettings } from '@skeletonlabs/skeleton';
	import NewNetworkModal from './NewNetworkModal.svelte';

	const modalStore = getModalStore();

	let parent: MenuButton;
	const modalComponent: ModalComponent = { ref: NewNetworkModal };

	const modal: ModalSettings = {
		type: 'component',
		component: modalComponent
	};
</script>


<MenuButton callback={()=>{	modalStore.trigger(modal)}} bind:this={parent}>
	New Network...
</MenuButton>

