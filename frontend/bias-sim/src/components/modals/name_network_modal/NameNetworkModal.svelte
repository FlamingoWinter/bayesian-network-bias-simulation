{#if $modalStore[0]}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
	<div class="h-full flex flex-col gap-5 justify-center items-center">
		<div transition:fade={{ duration: 400 } } on:click|stopPropagation role="alertdialog"
				 class="card p-4 bg-surface-200-700-token view w-[50vw] min-w-64 h-[40rem] max-h-[90vh] overflow-y-scroll drop-shadow-md rounded-lg flex flex-col justify-between">
			<div>
				<ModalDivider />
				<ModalRow center={false}>
					<h3 class="text-2xl font-bold  text-center">Name Network</h3>
				</ModalRow>
				<p class="px-20 py-4 whitespace-pre-line text-center">
					{caveatString}
				</p>
			</div>

			<footer class="flex justify-end">
				<div class="flex gap-2">
					<button class="btn variant-outline-primary" on:click={()=>{modalStore.close()}}>Cancel</button>
					<button class="btn variant-outline-secondary"
									on:click={async ()=>{
							await awaitSocketClose(nameNetworkSocket)

							nameNetworkSocket = await awaitSocketOpen(new WebSocket(`${webSocketUrl}/name-network/?session_key=${$sessionKey}`));
							await nameNetworkSocket.send("")
							modalStore.close()

							await $deconditionAll()

							await $loadProcess(nameNetworkSocket)
							await $invalidateNetwork()
						}}>Submit
					</button>
				</div>
			</footer>

		</div>
	</div>


{/if}

<ModalPopups />

<script lang="ts">

	import { fade } from 'svelte/transition';

	import { awaitSocketClose, awaitSocketOpen } from '../../../utiliites/socket';


	import { getModalStore } from '@skeletonlabs/skeleton';
	import ModalPopups from '../../popups/ModalPopups.svelte';

	import { webSocketUrl } from '../../../utiliites/api';
	import { deconditionAll, invalidateNetwork, loadProcess } from '../../../stores/functions';
	import { sessionKey } from '../../../stores/store';
	import ModalDivider from '../ModalDivider.svelte';
	import ModalRow from '../ModalRow.svelte';

	const modalStore = getModalStore();

	let nameNetworkSocket: WebSocket | undefined = undefined;

	const caveatString = `
This will generate randomised labels for each characteristic, using a small set of stochastic rules.

It's important to be aware that these characteristics are generated with little knowledge of actual
dependencies and are therefore solely illustrative.

This labelling of nodes isn't used within the dissertation.
The labelling will not represent true distributions in any job scenario and is only given here such that it may gave
some insight into how a protected characteristic may have an indirect dependency with actual job competency.

Additionally, some dependencies will be obviously wrong due to the primitive algorithm used to generate them.

By randomly labelling these nodes, you acknowledge that you won't interpret these labels as meaningful
predictions.`.split('\n\n').map((a) => {
		return a.split('\n').join(' ');
	}).join('\n\n');

</script>