<template>
  <v-card>
    <v-toolbar flat color="primary" dark>
      <v-toolbar-title>Zdefiniuj cele podróży</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            color="primary--text"
            large
            fab
            icon
            justify-center
            v-on="on"
          >
            <v-icon>mdi-help</v-icon>
          </v-btn>
        </template>
        <span>Gdy to zrobisz, optymalizator wykona za Ciebie resztę działań</span>
      </v-tooltip>
    </v-toolbar>
    <v-tabs
      horizontal
      fixed-tabs
    >
      <v-tab>
        <v-icon left>mdi-city</v-icon>
        Miasto
      </v-tab>
      <v-tab
        :disabled="disabledBase"
      >
        <v-icon left>mdi-map-marker-radius</v-icon>
        Baza
      </v-tab>
      <v-tab
        :disabled="disabledPlaces"
      >
        <v-icon left>mdi-near-me</v-icon>
        Miejsca
      </v-tab>

      <v-tab-item>
        <CityPicker
          @onCityUpdated="updateCity"
        ></CityPicker>
      </v-tab-item>
      <v-tab-item>
        <v-card>
          <v-list
            class="mx-4"
          >
            <PlacePicker
              label="Punkt startowy"
            ></PlacePicker>
            <DateTimePicker
              label="Czas przyjazdu"
            ></DateTimePicker>

            <PlacePicker
              label="Punkt końcowy"
            ></PlacePicker>
            <DateTimePicker
              label="Czas powrotu"
            ></DateTimePicker>
          </v-list>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-text>
            Ludzie tworzą miejsca, a miejsce tworzy ludzi.

            <p>
              Fusce a quam. Phasellus nec sem in justo pellentesque facilisis. Nam eget dui. Proin viverra, ligula sit amet ultrices semper, ligula arcu tristique sapien, a accumsan nisi mauris ac eros. In dui magna, posuere eget, vestibulum et, tempor auctor, justo.
            </p>

            <p class="mb-0">
              Cras sagittis. Phasellus nec sem in justo pellentesque facilisis. Proin sapien ipsum, porta a, auctor quis, euismod ut, mi. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nam at tortor in tellus interdum sagittis.
            </p>
          </v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs>
  </v-card>
</template>

<script>
import CityPicker from './CityPicker'
import DateTimePicker from './DateTimePicker'
import PlacePicker from './PlacePicker'

export default {
  name: 'MainTab',
  components: {
    CityPicker,
    DateTimePicker,
    PlacePicker
  },
  data: () => ({}),
  methods: {
    updateCity (newCity) {
      this.$store
        .dispatch('updateCity', newCity)
        .then(() => {
          console.log('city updated to ' + this.$store.getters.city)
        })
    }
  },
  computed: {
    disabledBase () {
      return this.$store.getters.city === null
    },
    disabledPlaces () {
      return true
    }
  }
}
</script>
