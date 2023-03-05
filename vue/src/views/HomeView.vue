<template>
  <div>
    <h1>My Blog</h1>
    <div v-for="post in posts" :key="post.id" class="border">
      <router-link :to="{ name: 'post', params: { post_id: post.post_id }}">{{ post.title }}</router-link>
      <p>{{ post.body }}</p>
      <p>Posted by {{ post.username }} on {{ post.created }}</p>
      <button @click="deletePost(post.post_id)">Delete</button>
      <router-link :to="{ name: 'update', params: { post_id: post.post_id }}">Edit</router-link>
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
    this.fetchPosts();
  },
  methods: {
    fetchPosts() {
      fetch('http://localhost:5000/')
        .then(response => response.json())
        .then(data => {
          this.posts = data.posts;
        })
        .catch(error => {
          console.log(error);
        });
    },
    deletePost(post_id) {
      fetch(`http://localhost:5000/delete/${post_id}`, {
        method: 'DELETE',
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          // Remove the deleted post from the `posts` array.
          this.posts = this.posts.filter(post => post.post_id !== post_id);
        })
        .catch(error => {
          console.log(error);
        });
    },
  },
};
</script>
