import { createRouter, createWebHistory } from 'vue-router';
import AuthView from "../views/AuthView.vue";
import MapView from "../views/MapView.vue";
import UsersView from "../views/UsersView.vue";

const routes = [
    {
        path: '/',
        name: 'AuthRedirect',
        redirect: '/auth'
    },
    {
        path: '/map',
        name: 'Map',
        component: MapView
    },
    {
        path: '/auth',
        name: 'Auth',
        component: AuthView
    },
    {
        path: '/users',
        name: 'Users',
        component: UsersView
    }
];

const router = createRouter({
    history: createWebHistory('/'),
    routes
});

export default router;
