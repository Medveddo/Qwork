<script>
	export let found_features;
	export let missing_features;
</script>

<div class="flex w-full">
	<div class="grid h-max w-max flex-grow card bg-green-200 rounded-box place-items-center">
		<strong>Признаки найдены</strong>
		{#if found_features}
			<ol class="list-decimal w-max">
				{#each found_features as found_feature}
					<li>{found_feature}</li>
				{/each}
			</ol>
		{/if}
	</div>
	<div class="divider divider-horizontal" />
	<div class="grid h-max w-max flex-grow card bg-red-200 rounded-box place-items-center">
		<strong>Признаки отсутствуют</strong>
		{#if missing_features}
			<ol class="list-decimal w-max">
				{#each missing_features as missing_feature}
					<li>{missing_feature}</li>
				{/each}
			</ol>
		{/if}
	</div>
</div>
