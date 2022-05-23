<script>
	import FoundMissingFeatures from '../components/found_missing_features.svelte';

	const backend_host = import.meta.env.VITE_API_URL;
	const getHistory = async function () {
		const url = backend_host + `history`;
		const res = await fetch(url);
		const data = await res.json();

		return data;
	};
	let runs = [];
	getHistory().then((data) => {
		console.log(data);
		runs = data;
	});
</script>

<div class="mx-10">
	{#each runs as run, i}
		<div class="collapse border border-base-300">
			<input type="checkbox" />
			<div class="collapse-title">
				<span class="text-xl">{i + 1}</span>
				{run.text}
			</div>
			<div class="collapse-content">
				<FoundMissingFeatures
					found_features={run.result.found_features}
					missing_features={run.result.missing_features}
				/>
			</div>
		</div>
	{/each}
</div>
