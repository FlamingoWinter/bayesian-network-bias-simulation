<script>
	import '../app.css';
	import { initializeStores, Modal, storePopup, Toast } from '@skeletonlabs/skeleton';
	import { arrow, autoUpdate, computePosition, flip, offset, shift } from '@floating-ui/dom';
	import Popups from '../components/popups/Popups.svelte';

	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

	initializeStores();
</script>
<Toast />
<Modal transitionInParams={{duration: 400}}
			 transitionOutParams={{duration: 400}} />

<Popups />

<slot></slot>


