<template lang="">
	<div class="bg-white flex flex-col rounded-xl border border-gray-100 shadow-2xl sm:p-6 lg:p-8" @click="$router.push('/post/' + post.post_id)">
		<span class="flex items-center justify-between">
			<h3 class="-mt-2 text-lg font-bold text-gray-900 sm:text-xl">{{ post.title }}</h3>
			<span class="-mt-2 rounded-full bg-green-100 px-3 py-1.5 text-xs font-medium text-green-600"> new </span>
		</span>
		<p class="mt-4 hidden text-sm sm:block">{{ post.body }}</p>
		<div class="flex justify-between mt-3 items-center">
			<span class="flex flex-col">
				<p>
					Posted By : <span class="font-bold">{{ post.username }}</span>
				</p>
				<p>
					On : <span class="font-bold">{{ formattedDate }}</span>
				</p>
			</span>
			<span class="space-x-2 text-xs" v-if="store.is_authenticated && store.username == post.username">
				<Button label="Edit" severity="info" rounded @click.stop="$router.push('/update/' + post.post_id)" />
				<Button label="Delete" severity="danger" rounded @click.stop="deletePost()" />
			</span>
		</div>
	</div>
</template>
<script setup>
	import { ref, onMounted } from "vue"
	import { useMainStore } from "../stores/mainStore";

	const props = defineProps({
		post: {
			type: Object,
			required: true,
		},
	})

	const store = useMainStore();
	const formattedDate = ref("")

	onMounted(() => {
		const date = new Date(Date.parse(props.post.created))
		const day = date.getDate()
		const month = date.getMonth() + 1
		const year = date.getFullYear()
		formattedDate.value = `${day < 10 ? "0" + day : day}-${month < 10 ? "0" + month : month}-${year}`
	})

	const deletePost = () => {
		fetch(`http://localhost:5000/delete/${props.post.post_id}`, {
			method: "DELETE",
			credentials: "include",
		})
			.then((response) => response.json())
			.then((data) => {
				if (data.message !== "Post has been deleted") {
					console.log(data)
				} else {
					// Remove the deleted post from the `posts` array.
					store.got_deleted = props.post.post_id
				}
			})
			.catch((error) => {
				console.log(error)
			})
	}
</script>
<style lang=""></style>
