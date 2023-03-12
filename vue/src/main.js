import { createApp } from 'vue'
import { createPinia } from 'pinia'
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
import Dialog from 'primevue/dialog'
import Card from 'primevue/card';
import Textarea from 'primevue/textarea';
import InputText from 'primevue/inputtext';

const pinia = createPinia()
const app = createApp(App)

app.component('Menubar', Menubar);
app.component('Button', Button);
app.component('Dialog', Dialog);
app.component('Card', Card);
app.component('Textarea', Textarea);
app.component('InputText', InputText);

app.use(router)
app.use(PrimeVue)
app.use(pinia)
app.mount('#app')
