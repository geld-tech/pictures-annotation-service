<template>
  <div class="error">
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  data () {
    return {
      msg: 'Resource not found!'
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.error {
  color: #FF4242;
}
</style>
