import { createApp } from 'vue'
import App from './App.vue'
import '../src/assets/tailwind.css'
import VueApexCharts from "vue3-apexcharts";
import { createVuetify } from "vuetify";
import 'vuetify/styles';
import router from './router';

const vuetify= createVuetify();

createApp(App)
    .use(VueApexCharts)
    .use(vuetify)
    .use(router)
    .mount('#app');
