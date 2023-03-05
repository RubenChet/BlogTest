<template>
	<div v-if="selectedPost">
		<h2>Modifier le post "{{ selectedPost.title }}"</h2>
		<label for="title">Titre :</label>
		<input id="title" v-model="selectedPost.title" />
		<label for="body">Corps :</label>
		<textarea id="body" v-model="selectedPost.body"></textarea>
		<button @click="updatePost">Enregistrer</button>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				selectedPost: null,
			}
		},
		beforeMount() {
			const postId = this.$route.params.post_id
			this.getPostDetails(postId)
		},
		methods: {
			getPostDetails(postId) {
				fetch(`http://localhost:5000/detail/${postId}`)
					.then((response) => response.json())
					.then((data) => {
						this.selectedPost = data.post
						console.log(this.selectedPost)
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
					body: JSON.stringify(data),
					headers: {
						"Content-Type": "application/json",
					},
				})
					.then((response) => response.json())
					.then((data) => {
						if (data.status === "success") {
							// rediriger vers la page d'accueil
							this.$router.push('/')
						} else {
							// afficher une erreur
						}
					})
			},
		},
	}
</script>
