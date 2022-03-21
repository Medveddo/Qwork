<script>
	import { onMount, onDestroy } from "svelte";
	import TextInfo from '../components/textInfo.svelte'

	// import dotenv from 'dotenv'

	// dotenv.config()

	// export const env = process.env
	
	let time = '';
	let text_to_process = 'Температура 37.9. Давление высокое - 120 на 80.';
	// const backend_host = env.API_URL
	const backend_host = "http://localhost:8000/api/"
	let text_info_result = null;
	
	async function fetchData() {
		console.log("Fetch")
		const url = backend_host + `now`;
		const res = await fetch(url);
		const data = await res.json();
		time = data.time;
	}

	const interval = setInterval(async () => {
		fetchData();
	}, 60000);

	onMount(async () => {
		fetchData();
	});

	onDestroy(() => clearInterval(interval));

	const processText = async () => {
		console.log(text_to_process)
		const url = backend_host + 'process_text'
		const res = await fetch(url, {
			method: "POST",
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({text: text_to_process})
		})
		const data = await res.json()
		console.log(data)
		text_info_result = data
	}

	const clearInfo = async () => {
		text_info_result = null;
	}

</script>

<p class="text-center">Time from server: {time}</p>
<h1 class="uppercase text-2xl text-center">Text processing system</h1>
<div class="text-center">
	<button class="border-4 border-red-300 bg-green-200" on:click={fetchData}>Refresh time</button>
</div>
<div class="text-center py-4">
	<textarea class="border-4 border-gray-400 text-center" placeholder="Text to process" bind:value={text_to_process} cols=40 rows=5/>
</div>
<div class="text-center pb-5">
	<button class="border-2" on:click={processText}>Process text</button>
</div>
{#if text_info_result}
	<TextInfo {...text_info_result} />
	<div class="text-center">
		<button class="mt-3 uppercase border-2 border-red-600 bg-red-300" on:click={clearInfo}>Clear info</button>
	</div>
{/if}