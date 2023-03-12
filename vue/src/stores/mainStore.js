import { defineStore } from "pinia"

export const useMainStore = defineStore("MainStore", {
	state: () => ({
		got_deleted: null,
		is_authenticated: false,
		username: null,
	}),
})
