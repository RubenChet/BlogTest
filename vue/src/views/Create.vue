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
          body: new FormData(event.target),
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
  