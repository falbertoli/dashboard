import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../views/DashboardView.vue";
import HydrogenView from "../views/HydrogenView.vue";
import TurnaroundTimeAnalysisView from "../views/TurnaroundTimeAnalysisView.vue";
import SustainabilityView from "../views/SustainabilityView.vue";
import StorageView from "../views/StorageView.vue";
import RegulationsView from "../views/RegulationsView.vue";
import NotFound from "../views/NotFound.vue";

const routes = [
  { path: "/", component: DashboardView },
  { path: "/hydrogen", component: HydrogenView },
  { path: "/economy", component: TurnaroundTimeAnalysisView },
  { path: "/sustainability", component: SustainabilityView },
  { path: "/storage", component: StorageView },
  { path: "/regulations", component: RegulationsView },
  { path: "/:pathMatch(.*)*", component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
