import { createApp } from "vue";
import App from "./App.vue";
import "./assets/style.css";
import router from "./router";
import { createPinia } from "pinia";
import formatters from "./plugins/formatters";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
// import "@fortawesome/fontawesome-free/css/all.min.css";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(formatters); // Add the formatters plugin
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");
