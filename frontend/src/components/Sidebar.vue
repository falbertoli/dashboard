<template>
  <nav class="sidebar">
    <ul>
      <li><router-link to="/">Dashboard</router-link></li>
      <li><router-link to="/hydrogen">Hydrogen</router-link></li>
      <li><router-link to="/economy">Economy</router-link></li>
      <li><router-link to="/sustainability">Sustainability</router-link></li>
      <li><router-link to="/storage">Storage</router-link></li>
      <li><router-link to="/regulations">Regulations</router-link></li>
    </ul>
  </nav>
</template>

<style scoped>
.sidebar {
  width: 200px;
  background: #2c3e50;
  padding: 15px;
  color: white;
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar li {
  margin: 10px 0;
}

.sidebar a {
  color: white;
  text-decoration: none;
}
</style>
