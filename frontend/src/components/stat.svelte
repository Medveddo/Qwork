<script>
	export let stats;
</script>

<div class="stats shadow">
	<div class="stat">
		<div class="stat-figure text-primary">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				class="inline-block w-8 h-8 stroke-current"
				><path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
				/></svg
			>
		</div>
		<div class="stat-title">Обработанно текстов</div>
		<div class="stat-value text-primary">{stats.texts_processed_total}</div>
		<!-- <div class="stat-desc">На 21% больше, чем в предыдущий месяц</div> -->
	</div>

	<div class="stat">
		<div class="stat-figure text-secondary">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				class="inline-block w-8 h-8 stroke-current"
				><path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M13 10V3L4 14h7v7l9-11h-7z"
				/></svg
			>
		</div>
		<div class="stat-title">Процент соответствия рекомендациям</div>
		<div class="stat-value text-secondary">
			{Math.round(stats.corresponding_runs_percent * 100 * 100) / 100}%
		</div>
		<!-- <div class="stat-desc">Больше всего в <strong>Амурской области</strong></div> -->
	</div>
</div>
