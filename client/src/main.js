import Vue from 'vue';
// import 'bootstrap';
// import 'bootstrap/dist/css/bootstrap.min.css';
import 'vue-slider-component/theme/default.css'
import fontawesome from '@fortawesome/fontawesome';
import solid from '@fortawesome/fontawesome-free-solid';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import store from './store';
import router from './router';
import App from './App.vue';
import VueSocketIO from 'vue-socket.io';
import panZoom from 'vue-panzoom'

global.$ = $;
let WS_URL = '';
if (process.env.NODE_ENV === 'production') {
  WS_URL = 'https://chatbot8.zkm.de';
} else if (process.env.NODE_ENV === 'development') {
  WS_URL = 'http://localhost:5005';
} else {
  WS_URL = 'http://localhost:5005';
}
Vue.use(
  new VueSocketIO({
    debug: true,
    connection: WS_URL,
    vuex: {
      store,
      actionPrefix: 'SOCKET_',
      mutationPrefix: 'SOCKET_',
    },
     options: { origins: 'http://localhost:5005' },
  })
);

Vue.use(panZoom, {componentName: 'yourPanZoom'})

fontawesome.library.add(solid);
Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
