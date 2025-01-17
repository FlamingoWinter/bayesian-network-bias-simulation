<script lang="ts">
	import { onMount } from 'svelte';
	import { conditioned, conditions, posteriorDistributions } from '../stores/store';
	import { apiRequest } from '../utiliites/api';
	import { condition, deconditionAll } from '../stores/functions';
	import { getToastStore, type ToastSettings } from '@skeletonlabs/skeleton';

	const toastStore = getToastStore();


	onMount(async () => {
		$condition = async (characteristic: string, value: number | null) => {
			const tempConditions = { ...$conditions };
			if (value === null) {
				delete tempConditions[characteristic];
			} else {
				tempConditions[characteristic] = value;
			}

			let conditionResponse: Record<string, number[]> = {};
			try {
				if (Object.keys(tempConditions).length > 0) {
					conditionResponse = await apiRequest('condition/', 'POST', JSON.stringify(tempConditions)) as Record<string, number[]>;
				}
				$conditions = tempConditions;
				$conditioned = Object.keys(tempConditions).length > 0;
				$posteriorDistributions = conditionResponse;
			} catch (e) {
				const t: ToastSettings = {
					message: 'Conditioning for this variable failed. Did you try to condition on impossible evidence?',
					timeout: 3000,
					background: 'variant-filled-error'
				};
				toastStore.trigger(t);
			}
		};

		$deconditionAll = async () => {
			$conditions = {};
			$conditioned = false;
		};
	});
</script>
