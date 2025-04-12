<script lang="ts">
	import { getDrawerStore, getModalStore, type ModalComponent, type ModalSettings } from '@skeletonlabs/skeleton';
	import MenuButton from '../menu/MenuButton.svelte';

	const modalStore = getModalStore();
	const drawerStore = getDrawerStore();

	export let component: ModalComponent;
	export let classList: string = '';


	const modal: ModalSettings = {
		type: 'component',
		component: component,
		backdropClasses: 'bg-gradient-to-tr from-indigo-500/50 via-purple-500/50 to-pink-500/50'
	};
</script>


<MenuButton classList={classList} callback={()=>{	modalStore.trigger(modal); drawerStore.close();}}>
	<slot />
</MenuButton>

