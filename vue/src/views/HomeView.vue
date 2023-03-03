<template>
  <div>
    <h1>My Blog</h1>
    <div v-for="post in posts" :key="post.id" class="border">
      <h2>{{ post.title }}</h2>
      <p>{{ post.body }}</p>
      <p>Posted by {{ post.username }} on {{ post.created }}</p>
    </div>
  </div>
</template>
  
<script>
export default {
  data() {
    return {
      posts: [],
    };
  },
  mounted() {
    fetch('http://localhost:5000/')
      .then(response => response.json())
      .then(data => {
        this.posts = data.posts;
      })
      .catch(error => {
        console.log(error);
      });
  },
};
</script>
