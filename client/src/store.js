/* eslint-disable no-param-reassign */
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);
const initialActiveData = {
  componentName: '',
  values: [],
};
const initialActiveDataImmutable = Object.freeze(initialActiveData);

export default new Vuex.Store({
  state: {
    userId: undefined,
    userEmail: undefined,
    currentInput: '',
    inputVisible: false,
    typing: false,
    showSplashScreen: true,
    currentActiveData: initialActiveData,
    currentGuide: '',
    allMessages: [],
    sphereTextContent: '',
    sphereImageContent: '',
    sphereColor: '',
    name_provided: false,
    icons: [
      {id: 0, name: 'Regenbogen', source: 'icon_regenbogen'},
      {id: 1, name: 'Hi!', source: 'smiley-2'},
      {id: 2, name: 'Peace', source: 'icon_peace'},
      {id: 3, name: 'Anonym', source: 'icon_anonym'},
      {id: 4, name: 'Weisheit', source: 'icon_weisheit'},
      {id: 5, name: 'Auge', source: 'icon_auge'},
      {id: 6, name: 'Atomexplosion', source: 'icon_atomexplosion'},
      {id: 8, name: 'Atomsprengkopf', source: 'icon_atomsprengkopf'},
      {id: 9, name: 'Angst', source: 'icon_angst'},
      {id: 10, name: 'Aufgepasst', source: 'icon_aufgepasst'},
      {id: 11, name: 'Cycling', source: 'icon_cycling'},
      {id: 12, name: 'Herzschlag', source: 'icon_herzschlag'},
      {id: 13, name: 'Taste', source: 'icon_taste'},
      {id: 14, name: 'Koerper', source: 'icon_koerper'},
      {id: 15, name: 'Hitze', source: 'icon_hitze'},
      {id: 16, name: 'Herz', source: 'icon_herz'},
      {id: 17, name: 'Schreiben', source: 'icon_schreiben'},
      {id: 18, name: 'Traurig', source: 'icon_traurig'},
      {id: 19, name: 'BrokenHeart', source: 'icon_brokenheart'},
      {id: 20, name: 'Smile', source: 'icon_smile'},
      {id: 21, name: 'Erstaunt', source: 'icon_erstaunt'},
      {id: 22, name: 'Sinuswelle', source: 'icon_sinuswelle'},
      {id: 23, name: 'Veraergert', source: 'icon_veraergert'},
      {id: 24, name: 'Geraeusch', source: 'icon_geraeusch'},
      {id: 25, name: 'ClosedEyes', source: 'icon_closedeyes'},
      {id: 26, name: 'Zwinker', source: 'icon_zwinker'},
      {id: 27, name: 'Uhr', source: 'icon_uhr'},
      {id: 28, name: 'Maske', source: 'icon_maske'},
      {id: 29, name: 'Auto', source: 'icon_auto'},
      {id: 30, name: 'Heizung', source: 'icon_heizung'},
      {id: 31, name: 'FragendesGesicht', source: 'icon_fragendesgesicht'},
    ],
    mainMenuOpen: false,
    mainMenuAllowOpen: false,
    qrOpen: false,
    backgroundImage: '',
    lottieImage: '',
    dateSelection: false,
    dateInput: '',
    timer: '',
    videoInterrupt: false,
    currentQuickReply: {
      format: 'quick_replies',
      type: 'in',
      iconStyle: 'none',
      quickReplies: [
        {
          title: "Los geht's",
          payload: 'Starte Beratung',
          // payload: 'start-second-bot'
        },
      ],
    },
    currentEmailForm: undefined,
    activeConnection: false,
    showContactForm: false,
    startTour: false,
    feedbackObject: undefined,
    showInputForm: false,
    formText: '',
    submitForm: false,
    quote: '',
    compare: false,
    modal: false,
    slider: false,
    isGuideContext: false
  },
  getters: {
    userId: (state) => state.userId,
    userEmail: (state) => state.userEmail,
    allMessages: (state) => state.allMessages,
    currentQuickReply: (state) => state.currentQuickReply,
    currentGuide: (state) => state.currentGuide,
    inputVisible: (state) => state.inputVisible,
    typing: (state) => state.typing,
    currentInput: (state) => state.currentInput,
    currentActiveData: (state) => state.currentActiveData,
    activeConnection: (state) => state.activeConnection,
    showSplashScreen: (state) => state.showSplashScreen,
    mainMenuOpen: (state) => state.mainMenuOpen,
    mainMenuAllowOpen: (state) => state.mainMenuAllowOpen,
    qrOpen: (state) => state.qrOpen,
    videoInterrupt: (state) => state.videoInterrupt,
    showContactForm: (state) => state.showContactForm,
    isGuideContext: (state) => state.isGuideContext,
    startTour: (state) => state.startTour,
    showSwiperCard: (state) => state.showSwiperCard,
    items: (state) => state.items,
    feedbackObject: (state) => state.feedbackObject,
    videoUrl: (state) => state.videoUrl,
    imageUrl: (state) => state.imageUrl,
    backgroundImage: (state) => state.backgroundImage,
    timer: (state) => state.timer,
    lottieImage: (state) => state.lottieImage,
    dateSelection: (state) => state.dateSelection,
    dateInput: (state) => state.dateInput,
    showInputForm: (state) => state.showInputForm,
    formText: (state) => state.formText,
    submitForm: (state) => state.submitForm,
    quote: (state) => state.quote,
    compare: (state) => state.compare,
    modal: (state) => state.modal,
    slider: (state) => state.slider,
    name_provided: (state) => state.name_provided, 
    getIcon: (state) => {
      return state.icons.find((icon) => icon.name === state.sphereTextContent);
    },
    getIconImageContent: (state) => state.sphereImageContent,    
  },
  mutations: {
    setSphereTextContent(state, value) {
      state.sphereTextContent = value;
    },
    setSphereImageContent(state, value) {
      state.sphereImageContent = value;
    },
    setSphereColor(state, value) {
      state.sphereColor = value;
    },
    setSphereDefault(state) {
      state.sphereColor = '';
      state.sphereTextContent = '';
    },
    setName_provided(state, value) {
      state.name_provided = value
    },
    closeSplashScreen: (state) => {
      state.showSplashScreen = false;
    },
    allowMainMenuOpen: (state) => {
      state.mainMenuAllowOpen = true;
    },
    setMainMenuOpen: (state, val) => {
      state.mainMenuOpen = val;
    },
    setQrOpen: (state, val) => {
      state.qrOpen = val;
    },
    setVideoInterrupt: (state, val) => {
      state.videoInterrupt = val
    },
    setUserId: (state, str) => {
      state.userId = str;
    },
    setUserEmail: (state, str) => {
      state.userEmail = str;
    },
    setCurrentGuide: (state, str) => {
      state.currentGuide = str;
    },
    storeNewMessage: (state, obj) => {
      state.allMessages.push(obj);
    },
    setCurrentQuickReply: (state, obj) => {
      state.currentQuickReply = obj;
    },
    setTypingIndicator: (state, val) => {
      state.typing = val;
    },
    setInputVisible: (state, val) => {
      state.inputVisible = val;
    },
    setCurrentInput: (state, val) => {
      state.currentInput = val;
    },
    setCurrentItems: (state, val) => {
      state.items = val;
      state.showSwiperCard = true;
    },
    setFormText: (state, val) => {
      state.formText = val;
    },
    hideComponentsAfterSend: (state) => {
      state.currentActiveData = JSON.parse(JSON.stringify(initialActiveDataImmutable));
      state.currentQuickReply = undefined;
      state.currentInput = '';
      state.inputVisible = false;
      state.showContactForm = false;
      // state.isGuideContext = false;
      state.feedbackObject = undefined;
      state.backgroundImage = '';
      state.lottieImage = '';
      state.dateSelection = false;
      state.dateInput = '';
      // state.imageUrl = "";
      state.showInputForm = false;
      state.submitForm = false;
      // state.mainMenuOpen = false;
      state.timer = '';
      state.sphereColor = '';
      state.sphereTextContent = '';
      state.compare = false;
      state.quote = false;
      state.modal = false;
      state.slider = false;
    },
    setActiveConnection: (state, val) => {
      state.activeConnection = val;
    },
    setShowContactForm: (state, val) => {
      state.showContactForm = val;
    },
    setContextGuide: (state, val) => {
      state.isGuideContext = val;
    },
    setStartTour: (state, val) => {
      state.startTour = val;
    },
    setFeedback: (state, val) => {
      state.feedbackObject = val;
    },
    setBackgroundImage: (state, val) => {
      state.backgroundImage = val;
    },
    setQuote: (state, val) => {
      state.quote = val;
    },
    setModal: (state, val) => {
      state.modal = val;
    },
    setSlider: (state, val) => {
      state.slider = val;
    },
    setCompare: (state, val) => {
      state.compare = val;
    },
    setLottieImage: (state, val) => {
      state.lottieImage = val;
    },
    setDateSelection: (state, val) => {
      state.dateSelection = val;
    },
    setDateInput: (state, val) => {
      state.dateInput = val;
    },
    setShowInputForm: (state, val) => {
      state.showInputForm = val;
    },
    setSubmitForm: (state, val) => {
      state.submitForm = val;
    },
    setTimer: (state, val) => {
      state.timer = val;
    },
  },
  actions: {},
});
