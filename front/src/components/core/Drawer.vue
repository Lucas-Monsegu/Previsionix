<template>
    <div>

        <v-btn
            fab
            dark
            :color="color"
            @click="shouldShow = !shouldShow"
            v-show="!shouldShow"
            style='position: fixed; z-index: 10'
        >
            <v-icon dark>mdi-menu</v-icon>
        </v-btn>

        <v-navigation-drawer
            id="app-drawer"
            app
            dark
            v-model="shouldShow"
            :temporary="isMobile"
            :permanent="!isMobile"
            width="260"
        >
            <v-img
                :src="require('../../assets/asterix_bg.jpg')"
                height="100%"
                gradient="rgba(25,32,72,.7), rgba(100,115,201,.33)"
            >

                <v-layout
                    class="fill-height"
                    tag="v-list"
                    column
                >

                    <v-list-tile class="py-3">

                        <v-img
                            :src="require('../../assets/asterix_sized2.png')"
                            height="80"
                            width="80"
                            @click="$router.push('/')"
                        />

                        <v-list-tile-content>
                            <v-list-tile-title>
                                <span class="title">Previsionix</span>
                            </v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-divider />

                    <v-list-tile
                        v-for="(link, i) in links"
                        :key="i"
                        :to="link.to"
                        :active-class=" color"
                        class="v-list-item"
                    >
                        <v-list-tile-action class="test">
                            <v-icon color="white">{{ link.icon }}</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content class='test'>
                            <v-list-tile-title>{{ link.text }}</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </v-layout>
            </v-img>
        </v-navigation-drawer>
    </div>
</template>

<script>
// Utilities

export default {
    data: () => ({
        isMobile: false,
        shouldShow: false,
        logo: '../../assets/asterix_sized2.png',
        links: [
            {
                to: '/',
                icon: 'mdi-calendar-today',
                text: 'Aujourd\'hui'
            },
            {
                to: '/statistics',
                icon: 'mdi-chart-line',
                text: 'Statistiques'
            },
            {
                to: '/data',
                icon: 'mdi-calendar-range',
                text: 'Historique'
            },
            {
                to: '/prevision',
                icon: 'mdi-microscope',
                text: 'Prevision'
            }

        ],
        responsive: false
    }),
    computed: {
        color () {
            return 'light-blue darken-1'
        },
        image () {
            return 'static/asterix_bg.jpg'
        },
        items () {
            return this.$t('Layout.View.items')
        }
    },
    mounted () {
        this.onResize()
        window.addEventListener('resize', this.onResize, { passive: true })
    },
    beforeDestroy () {
        if (typeof window !== 'undefined') {
            window.removeEventListener('resize', this.onResize, { passive: true })
        }
    },
    methods: {
        onResize () {
            this.isMobile = window.innerWidth < 800
        }
    }
}
</script>
<style scoped>
.bottom-gradient {
    background-image: linear-gradient(
        to top,
        rgba(0, 0, 0, 0.4) 0%,
        transparent 72px
    );
}

.repeating-gradient {
    background-image: repeating-linear-gradient(
        -45deg,
        rgba(255, 0, 0, 0.25),
        rgba(255, 0, 0, 0.25) 5px,
        rgba(0, 0, 255, 0.25) 5px,
        rgba(0, 0, 255, 0.25) 10px
    );
}
</style>
<style >
#app-mobile .v-list__tile {
	padding-left: 8px;
}
 #app-drawer .v-list__tile {
	border-radius: 10px;
	padding-left: 0px;
	margin-top: 10px;
	margin-right: 10px;
	margin-left: 10px;
}
 #app-drawer .test {
	padding-left: 28px;
}
 #app-drawer .mob {
	padding-left: 10px;
	background-color: blue;
}
 #app-drawer .v-image__image--contain {
	top: 9px;
	height: 60%;
}
</style>
