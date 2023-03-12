<template>
	<a class="bg-white flex flex-col rounded-2xl border border-gray-100 shadow-2xl sm:p-6 lg:p-8 w-[40%] mx-auto mt-20 just">
		<h1 class="mx-auto text-3xl">{{selectedPost.title}}</h1>
		<div class="mx-auto mt-6">
			<p>{{selectedPost.body}}</p>
		</div>
		<div class="flex justify-end mt-4">
			<Button label="Back" severity="secondary" size="small" @click="$router.push('/')" />
		</div>
	</a>
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
				fetch(`http://localhost:5000/detail/${postId}`, { credentials: "include" })
					.then((response) => response.json())
					.then((data) => {
						this.selectedPost = data.post
						console.log(data.is_author)
					})
			},
		},
	}
</script>
