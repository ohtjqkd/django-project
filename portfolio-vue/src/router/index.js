import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/components/views/Login'
import Home from '@/components/views/Home'

Vue.use(VueRouter)
const routes = [
    { path: '/', name: 'Main', component: Home},
    { path: '/login', name: 'Login', component: Login}
]

export default new VueRouter({
    mode:'history',
    routes
})