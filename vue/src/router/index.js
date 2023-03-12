import { createRouter, createWebHistory } from "vue-router"

async function checkifUserOwnsPost(id) {
	try {
		const response = await fetch("http://localhost:5000/check_id_and_user", {
			method: "POST",
			credentials: "include",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				id: id,
			}),
		})

		if (!response.ok) {
			throw new Error("Network response was not ok")
		}

		const data = await response.json()

		return data // or false, depending on the logic you want to implement
	} catch (error) {
		// handle error
		console.error("There was a problem with the login:", error)
		return false // or throw an error, depending on the logic you want to implement
	}
}

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/",
			name: "home",
			component: () => import("../views/Home.vue"),
		},
		{
			path: "/login",
			name: "login",
			component: () => import("../views/Login.vue"),
		},
		{
			path: "/register",
			name: "register",
			component: () => import("../views/Register.vue"),
		},
		{
			path: "/create",
			name: "create",
			component: () => import("../views/Create.vue"),
		},
		{
			path: "/post/:post_id",
			name: "post",
			component: () => import("../views/Post_details.vue"),
		},
		{
			path: "/update/:post_id",
			name: "update",
			component: () => import("../views/Update.vue"),
			beforeEnter: async (to) => {
				const id = to.params.post_id
				const result = await checkifUserOwnsPost(id)
        console.log(result)
				if (result.status != "success") return { name: "not-found" }
			},
		},
		{
			path: "/:pathMatch(.*)*",
			name: "not-found",
			component: () => import("../views/NotFound.vue"),
		},
	],
})

export default router
