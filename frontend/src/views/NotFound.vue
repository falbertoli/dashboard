<template>
  <div class="not-found">
    <h1>404 - Page Not Found</h1>
    <p>Oops! The page you're looking for doesn't exist.</p>
    <router-link to="/">Go Back to Dashboard</router-link>
  </div>
</template>

<style scoped>
.not-found {
  text-align: center;
  margin-top: 50px;
}

.not-found h1 {
  font-size: 2rem;
  color: red;
}

.not-found p {
  font-size: 1.2rem;
}

.not-found a {
  display: inline-block;
  margin-top: 15px;
  text-decoration: none;
  color: blue;
  font-weight: bold;
}
</style>
