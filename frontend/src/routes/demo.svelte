<script>
	// import { onMount, onDestroy } from 'svelte';

	import { text_process_result } from '../stores.js';

	import TextInfo from '../components/textInfo.svelte';

	import FoundMissingFeatures from '../components/found_missing_features.svelte'
import { missing_component } from 'svelte/internal';

	const api_url = import.meta.env.VITE_API_URL;

	const EXAMPLE_TEXT = 'Температура 37.9. Давление высокое - 120 на 80.';
	const EXAMPLE_TEXT2 =
		'Осмотр на фоне приема беталок зок 25 мг 1 р вечер  , панангин форте 1 /2 т, лозап + 1/2 т вечер, антикоагулянты не принимает  Состояние удовлетворительное.  Тоны сердца ослаблены , аритмичные, акцент 2 тона над легочной артерией. АД   120/70        мм рт ст ЧСС   75 в мин В легких дыхание везикулярное. Живот  при пальпации мягкий , безболезненный. Стул и диурез за ночь до 3 литров , со слов пациентки . Отеки нет  ЭКГ 21.12.17 - ритм фибрилляция предсердий с чсс 57-112   в  мин . Признаки НБПНПГ , ЭКГ 29.12.17 - ритм фибрилляция предсердий с чсс 70-120   в  мин . Признаки НБПНПГ ,  в БАК от 10.11.17 - мочевина 9,8 , креатинин ?,калий ?  в ОАК 10.11.17 анемия легкой степени ( эр 3,6 , Hb-115 г/л   ХМ ЭКГ 27.12.17 - ритм фибрилляция предсердий с чсс днем 57-89-39в мин , ночь -57-78-121 в мин . Зар-но 1297 ж.э. 3 эпизода Ж,Т от 3-до 15 комплексов . Макс RR- 2773 мсек( без отрицательной динамики в сравнении с ХМ ЭКГ от 2012 г';
	const EXAMPLE_TEXT3 =
		'Состояние удовлетворительное.  РОСТ= 174см,   ВЕС=100 кг,  ИМТ=33,03.  Ожирение 1  ст.  Тоны сердца  приглушены  аритмичные, мерцательная аритмия  с  ЧСС=86   уд/мин.  АД= 127/103  мм.рт.ст.  В легких дыхание везикулярное,хрипов нет.  Живот   увеличен в обьеме  за счет п/к жирового слоя.  Отеков нет.  По ЭКГ фибрилляция предсердий с ЧСС=62-74уд. мин. Диффузные изменения миокарда.  Хс=   нет данных.  ХМ ЭКГ и заключение их НИИПК прилагаются.';
	const TEXT_EXAMPLES = [EXAMPLE_TEXT, EXAMPLE_TEXT2, EXAMPLE_TEXT3];
	const EXAMPLES_LEN = TEXT_EXAMPLES.length;

	const TEXT_TYPE_DEAFULT = 'Тип заболевания';

	const PROCESS_TYPES = {
		'Острый коронарный синдром': 'acute_coronary_syndrome',
		'Фибрилляция и трепетание предсердий': 'atrial_fibrilation_and_flutter',
		'Универсальная обработка': 'all'
	};

	const _get_process_types_names = function () {
		let result = [];
		for (const [key, value] of Object.entries(PROCESS_TYPES)) {
			console.log(key);
			result.push(key);
		}
		return result;
	};

	// User input bindings
	let user_input = '';
	let text_type_option = TEXT_TYPE_DEAFULT;
	let is_loading = false;

	let is_active_error = false; // TODO: move to __layout as alert component with store usage
	let error_message = '';

	let result_;

	function clearError() {
		error_message = '';
		is_active_error = false;
	}

	function setExampleText() {
		let index = Math.floor(Math.random() * EXAMPLES_LEN);
		user_input = TEXT_EXAMPLES[index];
	}

	const processTextInstant = async () => {
		if (user_input === '') {
			error_message = 'Текст для обработки не может быть пустым';
			is_active_error = true;
			return;
		}

		if (text_type_option === TEXT_TYPE_DEAFULT || text_type_option === '') {
			error_message = 'Выберите тип заболевания';
			is_active_error = true;
			return;
		}
		is_loading = true;
		const url = api_url + 'process_text_instant';
		const res = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				text: user_input,
				type: PROCESS_TYPES[text_type_option]
			})
		});
		const data = await res.json();
		console.log(data);
		result_ = data;
		is_loading = false;
	};

	const processText = async () => {
		if (user_input === '') {
			error_message = 'Текст для обработки не может быть пустым';
			is_active_error = true;
			return;
		}

		if (text_type_option === TEXT_TYPE_DEAFULT || text_type_option === '') {
			error_message = 'Выберите тип заболевания';
			is_active_error = true;
			return;
		}

		is_loading = true;
		const url = api_url + 'process_text';
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

		let requests_count = 0;
		let response_status_code = 0;
		let run_data = {};
		do {
			await new Promise((r) => setTimeout(r, 500));
			const run_info_url = api_url + 'run/' + data.run_id;
			const result = await fetch(run_info_url, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json'
				}
			});
			response_status_code = result.status;
			// console.log(requests_count, response_status_code)
			const fetched_run_data = await result.json();
			// console.log(fetched_run_data);
			run_data = fetched_run_data;
			requests_count++;
		} while (response_status_code != 200 && requests_count < 10);

		console.log(run_data);
		text_process_result.set(run_data);
		is_loading = false;
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
					{#each Object.entries(PROCESS_TYPES) as [key, value]}
						<option>{key}</option>
					{/each}
				</select>
			</div>
		</div>
		<div class="textwrapper mx-2">
			<textarea
				class="textarea textarea-primary my-2"
				bind:value={user_input}
				placeholder={EXAMPLE_TEXT}
				cols="80"
				rows="5"
			/>
		</div>
		<br />
		<button class="btn btn-accent w-64 rounded-full" on:click={setExampleText}
			>Вставить пример текста</button
		>
		{#if is_loading}
			<button class="btn loading my-2">Обрабатываем</button>
		{:else}
			<button class="btn btn-secondary w-64 rounded-full my-2" on:click={processTextInstant}
				>Обработать и проверить</button
			>
		{/if}

		<TextInfo />

		<!-- New Green Red Results -->
		{#if result_}
			<FoundMissingFeatures found_features={result_.found_features} missing_features={result_.missing_features} />
		{/if}
	</div>
</main>

<style>
	textarea {
		width: 100%;
	}
	.textwrapper {
		border: 1px solid #999999;
		margin: 5px 0;
		padding: 3px;
	}
</style>
