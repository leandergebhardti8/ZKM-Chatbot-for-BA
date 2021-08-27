<template>
  <div
    class="main-menu-overlay"
    :class="mainMenuOpen ? 'menu-shown' : 'menu-hidden'"
  >
    <div class="nav-wrapper">
      <!--div
				class="nav-element"
				@click="
					sendTriggerToBot({ text: 'Neustart', payload: 'Starte Beratung'})
				"
		>
				<p class="menu-item">Neustart</p>
			</div-->
      <div
        class="nav-element"
        @click="
          sendTriggerToBot({
            text: 'Ich habe eine Frage',
            payload: 'Hallo',
          })
        "
      >
        <p class="menu-item">Ich habe eine Frage</p>
      </div>
      <p class="menu-title">SERVICEFRAGEN</p>
      <hr>
      <div
        class="nav-element"
        @click="
          sendTriggerToBot({
            text: 'Öffnungszeiten',
            payload: 'Öffnungszeiten',
          })
        "
      >
        <p class="menu-item">Öffnungszeiten</p>
      </div>
      <div
        class="nav-element"
        @click="
          sendTriggerToBot({
            text: 'Corona Informationen',
            payload: 'Corona',
          })
        "
      >
        <p class="menu-item">Corona Informationen</p>
      </div>
      <div
        class="nav-element"
        @click="
          sendTriggerToBot({
            text: 'Aktuelles Programm',
            payload: 'Aktuelles Programm',
          })
        "
      >
        <p class="menu-item">Aktuelles Programm</p>
      </div>
      <div
        class="nav-element"
        @click="
          sendTriggerToBot({
            text: 'Führung buchen',
            payload: 'Führung buchen',
          })
        "
      >
        <p class="menu-item">Führung buchen</p>
      </div>
      <p class="menu-title">AUSSTELLUNGS-GUIDE</p>
      <hr>
        <SwiperWrapper       
        :items= ausstellungen
        :menu= true
        @clicked="switchToGuideMenu"
        v-if="!showGuideMenu"
      />
      <!-- <div
        class="nav-element"
        @click="
          sendTriggerToBot({
            text: 'Rundgang starten',
            payload: 'Starte Tour',
          })
        "
      >
        <p class="menu-item">Rundgang starten</p>
      </div> -->
	  <werk-menu
      v-if="showGuideMenu"
    />
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import MessageHandlerMixin from "../mixins/MessageHandlerMixin";
import SwiperWrapper from "./SwiperWrapper.vue";
import WerkMenu from "./WerkMenu.vue";

export default {
  name: "MainMenu",
  mixins: [MessageHandlerMixin],
  computed: {
    ...mapGetters([
      "mainMenuOpen"
      ]),
  },
  components: {
    WerkMenu,
    SwiperWrapper,
  },
  methods: {
    switchToGuideMenu(value) {
      this.showNav = false;
      this.showGuideMenu = true;
      console.log(value)
    }
  },
  data() {
    return {
      ausstellungen: [{"title":"Writing the History of the Future ","image_url":"https://zkm.de/media/bild/zkm_sammlung.jpg"},{"title":"Critical Zones","image_url":"https://zkm.de/media/bild/zkm_cz-banner_1280x800_1.png"}],
      showNav: true,
      showGuideMenu: false,
      showExtra: false,
    };
  }
};
</script>

<style lang="scss" scoped>
#app .main-menu-overlay {
  padding-top: 55px;
  height: 100%;
  position: absolute;
  width: 100%;
  overflow-y: auto;
  hr{
    color: #70CDB2;
    border: 1px solid #70CDB2;
    border-left: none;
    border-right: none;
    width: 100%;
    margin: 0px 0px 10px 0px;
  }
  .menu-title {
    color: #70CDB2;
    font-size: 18px;
    left: 10px;
    font-weight: 600;
    margin-bottom: 0px;
    margin-top: 20px;
    position: relative;
    margin-right: auto;
  }
  .nav-wrapper {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    // justify-content: center;
    flex-direction: column;
    background: rgba(0, 0, 0, 0.7);
    .nav-element {
      max-width: 200px;
      width: 100%;
      text-align: center;
      margin: 5px 0 5px 0;
      border: solid 1px white;
      border-radius: 0;
      color: white;
      height: 38px;
      display: block;
      box-sizing: border-box;
      .menu-item {
        font-size: 14px;
        line-height: 38px;
        color: white;
        display: inline;
        margin: 0 0 0 0;
        transition: all 0.25s ease;
        cursor: pointer;
        &:hover {
          opacity: 0.5;
        }
      }
    }
  }
}
</style>