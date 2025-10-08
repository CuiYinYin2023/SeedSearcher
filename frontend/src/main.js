import { createApp } from 'vue'
import 'normalize.css'
import './style/main.css'
import 'element-plus/dist/index.css'
import router from './router'
import App from './App.vue'

const app = createApp(App)
app.use(router)
app.mount('#app')
