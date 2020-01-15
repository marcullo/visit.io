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
        md="4"
      >
        <v-card class="elevation-12">
          <v-toolbar
            color="primary"
            dark
            flat
          >
            <v-toolbar-title>Dodaj punkt do odwiedzenia</v-toolbar-title>
            <v-spacer />
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  :href="source"
                  icon
                  large
                  target="_blank"
                  v-on="on"
                >
                  <v-icon>mdi-code-tags</v-icon>
                </v-btn>
              </template>
              <span>Source</span>
            </v-tooltip>
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-btn
                  icon
                  large
                  href="https://codepen.io/johnjleider/pen/pMvGQO"
                  target="_blank"
                  v-on="on"
                >
                  <v-icon>mdi-codepen</v-icon>
                </v-btn>
              </template>
              <span>Codepen</span>
            </v-tooltip>
          </v-toolbar>
          <v-card-text>
            <v-form>
              <v-text-field
                label="Miasto"
                name="city"
                type="text"
              />

              <v-text-field
                id="timeInPlaceId"
                label="Czas pobytu (w minutach)"
                name="timeInPlace"
                type="text"
              />
              </v-form>
            </v-card-text>
            <v-card-actions>
            <v-spacer />
            <v-btn color="primary">Dodaj</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import format from 'date-fns/format'

export default {
  props: {
    source: String,
  },
  data() {
    return {
      due: null,
      menu: false
    }
  },

  methods: {
    submit() {
      if(this.$refs.form.validate()) {
       // console.log(this.title, this.content)
      }
    }
  },

  computed: {
    formattedDate () {
      //console.log(this.due)
      return this.due ? format(this.due, 'Do MMM YYYY') : ''
    }
  }
}
</script>
