<template>
  <v-app-bar
    app
    dark
    class="primary"
  >
    <div class="d-flex align-center">
      <div class="headline font-weight-bold">
        visit.io
      </div>

      <v-divider
        class="mx-4"
        :inset="inset"
        vertical
      ></v-divider>

      <div class="caption font-italic">
        Visit. Explore. Repeat.
      </div>
    </div>

    <v-spacer></v-spacer>

    <v-btn
      href="https://github.com/vuetifyjs/vuetify/releases/latest"
      target="_blank"
      text
    >
      <span class="mr-2">Powered By</span>
      <v-img
        alt="Vuetify Logo"
        class="shrink mr-2"
        contain
        src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-light.png"
        transition="scale-transition"
        width="20"
      />
    </v-btn>

    <v-btn
      href="https://github.com/marcullo/visit.io/releases/latest"
      target="_blank"
      text
    >
      <span class="mr-2">Latest Release</span>
      <v-icon>mdi-github-face</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
    name: 'Navbar'
}
</script>
