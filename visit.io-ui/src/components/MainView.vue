<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-row
      align="center"
      justify="center"
    >
      <v-col
        cols="12"
        sm="8"
        md="6"
        lg="4"
      >
          <MainTab/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MainTab from '@/components/MainTab'

export default {
  name: 'MainView',
  components: {
    MainTab
  }
}
</script>
