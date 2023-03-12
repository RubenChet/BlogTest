<template>
	<div class="w-[80%] mx-auto flex flex-wrap justify-between">
		<div v-for="post in posts" :key="post.post_id" class="w-[30%] mt-14">
			<PostVue :post="post" />
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted, watch } from "vue"
	import { useMainStore } from "../stores/mainStore"
	import PostVue from "../components/Post.vue"

	const store = useMainStore()

	const posts = ref([])

	onMounted(() => {
		fetch("http://localhost:5000/", {
			credentials: "include",
		})
			.then((response) => response.json())
			.then((data) => {
				posts.value = data.posts
			})
			.catch((error) => {
				console.log(error)
			})
		fetch("http://localhost:5000/is_logged_in", {
			credentials: "include",
		})
			.then((response) => response.json())
			.then((data) => {
				if (data.status === "success") {
					store.is_authenticated = true
					store.username = data.username
				} else {
					store.is_authenticated = false
				}
			})
	})
	watch(() => store.got_deleted, (newValue) => {
      // Faire quelque chose ici quand la valeur de got_deleted change
	  posts.value = posts.value.filter(post => post.post_id !== newValue)
    })
</script>
