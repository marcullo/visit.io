<template>
  <v-card>
    <v-layout justify-center>
      <v-col class="d-flex" sm="6" md="4" xs="4">
        <v-select
          :items="cities"
          label="Miasto"
          outlined
          @change="onCityUpdated"
        ></v-select>
      </v-col>
      <v-card flat class="d-flex">
        <v-card-text class="font-italic font-weight-light">
          Rynek, Kilka uliczek – Oto całe miasto. Wszędzie jest bardzo blisko… Dosłownie dwa kroki. ~Groński
        </v-card-text>
      </v-card>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  name: 'CityPicker',
  data: () => ({
    cities: ['Warszawa', 'Kraków', 'Wrocław', 'Gdańsk']
  }),
  methods: {
    onCityUpdated (city) {
      this.$emit('onCityUpdated', city)
    }
  }
}
</script>
