<template>
	<div>
		<div v-if="selectedPost">
			<h2>{{ selectedPost.title }}</h2>
		</div>
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
					})
			},
		},
	}
</script>
