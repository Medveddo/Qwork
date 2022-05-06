<script>
	import { onDestroy } from 'svelte';

	import { fade } from 'svelte/transition';

	import { text_process_result } from '../stores.js';

	let info = {};

	const unsubscribe = text_process_result.subscribe((data) => {
		info = data;
	});

	onDestroy(unsubscribe);

	function clearInfo() {
		text_process_result.set({});
	}
</script>

{#if Object.keys(info).length}
	<div class="card w-144 bg-base-100 shadow-xl" transition:fade>
		<div class="card-body items-center text-center">
			<h2 class="card-title">Результат обработки</h2>
			<p>
				<strong>Соответствует клиническим рекомендациям</strong>: {info.is_corresponding
					? 'Да'
					: 'Нет'}<br />
				<strong>Температура</strong>: {info.temperature ? info.temperature : '-'}<br />
				<strong>Систолическое давление</strong>: {info.systole_pressure
					? info.systole_pressure
					: '-'}<br />
				<strong>Диастолическое давление</strong>: {info.diastole_pressure
					? info.diastole_pressure
					: '-'}<br />
			</p>
			<div class="card-actions justify-end">
				<button class="btn btn-circle" on:click={clearInfo}>
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
	</div>
{/if}
