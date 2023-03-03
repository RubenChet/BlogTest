<template>
	<div>
		<h1>Create a new post</h1>
		<form @submit.prevent="submitForm">
			<div>
				<label for="title">Title</label>
				<input type="text" id="title" v-model="title" />
			</div>
			<div>
				<label for="body">Body</label>
				<textarea id="body" v-model="body"></textarea>
			</div>
			<button type="submit">Submit</button>
		</form>
	</div>
</template>

<script>
	import VueCookies from 'vue-cookies'
	export default {
	  data() {
	    return {
	      title: '',
	      body: '',
	    };
	  },
	  methods: {
	    submitForm() {
	      fetch('http://localhost:5000/create', {
	        method: 'POST',
	        headers: {
							"Content-Type": "application/json",
						},
						body: JSON.stringify({
							title: this.title,
							body: this.body,
							cookie: VueCookies.get('user_id'),
						}),
	      })
	        .then(response => response.json())
	        .then(data => {
	          if (data.success) {
	            alert(data.message);
	            this.title = '';
	            this.body = '';
	          } else {
	            alert(data.message);
	          }
	        })
	        .catch(error => {
	          console.log(error);
	        });
	    },
	  },
	};
</script>
