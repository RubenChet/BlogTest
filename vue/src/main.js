import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// PrimeVue
import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/lara-light-blue/theme.css'     //theme
import 'primevue/resources/primevue.min.css'                 //core css
import 'primeicons/primeicons.css'                          //icons

// Tailwind CSS
import './style/tailwind.css'


import Menubar from 'primevue/menubar';
import Button from 'primevue/button';

const app = createApp(App)

app.component('Menubar', Menubar);
app.component('Button', Button);


app.use(router)
app.use(PrimeVue)
app.mount('#app')
