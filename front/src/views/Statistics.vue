<template>
    <v-container
        fill-height
        fluid
        grid-list-xl
    >
        <v-layout
            row
            wrap
            justify-center
        >
            <v-flex xs12>
                <div class="display-3 text-xs-center">Statistiques
                </div>
            </v-flex>
            <v-flex
                shrink
                xs6
            >

                <v-select
                    :items="attractions"
                    v-model="selectedAttraction"
                    label="Attraction"
                ></v-select>
            </v-flex>
            <v-flex
                shrink
                xs12
            >
                <v-tabs
                    fixed-tabs
                    show-arrows
                    @change="displayGraph"
                    slider-color="orange"
                >
                    <v-tab
                        v-for="n in allCategories"
                        :key="n"
                    >
                        {{n}}
                    </v-tab>
                </v-tabs>
                <component
                    :cdata="pointsChart.datacollection"
                    :options="pointsChart.options"
                    :is="pointsChart.type == 'Scatter' ? 'ScatterChart' : 'LineChart'"
                    class="my-2"
                />

            </v-flex>

        </v-layout>
    </v-container>
</template>
<script>
import axios from 'axios'
import ScatterChart from '../components/charts/ScatterChart.vue'
import LineChart from '../components/charts/MultipleLine.vue'

export default {
    components: {
        ScatterChart,
        LineChart
    },
    data () {
        return {
            pointsChart: {
                datacollection: {
                    labels: ['9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],
                    data: {}
                },
                options: {
                    scales: {
                        yAxes: [{
                            display: true,
                            ticks: {
                                suggestedMin: 0, // minimum will be 0, unless there is a lower value.
                                suggestedMax: 100,
                                // OR //
                                beginAtZero: true // minimum value will be 0.
                            }
                        }],
                        xAxes: [{
                            display: true,
                            ticks: {
                                suggestedMin: -5,
                                suggestedMax: 45
                            }
                        }]
                    },
                    responsive: true,
                    maintainAspectRatio: false
                },
                type: 'Scatter'

            },

            attractions: ['Tous', 'Attention Menhir', 'Discobelix', 'Epi de mais Croisiere', 'Goudurix', "L'Hydre de Lerne",
                "L'Oxygenarium", 'La Galere', 'La Trace du Hourra', 'Le Cheval de Troie', 'Le Defi de Cesar',
                "Le Vol d'Icare", 'Les Chaises Volantes', 'Les Chaudrons', 'Les Espions de Cesar', 'Menhir Express',
                'OzIris', 'Pegase Express', 'Romus et Rapidus', 'SOS Numerobis', 'Tonnerre de Zeus'],
            filteredList: ['Tous', 'Attention Menhir', 'Discobelix', 'Epi de mais Croisiere', 'Goudurix', "L'Hydre de Lerne",
                "L'Oxygenarium", 'La Galere', 'La Trace du Hourra', 'Le Cheval de Troie', 'Le Defi de Cesar',
                "Le Vol d'Icare", 'Les Chaises Volantes', 'Les Chaudrons', 'Les Espions de Cesar', 'Menhir Express',
                'OzIris', 'Pegase Express', 'Romus et Rapidus', 'SOS Numerobis', 'Tonnerre de Zeus'],
            translateTable: {
                'Tous': 'all',
                'Attention Menhir': 'AttentionMenhir',
                'Discobelix': 'Discobelix',
                'Epi de mais Croisiere': 'EpidemaisCroisiere',
                'Goudurix': 'Goudurix',
                "L'Hydre de Lerne": 'LHydredeLerne',
                "L'Oxygenarium": 'LOxygenarium',
                'La Galere': 'LaGalere',
                'La Trace du Hourra': 'LaTraceduHourra',
                'Le Cheval de Troie': 'LeChevaldeTroie',
                'Le Defi de Cesar': 'LeDefideCesar',
                "Le Vol d'Icare": 'LeVoldIcare',
                'Les Chaises Volantes': 'LesChaisesVolantes',
                'Les Chaudrons': 'LesChaudrons',
                'Les Espions de Cesar': 'LesEspionsdeCesar',
                'Menhir Express': 'MenhirExpress',
                'OzIris': 'OzIris',
                'Pegase Express': 'PegaseExpress',
                'Romus et Rapidus': 'RomusetRapidus',
                'SOS Numerobis': 'SOSNumerobis',
                'Tonnerre de Zeus': 'TonnerredeZeus'
            },
            allCategories: ['Temperature', 'Humidité', 'Vitesse du Vent', 'Jours', 'Mois', 'Année'],
            selectedAttraction: 'Tous',
            filter: '',
            buttonSelected: '.',
            selectedTab: 0,
            allInfos: {},
            attractionInfo: {}
        }
    },
    watch: {
        selectedAttraction (current, prev) {
            axios
                .get('/api/all-daily-delays/' + this.translateTable[current])
                .then(response => {
                    this.attractionInfo = response.data
                    this.displayGraph(this.selectedTab)
                })
        }

    },
    mounted () {
        this.displayGraph(this.selectedTab)
        axios
            .get('/api/all-daily-infos')
            .then(response => {
                this.allInfos = response.data
            })
        axios
            .get('/api/all-daily-delays/' + this.translateTable[this.selectedAttraction])
            .then(response => {
                this.attractionInfo = response.data
                this.displayGraph(this.selectedTab)
            })
    },
    methods: {
        test: function (t) {
        },
        updateListAttr: function (s) {
            this.filteredList = this.attractions.filter(word => word.toLowerCase().startsWith(s.toLowerCase()))
        },
        changeFilter: function (s) {
            this.updateListAttr(s)
        },
        displayGraph: function (index) {
            let buttonSelected = this.allCategories[index].normalize('NFD').replace(/[\u0300-\u036f]/g, '')
            this.selectedTab = index
            let numb = 0
            if (buttonSelected === 'Temperature') {
                numb = 0
                this.setOptionsScatter(-5, 45, 0, 60, '°C')
            } else if (buttonSelected === 'Humidite') {
                numb = 1
                this.setOptionsScatter(0, 100, 0, 60, ' %')
            } else if (buttonSelected === 'Vitesse du Vent') {
                numb = 2
                this.setOptionsScatter(0, 20, 0, 60, ' m/s')
            } else if (buttonSelected === 'Jours') {
                this.week()
                return
            } else if (buttonSelected === 'Mois') {
                this.month()
                return
            } else if (buttonSelected === 'Annee') {
                this.year()
                return
            } else {
                return
            }
            let res = []
            let all = this.allInfos
            let attraction = this.attractionInfo
            if (attraction === 'all') {
                Object.values(all).forEach((val) => {
                    res.push({ x: val[numb], y: val[3] })
                })
            } else {
                Object.keys(attraction).forEach((key) => {
                    if (key in all) {
                        res.push({ x: all[key][numb], y: attraction[key] })
                    }
                })
            }
            this.pointsChart.datacollection = {
                labels: ['10', '11', '12', '13', '14', '15', '16', '17', '18'],
                datasets: [
                    {
                        label: 'Temps d\'attente moyen',
                        backgroundColor: '#FFA000AA',
                        data: res
                    }
                ]
            }
        },
        week () {
            let res = []
            for (let i = 0; i < 7; ++i) {
                res.push([])
            }
            Object.keys(this.attractionInfo).forEach((key) => {
                let weekday = new Date(key).getDay() - 1
                if (weekday < 0) { weekday = 6 }
                res[weekday].push(this.attractionInfo[key])
            })
            let bars = [[], [], []]
            for (let i = 0; i < res.length; ++i) {
                if (res[i].length === 0) {
                    for (let i = 0; i < 3; ++i) {
                        bars[i].push(0)
                    }
                    continue
                }
                bars[0].push(Math.min(...res[i]))
                bars[1].push((res[i].reduce((a, b) => a + b) / res[i].length))
                bars[2].push(Math.max(...res[i]))
            }
            this.pointsChart.type = 'Line'
            this.pointsChart.datacollection = {
                labels: ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
                datasets: [
                    {
                        label: 'Minimum recorded',
                        fill: false,
                        borderColor: '#42A5F5AA',
                        backgroundColor: '#42A5F5AA',
                        data: bars[0]
                    },
                    {
                        label: 'All time average',
                        borderColor: '#FFA000AA',
                        backgroundColor: '#FFA000AA',
                        fill: false,
                        data: bars[1]
                    }, {
                        label: 'Maximum recorded',
                        borderColor: '#EF6C00AA',
                        backgroundColor: '#EF6C00AA',
                        fill: false,
                        data: bars[2]
                    }
                ]
            }
        },
        month () {
            let res = []
            for (let i = 0; i < 12; ++i) {
                res.push([])
            }

            Object.keys(this.attractionInfo).forEach((key) => {
                let month = new Date(key).getMonth()
                res[month].push(this.attractionInfo[key])
            })
            let bars = [[], [], []]
            for (let i = 0; i < res.length; ++i) {
                if (res[i].length === 0) {
                    for (let i = 0; i < 3; ++i) {
                        res[i].push(null)
                    }
                    continue
                }
                bars[0].push(Math.min(...res[i]))
                bars[1].push(res[i].reduce((a, b) => a + b) / res[i].length)
                bars[2].push(Math.max(...res[i]))
            }

            this.pointsChart.type = 'Line'
            this.pointsChart.datacollection = {
                labels: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Octobre', 'Novembre', 'Décembre'],
                datasets: [
                    {
                        label: 'Minimum recorded',
                        fill: false,
                        borderColor: '#42A5F5AA',
                        data: bars[0]
                    },
                    {
                        label: 'All time average',
                        borderColor: '#FFA000AA',
                        fill: false,
                        data: bars[1]
                    }, {
                        label: 'Maximum recorded',
                        borderColor: '#EF6C00AA',
                        fill: false,
                        data: bars[2]
                    }
                ]
            }
        },
        year () {
            let res = []
            let labels = []
            let yearMin = Math.min(...Object.keys(this.attractionInfo).map(key => { return new Date(key).getFullYear() }))
            let yearMax = Math.max(...Object.keys(this.attractionInfo).map(key => { return new Date(key).getFullYear() }))
            for (let i = yearMin; i <= yearMax; ++i) {
                res.push([])
                labels.push(i.toString())
            }
            Object.keys(this.attractionInfo).forEach((key) => {
                let year = new Date(key).getFullYear()
                res[year - yearMin].push(this.attractionInfo[key])
            })
            let bars = [[], [], []]
            for (let i = 0; i < res.length; ++i) {
                if (res[i].length === 0) {
                    for (let i = 0; i < 3; ++i) {
                        res[i].push(null)
                    }
                    continue
                }
                bars[0].push(Math.min(...res[i]))
                bars[1].push(res[i].reduce((a, b) => a + b) / res[i].length)
                bars[2].push(Math.max(...res[i]))
            }

            this.pointsChart.type = 'Line'
            this.pointsChart.datacollection = {
                labels: labels,
                datasets: [
                    {
                        label: 'Minimum recorded',
                        fill: false,
                        borderColor: '#42A5F5AA',
                        data: bars[0]
                    },
                    {
                        label: 'All time average',
                        borderColor: '#FFA000AA',
                        fill: false,
                        data: bars[1]
                    }, {
                        label: 'Maximum recorded',
                        borderColor: '#EF6C00AA',
                        fill: false,
                        data: bars[2]
                    }
                ]
            }
        },
        setOptionsScatter (Xlow, Xhigh, Ylow, Yhigh, Xunit = '') {
            let options = {
                scales: {
                    yAxes: [{
                        display: true,
                        ticks: {
                            suggestedMin: Ylow, // minimum will be 0, unless there is a lower value.
                            suggestedMax: Yhigh,
                            // OR //
                            beginAtZero: true, // minimum value will be 0.
                            callback: function (value, index, values) {
                                return value + ' m'
                            }

                        }
                    }],
                    xAxes: [{
                        display: true,
                        ticks: {
                            suggestedMin: Xlow,
                            suggestedMax: Xhigh,
                            callback: function (value, index, values) {
                                return value + Xunit
                            }
                        }
                    }]
                },
                responsive: true,
                maintainAspectRatio: false
            }
            this.pointsChart.type = 'Scatter'
            this.pointsChart.options = options
        },
        setOptionBar (labels) {
        }
    }
}
</script>
<style scoped>
.tile {
    background: orange;
}
</style>
