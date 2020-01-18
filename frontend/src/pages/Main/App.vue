<template>
  <div id="app">
    <img alt="Vue logo" src="@/assets/logo.png" />
    <h1>List of animals</h1>
    <p v-for="(animal, index) in animals" :key="index">{{ animal }}</p>
    <button type="button" @click="getAnimals">Get Animals</button>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import HelloWorld from "@/components/HelloWorld.vue";

@Component({
  components: {
    HelloWorld
  },
  data: function() {
    return {
      animals: []
    };
  },
  methods: {
    async getAnimals() {
      const response = await this.$http.get("/api/animals/");
      (this as any).animals = response.data.data;
    }
  }
})
export default class App extends Vue {}
</script>

<style lang="scss">
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
