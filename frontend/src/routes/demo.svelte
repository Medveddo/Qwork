<script>
	import { onMount, onDestroy } from 'svelte';

	import { text_process_result } from '../stores.js';

	import TextInfo from '../components/textInfo.svelte';

	const environment = import.meta.env.VITE_ENVIRONMENT;
	const backend_host = import.meta.env.VITE_API_URL;
	console.log(environment);
	console.log(backend_host);

	const EXAMPLE_TEXT = 'Температура 37.9. Давление высокое - 120 на 80.';
	let text_info_result = null;

	// User input bindings
	let user_input = '';
	let text_type_option = 'Тип заболевания';

	let is_active_error = false;
	let error_message = '';

	function clearError() {
		error_message = '';
		is_active_error = false;
	}

	function setExampleText() {
		user_input = EXAMPLE_TEXT;
	}

	const processText = async () => {
		console.log(text_type_option);
		if (user_input === '') {
			error_message = 'Текст для обработки не может быть пустым';
			is_active_error = true;
		}
		const url = backend_host + 'process_text_instant';
		const res = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				text: user_input,
				type: text_type_option
			})
		});
		const data = await res.json();
		console.log(data);
		// text_info_result = data;
        text_process_result.set(data)
	};

	const clearInfo = async () => {
		text_info_result = null;
	};
</script>

<main class="flex-grow">
	{#if is_active_error}
		<div class="alert alert-error shadow-lg">
			<div>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="stroke-current flex-shrink-0 h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					><path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
					/></svg
				>
				<span>{error_message}</span>
			</div>

			<div class="flex-none">
				<button class="btn btn-circle" on:click={clearError}>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						><path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						/></svg
					>
				</button>
			</div>
		</div>
	{/if}

	<div class="flex flex-col items-center justify-center">
		<div class="form-control">
			<div class="input-group">
				<select class="select select-bordered" bind:value={text_type_option}>
					<!-- https://svelte.dev/tutorial/select-bindings -->
					<option disabled selected>Тип заболевания</option>
					<option>Острокоронарный синдром ❤️</option>
				</select>
			</div>
		</div>
		<textarea
			class="textarea textarea-primary my-2"
			bind:value={user_input}
			placeholder={EXAMPLE_TEXT}
			cols="60"
			rows="5"
		/>
		<br />
		<button class="btn btn-accent w-64 rounded-full" on:click={setExampleText}
			>Вставить пример текста</button
		>
		<button class="btn btn-secondary w-64 rounded-full my-2" on:click={processText}
			>Обработать и проверить</button
		>
		<button class="btn loading">loading</button>
		
        <TextInfo />

	</div>
</main>
