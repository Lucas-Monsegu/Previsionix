<template>
    <v-container
        fill-height
        fluid
        grid-list-xl
    >
        <v-layout
            wrap
            justify-center
        >
            <v-flex xs12>
                <div class="display-3 text-xs-center">Aujourd'hui</div>
            </v-flex>
            <v-flex
                sm6
                xs12
                md6
                lg3
            >
                <material-stats-card
                    :value="averageTime + 'min'"
                    :sub-text="dataDate.date"
                    color="green lighten-1"
                    icon="mdi-clock-outline"
                    title="Temps moyen"
                    sub-icon="mdi-update"
                />
            </v-flex>
            <v-flex
                sm6
                xs12
                md6
                lg3
            >
                <material-stats-card
                    :value="temperature.data+' °C'"
                    :sub-text="temperature.date"
                    color="blue lighten-1"
                    icon="mdi-cloud"
                    title="Temperature"
                    sub-icon="mdi-update"
                />
            </v-flex>
            <v-flex
                sm6
                xs12
                md6
                lg3
            >
                <material-stats-card
                    :value="worthAttr.data"
                    :sub-text="worthAttr.date"
                    color="orange lighten-1"
                    icon="mdi-star"
                    title="La plus rentable"
                    sub-icon="mdi-update"
                />
            </v-flex>
            <v-flex
                shrink
                xs12
                md8
            >
                <component
                    :cdata="datacollection"
                    :options="this.options"
                    :is="'LineChart'"
                    class="my-2"
                    xLabel='heure'
                    yLabel='minute'
                />
            </v-flex>
        </v-layout>
    </v-container>
</template>
<script>
import axios from 'axios'
import LineChart from '../components/charts/LineChart.vue'

export default {
    components: {
        LineChart
    },
    data () {
        return {
            datacollection: {

            },
            loaded: false,
            dataDate: { date: '~~' },

            temperature: {
                data: 0,
                date: '~~'
            },
            worthAttr: {
                date: '~~',
                data: '~~'
            },
            options: {
                scales: {
                    yAxes: [{
                        display: true,
                        ticks: {
                            suggestedMin: 0, // minimum will be 0, unless there is a lower value.
                            suggestedMax: 30
                        }
                    }]
                }
            }
        }
    },
    computed: {
        lastHourDifference () {
            if (this.datacollection.datasets === undefined) {
                return 0
            }
            let tab = this.datacollection['datasets'][0]['data']
            if (tab.length <= 1) { return 0 }
            let dif = tab[tab.length - 1] / tab[tab.length - 2] * 100 - 100
            return Math.round(dif)
        },
        averageTime () {
            if (this.datacollection.datasets === undefined) {
                return 0
            }
            let tab = this.datacollection['datasets'][0]['data']
            if (tab === null || tab.length === 0) { return '~~' }
            let k = Math.round(tab.reduce((a, b) => a + b) / tab.length)
            return k.toString()
        }
    },
    mounted () {
        axios
            .get('/api/todayHourAll')
            .then(response => {
                this.datacollection = {
                    labels: ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],
                    datasets: [
                        {
                            label: 'temps d\'attente moyen',
                            borderColor: '#FFA000',
                            borderWidth: 2,
                            data: [0].concat(response.data.values)
                        }
                    ]
                }
                this.dataDate.date = this.FormatDate(response.data.timestamp)
                this.loaded = true
            })
            .catch(() => (this.games = null))
        axios.get('/api/lastTemperature').then(response => {
            this.temperature.data = response.data['value']

            this.temperature.date = this.FormatDate(response.data['timestamp'])
        })
        axios.get('/api/worthAttraction').then(response => {
            this.worthAttr.data = response.data['value']
            this.worthAttr.date = this.FormatDate(response.data['timestamp'])
        })
    },
    methods: {
        FormatDate: function (time) {
            if (time === '~~') {
                return '~~'
            }
            let date = Math.floor((Date.now() / 1000 - time) / 60)
            if (date === 0) {
                date = 'A l\'instant'
            } else {
                date = 'Mis à jour il y a ' + date.toString() + ' minutes'
            }
            return date
        }

    }
}
</script>
