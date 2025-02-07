<script lang="ts">
	import MenuButton from '../../menu/MenuButton.svelte';
	import { getModalStore, type ModalComponent, type ModalSettings } from '@skeletonlabs/skeleton';
	import NewNetworkModal from './NewNetworkModal.svelte';

	const modalStore = getModalStore();

	const modalComponent: ModalComponent = { ref: NewNetworkModal };

	const modal: ModalSettings = {
		type: 'component',
		component: modalComponent
	};
</script>


<MenuButton callback={()=>{	modalStore.trigger(modal)}}>
	New Network...
</MenuButton>

