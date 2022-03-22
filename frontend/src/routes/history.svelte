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
	let d = [];
	getHistory().then((data) => {
		console.log(data);
		d = data;
	});
</script>

<table class="table-auto bg-cyan-100">
	<thead class="border-2 border-orange-300">
		<tr>
			<th>#</th>
			<th>Text</th>
			<th>Temperatute</th>
			<th>OK</th>
		</tr>
	</thead>
	<tbody>
		{#each d as run, i}
			<tr class="border-2 border-orange-300">
				<td>{i + 1}</td>
				<td>{run.text}</td>
				<td>{run.temperature ? run.temperature : "-"}</td>
				<td>{run.is_corresponding ? "✅" : "❌"}</td>
			</tr>
		{/each}
	</tbody>
</table>
