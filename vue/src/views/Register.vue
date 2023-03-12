<template lang="">
	<div class="w-[35%] mx-auto mt-10">
		<a class="bg-white flex justify-center rounded-xl border border-gray-100 p-4 shadow-2xl sm:p-6 lg:p-8">
			<main aria-label="Main" class="flex items-center justify-center px-8 py-8 sm:px-12 lg:col-span-7 lg:py-12 lg:px-16 xl:col-span-6">
				<div class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
					<div class="w-[80vh] max-w-md space-y-8">
						<div>
							<img class="mx-auto h-12 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company" />
							<h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">Create an account</h2>
						</div>
						<form @submit.prevent="register" class="mt-8 space-y-6">
							<div class="-space-y-px rounded-md shadow-sm">
								<div>
									<input
										id="username"
										name="username"
										type="text"
										v-model="username"
										autocomplete="username"
										required
										class="relative block w-full rounded-t-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
										placeholder="Username"
									/>
								</div>
								<div>
									<input
										id="password"
										name="password"
										v-model="password"
										type="password"
										autocomplete="current-password"
										required
										class="relative block w-full rounded-b-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
										placeholder="Password"
									/>
								</div>
							</div>

							<div class="flex items-center justify-center text-base space-x-2">
								<p>Already have an account ?</p>
								<a @click="$router.push('/login')" class="font-medium text-indigo-600 hover:text-indigo-500 underline">Login</a>
							</div>

							<div>
								<button
									class="group relative flex w-full justify-center rounded-md bg-indigo-600 py-2 px-3 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
								>
									Register
								</button>
							</div>
						</form>
					</div>
				</div>
			</main>
		</a>
	</div>
</template>
<script setup>
	import { ref } from "vue"
	import { useRouter } from "vue-router"
	import { useMainStore } from "../stores/mainStore"

	const router = useRouter()
	const store = useMainStore()

	const username = ref("")
	const password = ref("")

	const login = () => {
		fetch("http://localhost:5000/auth/login", {
			method: "POST",
			credentials: "include",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				username: username.value,
				password: password.value,
			}),
		})
			.then((response) => {
				if (!response.ok) {
					throw new Error("Network response was not ok")
				}
				return response.json()
			})
			.then((data) => {
				// handle successful login
				console.log(data)
				if (data.status === "success") {
					router.push("/")
				}
			})
			.catch((error) => {
				// handle error
				console.error("There was a problem with the login:", error)
			})
	}

	const register = () => {
		fetch("http://localhost:5000/auth/register", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				username: username.value,
				password: password.value,
			}),
		})
			.then((response) => {
				if (!response.ok) {
					throw new Error("Network response was not ok")
				}
				return response.json()
			})
			.then((data) => {
				// handle successful Register
				console.log(data)
				if (data.status === "success") {
					login()
				}
			})
			.catch((error) => {
				// handle error
				console.error("There was a problem with the Register:", error)
			})
	}
</script>

<style lang=""></style>
