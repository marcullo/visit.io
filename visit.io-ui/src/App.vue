<template>
  <v-app>
    <Navbar/>
    <MainView/>
  </v-app>
</template>

<script>
import MainView from '@/components/MainView'
import Navbar from '@/components/Navbar'

export default {
  name: 'App',
  components: {
    Navbar,
    MainView
  },
  data: () => ({})
};
</script>
