<template>
    <form @submit.prevent="Register">
      <div class="imgcontainer">
        <img src="img_avatar2.png" alt="Avatar" class="avatar" />
      </div>
  
      <div class="container">
        <label for="username"><b>Username</b></label>
        <input type="text" placeholder="Enter Username" v-model="username" name="username" required />
  
        <label for="password"><b>Password</b></label>
        <input type="password" placeholder="Enter Password" v-model="password" name="password" required />
  
        <button type="submit">Register</button>
        <label> <input type="checkbox" checked="checked" name="remember" /> Remember me </label>
      </div>
    </form>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: "",
        password: "",
      };
    },
    methods: {
      Register() {
        fetch("http://localhost:5000/auth/register", {
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
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((data) => {
            // handle successful Register
            console.log(data);
          })
          .catch((error) => {
            // handle error
            console.error("There was a problem with the Register:", error);
          });
      },
    },
  };
  </script>
  
  <style>
  /* styles for form */
  </style>
  