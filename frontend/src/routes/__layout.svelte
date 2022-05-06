<script>
	import Nav from '../components/nav.svelte';
	import Footer from '../components/footer.svelte';
</script>

<svelte:head>
	<title>Qwork</title>
</svelte:head>

<body class="flex flex-col min-h-screen">
	<!-- HEADER -->
	<header>
		<Nav />
	</header>

	<!-- MAIN -->
	<slot />

	<!-- FOOTER -->
	<Footer />
</body>

<style>
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>
