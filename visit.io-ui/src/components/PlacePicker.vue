<template>
  <v-card>
    <v-autocomplete
      v-model="select"
      :loading="loading"
      :items="items"
      :search-input.sync="search"
      cache-items
      outlined
      dense
      hide-no-data
      hide-details
      :label="label"
    ></v-autocomplete>
  </v-card>
</template>

<script>
import params from '../../../params/example.json'

export default {
  name: 'PlacePicker',
  props: [
    'label'
  ],
  data: () => ({
    loading: false,
    items: [],
    search: null,
    select: null,
    places: [
      params.available.from.place
    ]
  }),
  watch: {
    search (val) {
      val && val !== this.select && this.querySelections(val)
    }
  },
  methods: {
    querySelections (v) {
      this.loading = true
      // Simulated ajax query
      setTimeout(() => {
        this.items = this.places.filter(e => {
          return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1
        })
        this.loading = false
      }, 500)
    }
  }
}
</script>
