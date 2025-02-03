<Popup dataPopup="number-of-nodes" content="The number of nodes in the generated network.
																						Between 1 and 50." />

<Popup dataPopup="allowed-parents"
			 content="The minimum and maximum number of direct parents any one variable can have.
								Between 1 and 4." />

<Popup dataPopup="allowed-mutual-information"
			 content="The minimum and maximum mutual information between a variable and the collection of its direct parents.
								Between 0.1 and 0.9." />

<Popup dataPopup="values-per-variable"
			 content="The distribution from which the number of values each variable may take is drawn." />


<script lang="ts">
	import Popup from './Popup.svelte';
</script>