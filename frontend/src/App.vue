<template>
  <div id="app">
    <div id="nav">
      <router-link :to="{ name: 'Home' }">Home</router-link>
      |
      <router-link :to="{ name: 'About' }">About</router-link>
    </div>
    <router-view />
  </div>
</template>

<style lang="scss" src="./assets/styles/global.scss"></style>
<style lang="scss">
  #nav {
    padding: 30px;
  }
</style>
