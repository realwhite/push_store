<template>
    <v-dialog v-model="show" persistent width="800px">
      <v-card>
        <v-card-title class="grey darken-2">
        Create new metric
        </v-card-title>
        <v-container>
          <v-row class="mx-2">
            <v-col class="align-center justify-space-between" cols="12">
              <v-row align="center" class="mr-0" >
                <v-text-field placeholder="Title" v-model="form.title"></v-text-field>
              </v-row>
              <v-row align="center" class="mr-0" >
                <v-text-field placeholder="UUID" v-model="form.uuid"></v-text-field>
              </v-row>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="$emit('close')" >Cancel</v-btn>
          <v-btn text @click="$emit('save', form)" :disabled="!allow_to_save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: 'metric-form',
    props: {
        show: Boolean
    },
    data: () => ({
        form: {
            title: '',
            uuid: ''
        },
    }),
    computed: {
        allow_to_save () {
            return this.form.title.length > 3 && this.form.uuid.length > 3
        }
    }
}
</script>