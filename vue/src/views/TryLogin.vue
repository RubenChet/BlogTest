<template>
	<form @submit.prevent="login">
		<div class="imgcontainer">
			<img src="img_avatar2.png" alt="Avatar" class="avatar" />
		</div>

		<div class="container">
			<label for="username"><b>Username</b></label>
			<input type="text" placeholder="Enter Username" v-model="username" name="username" required />

			<label for="password"><b>Password</b></label>
			<input type="password" placeholder="Enter Password" v-model="password" name="password" required />

			<button type="submit">Login</button>
			<label> <input type="checkbox" checked="checked" name="remember" /> Remember me </label>
		</div>

		<div class="container" style="background-color: #f1f1f1">
			<button type="button" class="cancelbtn">Cancel</button>
			<span class="psw">Forgot <a href="#">password?</a></span>
		</div>
	</form>
</template>

<script>
	export default {
		data() {
			return {
				username: "",
				password: "",
			}
		},
		methods: {
			login() {
				fetch("http://localhost:5000/auth/login", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						username: this.username,
						password: this.password,
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
						document.cookie = `user_id=${data.cookie}`
					})
					.catch((error) => {
						// handle error
						console.error("There was a problem with the login:", error)
					})
			},
		},
	}
</script>

<style>
	/* styles for form */
</style>
