<template>
  <v-app>
    <Navbar/>
    <MainView/>
  </v-app>
</template>

<script>
import Navbar from '@/components/Navbar'
import MainView from '@/components/MainView'

export default {
  name: 'App',
  components: {
    Navbar,
    MainView
  },
  data: () => ({})
}
</script>
