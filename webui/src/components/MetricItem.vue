<template>
    <tr>
        <td>{{ item.title }}</td>
        <td>{{ item.uuid }}</td>
        <td>{{ item.events_count }}</td>
        <td>{{ pretty_timestamp }}</td>
        <td>
        <!-- <v-btn small class="ma-2"><v-icon left>mdi-pencil</v-icon> Edit</v-btn> -->
        <v-btn small class="ma-2" @click="$emit('toggle', item.uuid)" :color="item.status === 1 ? '': 'indigo'">
            {{status_change_map[item.status]}}
        </v-btn>
        <v-btn small class="ma-2" @click="$emit('truncate', item.uuid)">Truncate</v-btn>
        <v-btn class="ma-2" text small color="error" @click="$emit('delete_metric', item.uuid)" :disabled="item.status !=2">
            Drop
        </v-btn>
        </td>
    </tr>
</template>
<script>
export default {
    name: 'metric-item',
    props: {
      item: Object
    },
    data: () => ({
        status_change_map: {
            1: 'Pause',
            2: 'Active'
        },
        status_map: {
            1: 'Active',
            2: 'Paused'
        }
    }),
    computed: {
        pretty_timestamp: function () {
            return this.item.last_event === null ? 'never' : new Date(this.item.last_event * 1000).toLocaleString()
      }, 
    }
    
}
</script>