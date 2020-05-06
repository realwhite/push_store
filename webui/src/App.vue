<template>
  <v-app id="inspire">
    <v-app-bar app color="indigo" dark>
      <v-toolbar-title>Application</v-toolbar-title>
    </v-app-bar>

    <v-content>
      <v-container fluid>
        <v-row class="justify-center">
          <v-simple-table fixed-header width="400px">
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-center">Name</th>
                  <th class="text-center">type</th>
                  <th class="text-center">last event</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td colspan="4">
                    <v-btn block color="indigo" dark>Add new metric</v-btn>
                  </td>
                </tr>
                <tr v-for="item in items" :key="item.name">
                  <td>{{ item.name }}</td>
                  <td>{{ item.type }}</td>
                  <td>{{ item.last_event }}</td>
                  <td>
                    <v-btn small class="ma-2"><v-icon left>mdi-pencil</v-icon> Edit</v-btn>
                    <v-btn small class="ma-2">Pause</v-btn>
                    <v-btn small class="ma-2" @click="snackbar = true">Truncate</v-btn>
                    <v-btn class="ma-2" tile small color="danger" depressed>
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-row>
      </v-container>
    </v-content>

    <v-snackbar
      v-model="snackbar"
      :timeout="snackbar_timeout"
    >
      {{ snackbar_text }}
      <v-btn
        color="blue"
        text
        @click="show_message('truncated')"
      >
        Close
      </v-btn>
    </v-snackbar>

    <v-footer color="indigo" app >
      <span class="white--text">&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>
  export default {
    props: {
      source: String,
    },

    data: () => ({
      drawer: null,
      snackbar: false,
      snackbar_timeout: 2000,
      snackbar_text: '',
      items: [
        {name: 'testmetric', type: 'int', last_event: '1234567'},
        {name: 'testmetric1', type: 'int', last_event: '1234567'},
        {name: 'testmetric2', type: 'int', last_event: '1234567'},
        {name: 'testmetric3', type: 'int', last_event: '1234567'},
        {name: 'testmetric4', type: 'int', last_event: '1234567'},
      ],
      dropdown_icon: [
        { text: 'truncate data', callback: () => console.log('truncate') },
        { text: 'delete metric', callback: () => console.log('delete') },
      ],
    }),
    methods: {
      show_message: function (text) {
        this.snackbar_text = text
      }
    }
  }
</script>