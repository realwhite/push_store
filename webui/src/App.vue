<template>
  <v-app id="inspire">
    <!-- <v-app-bar app color="indigo" dark>
      <v-toolbar-title>Application</v-toolbar-title>
    </v-app-bar> -->
    <v-content>
      <v-container fluid>
        <v-row class="justify-center">
          <v-simple-table fixed-header width="400px">
            <template v-slot:default>
              <thead>
                <tr>
                  <td colspan="5">
                    <v-btn block color="indigo" dark @click.stop="show_form(true)">Add new metric</v-btn>
                  </td>
                </tr>
                <tr>
                  <th class="text-center">Title</th>
                  <th class="text-center">UUID</th>
                  <th class="text-center">Events</th>
                  <th class="text-center">Last event</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <metric-item
                  v-for="item in items" :item=item :key="item.name" 
                  @toggle="toggle"
                  @truncate="truncate"
                  @delete_metric="delete_metric"
                />
              </tbody>
            </template>
          </v-simple-table>
        </v-row>
      </v-container>
    </v-content>

    <metric-form :show="dialog" @close="show_form(false)" @save="create_metric"/>

    <v-snackbar top v-model="snackbar" :timeout="snackbar_timeout" :color="snackbar_color">
      {{ snackbar_text }}
      <v-btn color="blue" text @click="snackbar = false">
        Close
      </v-btn>
    </v-snackbar>

    <v-footer color="indigo" app >
      <span class="white--text">&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>
  import MetricItem from "./components/MetricItem"
  import MetricForm from "./components/MetricForm"

    export default {
      components: {
        MetricItem,
        MetricForm
      },
    data: () => ({
      dialog: false,
      snackbar: false,
      snackbar_color: 'info',
      snackbar_timeout: 3000,
      snackbar_text: '',
      items: [],
    }),
    methods: {
      show_message: function (text, color='info') {
        this.snackbar_text = text
        this.snackbar_color = color
        this.snackbar = true
      },
      pretty_errors: function(err) {
        let text = ''
        for (let k in err) {
          text += k.toUpperCase() + ': ' + err[k] + '\n'
        }
        return text
      },
      api_fetch: function(endpoint, options) {
        return new Promise((resolve, reject) =>  {
          fetch( window.location.protocol+ '//'+ window.location.host +'/'+ endpoint, options)
          .then(response => response.json())
          .then(data => {
            if (!data.success){
              reject(data.errors)
            }
            else {
              resolve(data.data)
            }
          })
        })
      },
      toggle: function(uuid) {
        this.api_fetch('metric/' + uuid + '/toggle', {method: 'POST'})
        .then((data) => {
          let metric_data = data.metric
          this.items = this.items.map((item) => {
            if (item.uuid == uuid){
              return metric_data
            }
            return item
          })
          this.show_message(metric_data.uuid + ' now has status: ' + metric_data.status) // TODO: вынести в константы
        })
        .catch(err => {
          this.show_message(this.pretty_errors(err), 'error')
        })
      },
      truncate: function(uuid) {
        this.api_fetch('metric/' + uuid + '/truncate', {method: 'POST'})
        .then(() => {
          this.show_message('Truncated')
        })
        .catch(err => {
          this.show_message(this.pretty_errors(err), 'error')
        })
      },
      delete_metric: function(uuid) {
        this.api_fetch('metric/' + uuid, {method: 'DELETE'})
        .then(() => {
          this.items = this.items.filter(i => i.uuid != uuid)
          this.show_message('DELETED')
        })
        .catch(err => {
          this.show_message(this.pretty_errors(err), 'error')
        })
      },
      create_metric (params) {
        this.api_fetch('metrics', {method: 'POST', body: JSON.stringify(params)})
        .then((data) => {
          this.items.push(data['metric'])
          this.show_message('Created')
          this.show_form(false)
        })
        .catch(err => {
          this.show_message(this.pretty_errors(err), 'error')
        })
      },
      show_form: function(is_show) {
        this.dialog = is_show
      }

    },
    mounted: function () {
      this.api_fetch('metrics', {})
      .then(data => {
        this.items = data.metrics
      })
    }
  }
</script>