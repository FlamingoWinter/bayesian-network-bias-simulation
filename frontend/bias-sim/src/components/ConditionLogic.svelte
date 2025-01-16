<script lang="ts">
	import { onMount } from 'svelte';
	import { conditioned, conditions, posteriorDistributions } from '../stores/store';
	import { apiRequest } from '../utiliites/api';
	import { condition } from '../stores/functions';


	onMount(async () => {
		$condition = async (characteristic: string, value: number | null) => {
			const tempConditions = { ...$conditions };
			if (value === null) {
				delete tempConditions[characteristic];
			} else {
				tempConditions[characteristic] = value;
			}

			const conditionResponse = await apiRequest('condition/', 'POST', JSON.stringify(tempConditions)) as Record<string, number[]>;

			$conditions = tempConditions;
			$conditioned = true;
			$posteriorDistributions = conditionResponse;
		};
	});
</script>
