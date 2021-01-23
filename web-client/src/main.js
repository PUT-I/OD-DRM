import Vue from 'vue';
import VueRouter from "vue-router";
import App from './App.vue';
import {BootstrapVue, IconsPlugin} from "bootstrap-vue";
import UsersView from "@/components/UsersView";

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

const routes = [
    {path: "/", redirect: "/users/"},
    {path: '/users/', component: UsersView}
];

const router = new VueRouter({
    mode: 'history',
    routes: routes
});

new Vue({
    router: router,
    render: h => h(App),
}).$mount('#app');
