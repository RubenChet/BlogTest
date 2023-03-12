<template>
	<a class="bg-white flex flex-col rounded-2xl border border-gray-100 shadow-2xl sm:p-6 lg:p-8 w-[40%] mx-auto mt-20 just">
		<h1 class="mx-auto text-3xl">Create a new post</h1>
		<form @submit.prevent="submitForm" class="mt-10 mx-auto">
			<div>
				<span class="p-float-label">
					<InputText id="Title" v-model="title" />
					<label for="Title">Title</label>
				</span>
			</div>
			<div class="mt-8">
				<span class="p-float-label">
					<Textarea v-model="body" rows="5" cols="30" />
					<label>Content</label>
				</span>
			</div>
			<div class="flex space-x-2 justify-end mt-5 ">
				<Button type="submit" label="Create" severity="info" size="small" />
				<Button label="Cancel" severity="secondary" size="small" @click="$router.push('/')" />
			</div>
		</form>
	</a>
</template>

<script>
	export default {
		data() {
			return {
				title: "",
				body: "",
			}
		},
		methods: {
			submitForm() {
				fetch("http://localhost:5000/create", {
					method: "POST",
					credentials: "include",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						title: this.title,
						body: this.body,
					}),
				})
					.then((response) => response.json())
					.then((data) => {
						if (data) {
							console.log(data)
							this.$router.push("/")
						} else {
							alert(data.message)
						}
					})
					.catch((error) => {
						console.log(error)
					})
			},
		},
	}
</script>
