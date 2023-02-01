<template>
    <v-menu
        :close-on-content-click="false"
        bottom
        left
        min-width="300"
        max-width="300"
        nudge-left="12"
        offset-x
        transition="slide-y-transition"
    />
</template>

<script>
// Utilities

export default {
    data: () => ({
        colors: [
            'primary',
            'info',
            'success',
            'warning',
            'danger'
        ],
        images: [
            'https://sf.viepratique.fr/wp-content/uploads/sites/4/2014/05/Asterix_on_the_Rock.jpg',
            'https://www.parisinfo.com/var/otcp/sites/images/node_43/node_51/node_77884/node_77888/parc-ast%C3%A9rix-oziris-attraction-%7C-630x405-%7C-%C2%A9-parc-ast%C3%A9rix/19021369-1-fre-FR/Parc-Ast%C3%A9rix-Oziris-Attraction-%7C-630x405-%7C-%C2%A9-Parc-Ast%C3%A9rix.jpg',
            'https://france3-regions.francetvinfo.fr/hauts-de-france/sites/regions_france3/files/styles/top_big/public/assets/images/2017/03/28/maxnewsworldtwo142268-2972829.jpg?itok=Yp_LKBqM',
            'https://demos.creative-tim.com/vue-material-dashboard/img/sidebar-3.3a54f533.jpg',
            'https://demos.creative-tim.com/vue-material-dashboard/img/sidebar-4.3b7e38ed.jpg'
        ]
    }),

    computed: {
        color () {
            return this.$store.state.app.color
        }
    },

    methods: {
        setColor (color) {
            this.$store.state.app.color = color
        }
    }
}
</script>

<style >
.v-avatar, .v-responsive {
	cursor: pointer;
}
 
</style>
