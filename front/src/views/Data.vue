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
                <div class="display-3 text-xs-center">Historique
                </div>
            </v-flex>
            <v-flex
                shrink
                xs6
            >
                <v-card
                    color="white"
                    dark
                >
                    <v-text-field
                        outline
                        label="Chercher"
                        light
                        color="light-blue darken-1"
                        class='px-3 pt-3'
                        hide-details
                        @input="changeFilter"
                    />
                    <v-list
                        light
                        style="max-height:300px"
                        class="scroll-y"
                    >
                        <v-list-tile
                            v-for="item in filteredList"
                            :key="item"
                            :class="item == selectedAttraction ? 'tile' : ''"
                            @click="selectedAttraction=item"
                        >

                            <v-list-tile-content color="blue">
                                <v-list-tile-title v-text="item" />
                            </v-list-tile-content>

                        </v-list-tile>
                    </v-list>
                </v-card>
            </v-flex>
            <v-flex
                shrink
                xs6
            >
                <v-date-picker
                    v-model="picker"
                    type="month"
                    color="orange darken-2"
                    header-color="light-blue darken-1"
                    width="100%"
                    :max="new Date().toISOString().substr(0, 7)"
                    min="2019-04-01T10:22:48+0000"
                    locale='fr'
                />
            </v-flex>
            <v-flex xs12>
                <v-sheet height="500">
                    <v-calendar
                        ref="calendar"
                        :value="selectedMonth"
                        color="primary"
                        locale='fr'
                    >
                        <template v-slot:day="{ present, past, date }">
                            <v-layout fill-height>
                                <template v-if="(past || present) && tracked[date]">
                                    <v-sheet
                                        :color="getColorCalendar(tracked[date])"
                                        :width="`${tracked[date] * 100/60}%`"
                                        height="100%"
                                        tile
                                    >
                                        <div
                                            class="text-xs-center"
                                            style="color: white; padding-left: 7px; padding-top:17px"
                                        >{{ tracked[date] }}</div>
                                    </v-sheet>
                                </template>
                            </v-layout>
                        </template>
                    </v-calendar>
                </v-sheet>
            </v-flex>
        </v-layout>
    </v-container>
</template>
<script>
import axios from 'axios'
export default {
    data () {
        return {
            picker: new Date().toISOString().substr(0, 7),
            selectedMonth: '2019-01-01',
            tracked: {
            },
            colors: ['green', 'blue', 'red'],
            attractions: ['Attention Menhir', 'Discobelix', 'Epi de mais Croisiere', 'Goudurix', "L'Hydre de Lerne",
                "L'Oxygenarium", 'La Galere', 'La Trace du Hourra', 'Le Cheval de Troie', 'Le Defi de Cesar',
                "Le Vol d'Icare", 'Les Chaises Volantes', 'Les Chaudrons', 'Les Espions de Cesar', 'Menhir Express',
                'OzIris', 'Pegase Express', 'Romus et Rapidus', 'SOS Numerobis', 'Tonnerre de Zeus', 'Tous'],
            filteredList: ['Attention Menhir', 'Discobelix', 'Epi de mais Croisiere', 'Goudurix', "L'Hydre de Lerne",
                "L'Oxygenarium", 'La Galere', 'La Trace du Hourra', 'Le Cheval de Troie', 'Le Defi de Cesar',
                "Le Vol d'Icare", 'Les Chaises Volantes', 'Les Chaudrons', 'Les Espions de Cesar', 'Menhir Express',
                'OzIris', 'Pegase Express', 'Romus et Rapidus', 'SOS Numerobis', 'Tonnerre de Zeus', 'Tous'],
            translateTable: {
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
                'Tonnerre de Zeus': 'TonnerredeZeus',
                'Tous': 'all'
            },
            selectedAttraction: 'all',
            filter: ''
        }
    },

    watch: {
        picker (current, prev) {
            this.selectedMonth = current + '-01'

            axios
                .get('/api/month-delay/' + this.translateTable[this.selectedAttraction] + '/' + current)
                .then(response => {
                    this.tracked = response.data
                })
        },
        selectedAttraction (current, prev) {
            axios
                .get('/api/month-delay/' + this.translateTable[current] + '/' + this.picker)
                .then(response => {
                    this.tracked = response.data
                })
        }
    },

    mounted () {
        let current = new Date().toISOString().substr(0, 7)
        this.selectedMonth = current + '-01'

        axios
            .get('/api/month-delay/all/' + current)
            .then(response => {
                this.tracked = response.data
            })
    },
    methods: {
        test: function (t) {
        },
        getColorCalendar: function (t) {
            if (t <= 20) { return 'green' } else if (t <= 30) { return 'orange' } else return 'red'
        },
        updateListAttr: function (s) {
            this.filteredList = this.attractions.filter(word => word.toLowerCase().startsWith(s.toLowerCase()))
        },
        changeFilter: function (s) {
            this.updateListAttr(s)
        }
    }
}
</script>
<style scoped>
.notran {
    transition: none;
}
.tile {
    transition: none;
    color: white;
    background: #f57c00;
}
</style>
