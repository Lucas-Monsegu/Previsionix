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
                <div class="display-3 text-xs-center">Prevision
                </div>
            </v-flex>
            <v-flex xs12>

            </v-flex>
            <v-flex
                shrink
                xs12
                md8
            >
                <BarChart
                    :cdata="test"
                    :options="options"
                    class="my-2"
                />
            </v-flex>
            <v-flex
                shrink
                xs12
                md8
            >
                <v-card
                    class="mx-auto"
                    max-width="800"
                >
                    <div class="d-flex flex-no-wrap justify-space-between">
                        <div>
                            <v-card-title class="headline">Infos</v-card-title>

                            <v-card-text>
                                <div>
                                    Nous ne savons pas si le parc est fermé ou non, donc même si une prévision est affiché le parc peut être fermé.
                                </div>
                                <div>
                                    Ces prévisions sont le résultat d'un algorithme de machine learning. Cet algorithme a étudié les précédentes données comme le jour, le mois, la température, etc. afin de trouver des relations et de pouvoir prédire le temps d'attente moyen des prochains jours.
                                </div>
                            </v-card-text>
                        </div>

                    </div>
                </v-card>
            </v-flex>
        </v-layout>

    </v-container>
</template>

<script>
import BarChart from '../components/charts/BarChart'
import axios from 'axios'

export default {
    components: {
        BarChart,
    },
    mounted () {
        let t = {
            labels: ['', '', '', '', '', '', ''],
            datasets: [{
                backgroundColor: [],
                data: []
            }
            ]
        }
        axios.get('/api/prediction')
            .then(response => {
                let i = 0
                let d = new Date()
                for (let tab of response.data) {
                    d.setDate(d.getDate() + 1)
                    let day = d.getDate().toString().padStart(2, '0')
                    let month = (d.getMonth() + 1).toString().padStart(2, '0')
                    t.labels[i] = this.tableDay[tab[1]] + ` ${day}/${month}`
                    t.datasets[0].data.push(tab[0])
                    t.datasets[0].backgroundColor.push(tab[0] <= 15 ? '#66BB6A' : tab[0] < 20 ? '#FFA726' : '#EF5350')
                    i += 1
                }
                this.test = t
            })
    },
    data () {
        return {
            tableDay: {
                0: 'Lundi',
                1: 'Mardi',
                2: 'Mercredi',
                3: 'Jeudi',
                4: 'Vendredi',
                5: 'Samedi',
                6: 'Dimanche'

            },
            test: {
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            callback: function (value) {
                                return value + ' m'
                            }
                        },
                        gridLines: {
                            display: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Temps d\'attente moyen'
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            beginAtZero: true
                        },
                        gridLines: {
                            display: false
                        }
                    }]
                },
                legend: {
                    display: false
                },
                responsive: true,
                maintainAspectRatio: false
            }
        }
    }
}
</script>
