<script lang="ts">
	import { onMount } from 'svelte';
	import { conditioned, conditions, posteriorDistributions } from '../stores/store';
	import { apiRequest } from '../utiliites/api';
	import { condition } from '../stores/functions';


	onMount(async () => {
		console.log($posteriorDistributions);
		$condition = async (characteristic: string, value: number) => {
			$conditions[characteristic] = value;

			const conditionResponse = await apiRequest('condition/', 'POST', JSON.stringify($conditions)) as Record<string, number[]>;

			$conditioned = true;
			$posteriorDistributions = conditionResponse;
		};
	});
</script>
