<script lang="ts">
	import { onMount } from 'svelte';
	import { conditioned, conditionedDistributions, conditions } from '../stores/store';
	import { apiRequest } from '../utiliites/api';
	import { condition } from '../stores/functions';


	onMount(async () => {
		$condition = async (characteristic: string, value: number) => {
			$conditions[characteristic] = value;

			const conditionResponse = await apiRequest('condition/', 'POST', JSON.stringify($conditions)) as Record<string, number[]>;

			$conditioned = true;
			$conditionedDistributions = conditionResponse;
		};
	});
</script>
