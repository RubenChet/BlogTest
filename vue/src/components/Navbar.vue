<template>
	<Menubar :model="items">
		<template #start>
			<div class="flex items-center ml-5">
				<img alt="logo" src="../assets/glorious.svg" height="40" class="mr-2" />
				<nav class="ml-12 space-x-4">
					<RouterLink to="/">Accueil</RouterLink>
					<RouterLink to="/create">Créer un post</RouterLink>
				</nav>
			</div>
		</template>
		<template #end>
			<div v-if="store.is_authenticated" class="text-sm space-x-4 mr-20 flex items-center">
				<h1>Hello {{ store.username }}</h1>
				<Button label="Logout" severity="secondary" raised @click="logout()" />
			</div>
			<div v-else class="text-sm space-x-4 mr-20">
				<Button label="Login" severity="info" raised @click="$router.push('/login')" />
				<Button label="Register" severity="secondary" raised @click="$router.push('/register')" />
			</div>
		</template>
	</Menubar>
</template>
<script setup>
	import { ref } from "vue"
	import { useRouter } from "vue-router"
	import { useMainStore } from "../stores/mainStore"

	const router = useRouter()
	const store = useMainStore()

	const items = ref([])

	function logout() {
		fetch("http://localhost:5000/auth/logout", {
			method: "POST",
			credentials: "include",
		})
			.then((response) => {
				if (!response.ok) {
					throw new Error("Network response was not ok")
				}
				return response.json()
			})
			.then((data) => {
				console.log(data)
				if (data.status === "success") {
					store.is_authenticated = false
				}
			})
			.catch((error) => {
				// handle error
				console.error("There was a problem with the logout:", error)
			})
	}
</script>

<style scoped>
	/* Votre style ici */
</style>
