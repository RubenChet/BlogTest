<template>
	<a class="bg-white flex flex-col rounded-2xl border border-gray-100 shadow-2xl sm:p-6 lg:p-8 w-[40%] mx-auto mt-20 just">
		<h1 class="mx-auto text-3xl">Create a new post</h1>
		<form @submit.prevent="submitForm" class="mt-10 mx-auto">
			<div>
				<span class="p-float-label">
					<InputText id="Title" v-model="selectedPost.title" />
					<label for="Title">Title</label>
				</span>
			</div>
			<div class="mt-8">
				<span class="p-float-label">
					<Textarea v-model="selectedPost.body" rows="5" cols="30" />
					<label>Content</label>
				</span>
			</div>
			<div class="flex space-x-2 justify-end mt-5">
				<Button type="submit" label="Update" severity="info" size="small" @click='updatePost' />
				<Button label="Cancel" severity="secondary" size="small" @click="$router.push('/')" />
			</div>
		</form>
	</a>
</template>

<script>
	export default {
		data() {
			return {
				selectedPost: {
					post_id: null,
					title: "",
					body: "",
					created: "",
					username: "",
				},
				postId: null,
			}
		},
		beforeMount() {
			this.postId = this.$route.params.post_id
			this.getPostDetails()
		},
		methods: {
			getPostDetails() {
				fetch(`http://localhost:5000/detail/${this.postId}`)
					.then((response) => response.json())
					.then((data) => {
						this.selectedPost = data.post
					})
			},
			updatePost() {
				const postId = this.selectedPost.post_id
				const data = {
					title: this.selectedPost.title,
					body: this.selectedPost.body,
				}
				fetch(`http://localhost:5000/update/${postId}`, {
					method: "PUT",
					credentials: "include",
					body: JSON.stringify(data),
					headers: {
						"Content-Type": "application/json",
					},
				})
					.then((response) => response.json())
					.then((data) => {
						if (data.status === "success") {
							// rediriger vers la page d'accueil
							this.$router.push("/")
						} else {
							// afficher une erreur
							console.log(data)
						}
					})
			},
		},
	}
</script>
