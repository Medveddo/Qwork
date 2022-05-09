<script>
	const backend_host = import.meta.env.VITE_API_URL
	const getHistory = async function () {
		const url = backend_host + `history`;
		const res = await fetch(url);
		const data = await res.json();
		const history = data.map((run, i) => {
			return {
				text: run.text,
				is_corresponding: run.is_corresponding,
				temperature: run.temperature,
				systole_pressure: run.systole_pressure,
				diastole_pressure: run.diastole_pressure
			};
		});
		return history;
	};
	let runs = [];
	getHistory().then((data) => {
		console.log(data);
		runs = data;
	});
</script>

<div class="overflow-x-auto">
	<table class="table w-full">
		<thead>
			<tr>
				<th></th>
				<th>Текст</th>
				<th>Температура</th>
				<th>Давление</th>
				<th>Соответствует</th>
			</tr>
		</thead>
		<tbody>
			{#each runs as run, i}
			<tr>
				<td>{i + 1}</td>
				<td>{run.text}</td>
				<td>{run.temperature ? run.temperature : "-"}</td>
				<td>
					{run.systole_pressure ? run.systole_pressure : "-"}/{run.diastole_pressure ? run.diastole_pressure : "-"}
				</td>
				<td>{run.is_corresponding ? "✅" : "❌"}</td>
			</tr>
			{/each}
		</tbody>
	</table>
</div>
		

