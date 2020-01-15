<template>
  <v-container fluid>
    <VueCtkDateTimePicker
      v-model="model"
      :label="label"
      no-header
      button-now-translation="Teraz"
      format="YYYY-MM-DD HH:mm"
      formatted="YYYY-MM-DD HH:mm"
    ></VueCtkDateTimePicker>
  </v-container>
</template>

<script>
export default {
  name: 'DateTimePicker',
  props: [
    'label',
    'label-now'
  ],
  data: () => ({
    model: null
  })
}
</script>
