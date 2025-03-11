import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/index/IndexPage.vue') }],
  },
  {
    path: '/twitter',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/twitter/search/twitterSearchPage.vue') }],
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
