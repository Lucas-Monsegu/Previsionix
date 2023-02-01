// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
// Components
import './components'

// Plugins
import './plugins'

// Application imports
import App from './App'
import router from '@/router'
import '@mdi/font/css/materialdesignicons.css'

Vue.config.productionTip = false
Vue.use(Vuetify)
/* eslint-disable no-new */
new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
