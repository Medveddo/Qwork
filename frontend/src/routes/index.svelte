<script context="module">
	export async function load({ params }) {
		const backend_host = import.meta.env.VITE_API_URL;
		const stats_url = backend_host + 'stats';

		const res = await fetch(stats_url);
		const stats_data = await res.json();
		return { props: { stats: stats_data } };
	}
</script>

<script>
	import Home from '../components/home.svelte';
	import Stat from '../components/stat.svelte';
	export let stats;
</script>

<Home />
<Stat stats={stats} />