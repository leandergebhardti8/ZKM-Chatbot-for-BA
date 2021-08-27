<template>
  <div class="chat">
    <transition name="fade">
      <div id="main-menu" v-if="mainMenuOpen">
        <MainMenu />
      </div>
      <div id="qr-reader" v-if="qrOpen">
        <QRCodeReader />
      </div>
    </transition>
    <div v-show="showSplashScreen" id="splash">
      <SplashScreen />
    </div>
    <TourTitle :class="startTour ? 'tour-container tour-active': 'tour-container'" />
    <Three
  
      class="avatar-container"
      :class="[startTour ? 'avatar-tour': '', showSplashScreen? 'avatar-splash': '']"
    />
    <div class="container-fluid chat-screen full-height">
      <div
        class="row main-chat-wrapper justify-content-center align-items-center"
        :class="[mainMenuOpen || qrOpen ? 'blurred' : '', startTour ? 'tour': '']"
      >
        <!-- <div v-if='backgroundImage'  
				:style="{
					backgroundImage: (backgroundImage ? 'url('+backgroundImage+')': 'none')
				}" 
				class="bg-image"></div>
				<div class='chat-top-overlay-bgImage' v-if="backgroundImage"></div>
        <div class='chat-top-overlay' v-if="!backgroundImage"></div>-->
        <div
          v-show="showBgImage" :style="{
					backgroundImage: (backgroundImage ? 'url('+backgroundImage+')':'undefined'),
					opacity: (backgroundImage ? '1':'0')
				}"
          class="bg-image"
        ></div>

        <div class="chat-top-overlay-bgImage" v-if="backgroundImage"></div>
        <div class="chat-top-overlay" v-if="!backgroundImage"></div>

        <div :class="inputVisible ? 'active' : ''" class="chat-container col-12">
          <div class="content-wrapper">
            <br />
            <br />
            <br />
            <br />
            <div v-for="(mess, index) in allMessages" :key="index" class="wrapper">
             
              <IncomingMessage
                v-if="
									mess.type === 'in' &&
										mess.format === 'message' &&
										(mess.text.length >= 1 &&
											mess.text.replace(/\s/g, '').length !== 0)
								"
                :id="index"
                :message="mess.text"
               
              />

              <WerkIntro 
                v-if="mess.format === 'intro'"
                :intro="mess.intro"
              />
              
              <OutgoingMessage
                v-if="
									mess.type === 'out' &&
										mess.format === 'message' &&
										(mess.text.length >= 1 &&
											mess.text.replace(/\s/g, '').length !== 0)
								"
                :id="index"
                :message="mess.text"
              />

              <ButtonEvent
                v-if="
									mess.format === 'button' ||
										mess.format === 'download_button' ||
										mess.format === 'link_button'
								"
                :buttons="mess.links"
              />
              
              <QuickReplies
                v-if="mess.format === 'quick_replies_answer'"
                :quickReplies="mess.quickReplies"
              />

              <SwiperWrapper 
                v-if="mess.format == 'items'" 
                :items="mess.data" 
              />

              <VideoPlayer 
                v-if="mess.format == 'video'" 
                :videoObject="mess.data" 
                :videoSubtitle="mess.text"
              />

              <ExpandableImage 
                v-if="mess.format == 'img'" 
                :src="mess.data" 
                :subtitle="mess.subtitle" 
              />

              <Modal 
                v-if="mess.format === 'modal'" 
                :modalText="mess.text" 
                :modal="mess.modal"
              />

              <SliderSelector 
                v-if="mess.format === 'slider'" 
                :options="mess.options"
              />

              <SliderSelectorValues 
                v-if="mess.format === 'slider-values'" 
                :marks="mess.marks" 
                :values="mess.slider" 
              />

              <QuoteCard 
                v-if="mess.format === 'quote-card'" 
                :quote="mess.quote" 
              />

              <Lottie v-if="mess.format == 'lottie'"
                :animationData="mess.data"
                class="animation"
                renderer="canvas"
                :loop="true"
                :autoplay="true"
                @getLottieInstance="getLottieInstance"
                @onEnterFrame="onEnterFrame"
                @onComplete="onComplete"
                @onLoopComplete="onLoopComplete"
              />
            
            </div>
            <CompareImages v-if="compare"></CompareImages>
            
             <Timer v-if="timer" :time-left="timeLeft"></Timer>
          <!--div v-if="lottieImage"-->
        <!--/div-->
            <div class="qr-wrapper">
              <QuickReplies
                v-if="currentQuickReply"
                :quickReplies="currentQuickReply.quickReplies"
              />

              <ToggleSwitch
                v-if="
									currentQuickReply &&
										currentQuickReply.formatType &&
										(currentQuickReply.formatType === 'contact_option' ||
											currentQuickReply.formatType === 'rating')
								"
              />
              <ContactForm v-if="showContactForm" />
              <UserInputForm v-if="showInputForm" :initialText="formText" :isGuideContext="isGuideContext" />
              <!--datepicker v-if='dateSelection' v-model="selectedDate" name="datepicker" placeholder="Datum wählen"></datepicker>
              <p>{{selectedDate}}</p-->

              <Feedback v-if="feedbackObject" :feedbackData="feedbackObject" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* Dependencies */
import { mapGetters } from "vuex";
/* Mixins */
import MessageHandlerMixin from "../mixins/MessageHandlerMixin";
/* Components */
import Feedback from "./Feedback";
import IncomingMessage from "./IncomingMessage.vue";
import OutgoingMessage from "./OutGoingMessage.vue";
import QuickReplies from "./QuickReplies.vue";
import ButtonEvent from "./ButtonEvent.vue";
import SplashScreen from "./SplashScreen.vue";
import ContactForm from "./ContactForm.vue";
import ToggleSwitch from "./ToggleSwitch.vue";
import MainMenu from "./MainMenu.vue";
import SwiperWrapper from "./SwiperWrapper";
import TourTitle from "./TourTitle";
import Three from "./Three";
import VideoPlayer from "./VideoPlayer";
import Datepicker from "./DatePicker";
import DateInput from "./DateInput";
import UserInputForm from "./UserInputForm.vue";
import Lottie from 'vue-lottie-web';
// import lottieData from "../assets/Exports/All/All2.json";
import Timer from "./Timer.vue";
import CompareImages from './CompareImages.vue';
import Modal from './Modal.vue';
import ExpandableImage from './ExpandableImage.vue';
import SliderSelector from './SliderSelector.vue';
import SliderSelectorValues from './SliderSelectorValues.vue';
import QuoteCard from './QuoteCard.vue';
import WerkIntro from './WerkIntro.vue';
import QRCodeReader from './QRCodeReader.vue';

export default {
  name: "Chat",
  components: {
    Lottie,
    MainMenu,
    IncomingMessage,
    OutgoingMessage,
    QuickReplies,
    ButtonEvent,
    SplashScreen,
    ContactForm,
    ToggleSwitch,
    SwiperWrapper,
    Three,
    TourTitle,
    Feedback,
    VideoPlayer,
    Datepicker,
    DateInput,
    UserInputForm,
    Timer,
    CompareImages,
    Modal,
    ExpandableImage,
    SliderSelector,
    SliderSelectorValues,
    QuoteCard,
    WerkIntro,
    QRCodeReader,
  },
  mixins: [MessageHandlerMixin],
  computed: {
    ...mapGetters([
      "userId",
      "allMessages",
      "currentInput",
      "inputVisible",
      "typing",
      "currentQuickReply",
      "currentActiveData",
      "showSplashScreen",
      "showContactForm",
      "mainMenuOpen",
      "qrOpen",
      "startTour",
      "items",
      "feedbackObject",
      "backgroundImage",
      "dateSelection",
      "showInputForm",
      "formText",
      "lottieImage",
      "timer",
      "quote",
      "compare",
      "isGuideContext"
    ]),
    timeLeft() {
      return this.timeLimit - this.timePassed;
    }
  },
  data: function() {
    return {
      bgstyle: {
        color: "red",
        fontSize: "13px"
      },
      selectedDate: "",
      lottieInstance: "",
      timeLimit: 60,
      timePassed: 0,
      timerInterval: null
    };
  },
  watch: {
    selectedDate: function(val) {
      this.$store.commit("setCurrentInput", val.toString());
    }
  },
  methods: {
    getLottieInstance(lottieInstance) {
      this.lottieInstance = lottieInstance;
      console.log(lottieInstance);
    },
    onComplete(e) {
      console.log("onComplete", e);
    },
    onLoopComplete(e) {
      // console.log("onLoopComplete", e);
    },
    onEnterFrame(e) {
      // console.log('onEnterFrame', e);
    },
    showBgImage() {
      this.show = !this.show;
    },
    startTimer() {
      this.timerInterval = setInterval(() => (this.timePassed += 1), 1000);
    }
  },
  mounted() {
    this.startTimer();
  }
};
</script>

<style lang="scss">
#app {
  #main-menu {
    height: 100%;
    position: absolute;
    width: 100%;
    z-index: 9;
    &.menu-shown {
      animation: fade-in 1s ease-in-out;
      opacity: 1;
      z-index: 9;
    }
    &.menu-hidden {
      animation: fade-out 1s ease-in-out;
      opacity: 0;
      z-index: -1;
    }
    @keyframes fade-in {
      0% {
        opacity: 0;
        z-index: -1;
      }
      100% {
        opacity: 1;
        z-index: 9;
      }
    }

    @keyframes fade-out {
      0% {
        opacity: 1;
        z-index: 9;
      }
      100% {
        opacity: 0;
        z-index: -1;
      }
    }
  }
  #qr-reader {
    height: 100%;
    position: absolute;
    width: 100%;
    z-index: 9;
    &.qr-shown {
      animation: fade-in 1s ease-in-out;
      opacity: 1;
      z-index: 9;
    }
    &.qr-hidden {
      animation: fade-out 1s ease-in-out;
      opacity: 0;
      z-index: -1;
    }
    @keyframes fade-in {
      0% {
        opacity: 0;
        z-index: -1;
      }
      100% {
        opacity: 1;
        z-index: 9;
      }
    }

    @keyframes fade-out {
      0% {
        opacity: 1;
        z-index: 9;
      }
      100% {
        opacity: 0;
        z-index: -1;
      }
    }
  }
  .chat {
    /* Transition Fade */
    .fade-enter {
      opacity: 0;
    }
    .fade-enter-active {
      transition: opacity 0.7s;
    }
    // .fade-leave {
    // 	/* opacity: 1; */
    // }
    .fade-leave-active {
      transition: opacity 0.7s;
      opacity: 0;
    }
    /* End Transition Fade */
    height: 100%;
    line-height: 1.2em !important;
    #splash {
      height: 100%;
      width: 100%;
    }
    .bg-image {
      position: absolute;
      width: 100%;
      height: 50%;
      top: 0;
      left: 0;
      filter: grayscale(1) brightness(50%);
      opacity: 0;
      transition: opacity 1.5s ease-in;
      background-size: cover;
      z-index: 1;
      pointer-events: none;
      background-position: center center;
    }
    .avatar-container {
      transition: all 1s ease-in-out;
      position: absolute;
      top: 45px;
      left: 0;
      width: 100%;
      height: 170px;
      z-index: 5;
      pointer-events: none;

      @media screen and (device-aspect-ratio: 40/71), (device-aspect-ratio: 375/667), (device-aspect-ratio: 9/16) {
        height: 120px;  
      }

      &.avatar-tour {
        top: 200px;
        height: 300px;
      }
      &.avatar-splash {
        top: 80px;
        height: 300px;
      
        @media screen and (device-aspect-ratio: 40/71), (device-aspect-ratio: 375/667), (device-aspect-ratio: 9/16) {
          top: 80px;
          height: 200px;  
        }
      }
    }

    .avatar-container-proton {
      position: absolute;
      top: 200px;
      left: 0;
      width: 100%;
      height: 200px;
      z-index: 4;
      &.avatar-tour {
        top: 200px;
        left: calc(50% - 150px);
        width: 300px;
        height: 300px;
      }
      &.avatar-splash {
        top: 80px;
        left: calc(50% - 150px);
        width: 300px;
        height: 300px;
      }
    }
    .tour-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 0;
      opacity: 0;
      &.tour-active {
        height: 60%;
        opacity: 1;
      }
    }
    .chat-screen {
      position: relative;
    }
    .background-image {
      width: 100%;
      height: 100%;
      text-align: center;
      position: absolute;
      display: flex;
      align-items: center;
      justify-content: center;
      & > img {
        max-width: 100%;
        opacity: 0.45;
      }
    }
    .chat-top-overlay {
      background: rgb(0, 0, 0);
      background: linear-gradient(
        180deg,
        black 20%,
        rgba(0, 0, 0, 0.9) 70%,
        rgba(0, 0, 0, 0) 100%
      );
      height: 220px;
      width: 100%;
      position: absolute;
      top: 0px;
      left: 0;
      z-index: 4;
      pointer-events: none;

      @media screen and (device-aspect-ratio: 40/71), (device-aspect-ratio: 375/667), (device-aspect-ratio: 9/16) {
        height: 180px;  
      }
    }

    .chat-top-overlay-bgImage {
      background: rgb(0, 0, 0);
      background: linear-gradient(
        0deg,
        black 5%,
        rgba(0, 0, 0, 0.9) 10%,
        rgba(0, 0, 0, 0) 20%
      );
      height: 50%;
      width: 100%;
      position: absolute;
      top: 0;
      left: 0;
      z-index: 2;
    }
    .main-chat-wrapper {
      position: absolute;
      margin-top: 0;
      transition: 1s all ease-in-out;
      bottom: 0;
      height: 100%;
      width: 100%;
      &.tour {
        height: 40%;
      }
      &.blurred {
        filter: blur(4px);
        -webkit-filter: blur(4px);
      }
      .chat-container {
        height: calc(100% - 85px);
        overflow: auto;
        border-radius: 2px;
        -ms-overflow-style: none;
        position: absolute;
        top: 0;
        left: 0;
        z-index: 3;
        .content-wrapper {
          min-height: 100%;
          padding-top: 20px;
          padding-bottom: 0;
          display: flex;
          flex-direction: column;
          justify-content: flex-end;
          .qr-wrapper {
            margin-top: 0;
          }
        }
      }
      .chat-container.active {
        top: 0;
        left: 0;
        position: absolute;
      }
      .chat-container::-webkit-scrollbar {
        width: 0 !important;
      }
    }
  }
}
</style>
