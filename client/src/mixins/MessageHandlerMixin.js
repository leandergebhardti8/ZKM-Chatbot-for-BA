import { mapGetters, mapState } from 'vuex';

console.log('MESSAGE HANDLER MIXIN LOADED');

export default {
  name: 'MessageHandlerMixin',
  computed: {
    ...mapGetters(['showSplashScreen', 'userId', 'currentInput']),
  },
  methods: {
    /* Renders a message to the screen, depending on the type */
    addNewMessage: function(data, type, format) {
      /* TEXT MESSAGE */
      console.log({data});
      console.log('incoming format ' + format);

      this.$store.commit('setSphereDefault');

      /* 
      Renders picture horizontal slider
      */
      if (data.items && data.items.length > 0) 
      {
        this.$store.commit('storeNewMessage', {
          text: '',
          type: type,
          format: 'items',
          data: data.items,
        });
      }

      if (data.sphereTextContent) 
      {
        this.$store.commit('setSphereTextContent', data.sphereTextContent);
      } else {
        this.$store.commit('setSphereDefault');
      }

      if(data.sphereImageContent)
      {
        this.$store.commit('setSphereImageContent', data.sphereImageContent);
      }

      if (data.sphereColor) 
      {
        this.$store.commit('setSphereColor', data.sphereColor);
      }

      if (data.inputContact) 
      {
        this.$store.commit('setShowInputForm', data.inputContact);
        return this.$store.commit('setFormText', data.text);

        this.scrollChatToBottom();
      }
      /* After the name is provided this is used to unlock Menu functionalities */
      if (data.name_provided) 
      {
        this.$store.commit('setName_provided', data.name_provided);
      }

      /* Check for feedback object */
      if (data.feedback) {
        return this.$store.commit('setFeedback', {
          text: data.text,
          buttons: data.quick_replies,
        });

        this.scrollChatToBottom();
      }

      if (data.text && data.text.length >= 1 && !data.modal)  
      {
        if (!data.mute_text) {
          this.$store.commit('storeNewMessage', {
            text: data.text,
            type: type,
            format: 'message',
          });

          this.scrollChatToBottom();
        }
      }

      /* IMAGE */

      if (data.img) 
      {
        this.$store.commit('storeNewMessage', {
          text: '',
          type: type,
          format: 'img',
          data: data.img,
          subtitle: data.subtitle
        });

        this.scrollChatToBottom();
      }

      /* LOTTIE */

      if (data.lottieImage) 
      {
        this.$store.commit('storeNewMessage', {
          text: '',
          type: type,
          format: 'lottie',
          data: data.lottieImage,
        });

        this.scrollChatToBottom();
      }

      /* VIDEO */

      if (data.video && Object.keys(data.video).length > 0) 
      {
        this.$store.commit('storeNewMessage', {
          text: data.text,
          type: type,
          format: 'video',
          data: data.video
        });

        this.scrollChatToBottom();
      }

      /* QUOTE */

      if (data.quote && Object.keys(data.quote).length > 0) 
      {
        return setTimeout(() => {
        this.$store.commit('storeNewMessage', {
          quote: data.quote, 
          type: type,
          format: 'quote-card',
        });

        this.scrollChatToBottom();
        }, 1000);
      }

      /* INTERVAL */

      if (data.interval && Object.keys(data.interval).length > 0) {
        return setTimeout(() => {
        this.$store.commit('storeNewMessage', {
          options: this.setMarks(data.interval),
          type: type,
          format: 'slider',
        });

        this.scrollChatToBottom();
        }, 1000);
      }

      /* SLIDER */

      if (data.slider && Object.keys(data.slider).length > 0) 
      {
        return setTimeout(() => {
        this.$store.commit('storeNewMessage', {
          slider: data.slider, 
          marks: this.setMarksValues(data.slider),
          type: type,
          format: 'slider-values',
        });

        this.scrollChatToBottom();
        }, 1000);
      }

      /* MODAL */

      if (data.modal && Object.keys(data.modal).length > 0) 
      {
        this.$store.commit('storeNewMessage', {
          text: data.text,
          modal: data.modal,
          type: type,
          format: 'modal',
        });

        this.scrollChatToBottom();
      }

      /* WERKINTRO */

      if (data.intro && Object.keys(data.intro).length > 0) {
        this.$store.commit('storeNewMessage', {
          intro: data.intro,
          type: type,
          format: 'intro',
        });

        this.scrollChatToBottom();
      }
      
      /* QUICK REPLIES */

      if (data.quick_replies && data.quick_replies.length > 0) {
        return setTimeout(() => {
          this.$store.commit('setCurrentQuickReply', {
            text: data.text,
            format: format,
            type: type,
            quickReplies: data.quick_replies,
          });

          this.scrollChatToBottom();
        }, 1000);
      } 
      
      /* STATIC BUTTONS */ 
      
      if (format === 'button') 
      {
        return setTimeout(() => {
          this.$store.commit('storeNewMessage', {
            text: data.text,
            format: format,
            type: type,
            buttons: data.buttons,
          });

          this.scrollChatToBottom();
        }, 1000);
      }

       /* Links BUTTONS */ 

      if (data.links && data.links.length > 0) 
      {
          this.$store.commit('storeNewMessage', {
            format: 'link_button',
            type: type,
            links: data.links,
          });

          this.scrollChatToBottom();
      } 

      if (format === 'set_user_email') {
        return this.$store.commit('setUserEmail', data.text);
      }
    },
    sendMessageToBot: function(text) {
      /* Send message to the bot if it isn't empty */
      if (text && text.length >= 1 && text.replace(/\s/g, '').length !== 0) {
        /* Append to array of messages (so that it gets rendered to the screen) */
        this.addNewMessage({ text: this.currentInput }, 'out', 'message');
        console.log('text:', text);
        // if(text.includes('email_senden_guide')){
        //   text = '/email_senden_guide';
        // }
        console.log('text2:', text);
        // this.$socket.emit('user_uttered', { message: "/email_senden_guide", room: this.userId });
        this.$socket.emit('user_uttered', { message: text, room: this.userId });
        this.$store.commit('hideComponentsAfterSend');
      }
    },
    setMarks(options){
      let marks = {};
      options.map((option, index) => {
        marks[`${index}`] = {
          label: Object.keys(options).length <= 3? option.title : "",
          payload: option.payload,
          title: option.title,
          labelStyle: {
            'font-size': Object.keys(options).length > 2? '14px' : '20px',
            'color': '#fff',
            'float': 'right',
            'font-family': 'Univers Next Pro Regular',
            'margin-top': '1rem',
            'padding': '11px'
          }
        }
      });
      return marks;
    },
    setMarksValues(values){
      let marks = {};
      marks[values.min] = {
        label: `${values.min} ${values.unit}`
      },
      marks[values.max] = {
        label: `${values.max} ${values.unit}`
      }
      return marks;
    },
    sendQrPayloadToBot: function(qrObj) {
      if (qrObj.text && qrObj.payload) {
        console.log("why im doing this ", {qrObj})

        if (qrObj.payload === 'Starte Beratung') {
          this.$store.commit('closeSplashScreen');
          // this.$store.commit('allowMainMenuOpen'); //bot starts after Splshscreen is closed
          this.$store.commit('setStartTour', false);
        } else if (qrObj.payload === 'Starte die Tour') {
          this.$store.commit('setStartTour', true);
        }
        this.$socket.emit('user_uttered', {
          message: qrObj.payload,
          room: this.userId,
        });
        this.$store.commit('hideComponentsAfterSend');
        this.$store.commit('setVideoInterrupt', true);
      }
    },
    sendFormToBot: function(formObj) {
      let message = '';
      formObj.text == 'cancel'
        ? (message = 'Abbrechen')
        : (message = `email info ${formObj.emailFrom} # ${formObj.text}`);
      this.$socket.emit('user_uttered', {
        message: message,
        room: this.userId,
      });
      this.$store.commit('hideComponentsAfterSend');
    },
    sendTriggerToBot: function(obj) {
      if (obj.text && obj.payload) {
        this.addNewMessage(obj, 'out', 'message');
        if (obj.payload === 'Starte Beratung') {
          this.$store.commit('closeSplashScreen');
          this.$store.commit('allowMainMenuOpen');
        }
        this.$socket.emit('user_uttered', {
          message: obj.payload,
          room: this.userId,
        });
        this.$store.commit('hideComponentsAfterSend');
        this.$store.commit('setStartTour', false);
        this.$store.commit('setMainMenuOpen', false);
        this.$store.commit('setQrOpen', false);
      }
      if (obj.img && obj.payload) {
        this.addNewMessage(obj, 'out', 'img');
        this.$socket.emit('user_uttered', {
          message: obj.payload,
          room: this.userId,
        });
        this.$store.commit('hideComponentsAfterSend');
        this.$store.commit('setStartTour', false);
        this.$store.commit('setMainMenuOpen', false);
      }
    },
    scrollChatToBottom: function() {
      $('.chat-container').stop();
      const scrollPosition = $('.chat-container')[0].scrollHeight;
      $('.chat-container').on("mousedown wheel DOMMouseScroll mousewheel touchmove", function(){
        $('.chat-container').stop();
      });
      $('.chat-container').animate({ scrollTop: scrollPosition }, 1000, function(){
        $('.chat-container').off("scroll mousedown wheel DOMMouseScroll mousewheel keyup touchmove");
      });
    },
    checkAttribute: function(data) {
      console.log('Input Visibility: ' + data.allowTyping);
      console.log("isGuide " + data.isGuideContext);
      console.log("contact " + data.contact);
      if (data.isGuideContext){
        this.$store.commit('setContextGuide', data.isGuideContext);
      }
      if (data.contact) {
        this.$store.commit('setShowContactForm', data.contact);
      } else {
        this.$store.commit('setInputVisible', data.allowTyping);
      }
      if (data.backgroundImage) {
        console.log('should change background ', data.backgroundImage);
        this.$store.commit('setBackgroundImage', data.backgroundImage);
      }
      if (data.quote) {
        console.log('this is a quote', data.quote);
        this.$store.commit('setQuote', data.quote);
      }
      if (data.modal) {
        console.log('this is a modal', data.modal);
        this.$store.commit('setModal', data.modal);
      }
      if (data.compare) {
        console.log('compare image', data.compare);
        this.$store.commit('setCompare', data.compare);
      }
      if (data.dateSelection) {
        console.log('show date picker', data.dateSelection);
        this.$store.commit('setDateSelection', data.dateSelection);
      }
      if (data.dateInput) {
        console.log('User date input', data.dateInput);
        this.$store.commit('setDateInput', data.dateInput);
      }
      if (data.submitForm) {
        console.log('submitForm set to =>', data.submitForm);
        this.$store.commit('setSubmitForm', data.submitForm);
      }
      if (data.timer) {
        console.log('should show timer ', data.timer);
        this.$store.commit('setTimer', data.timer);
      }
      if(data.video) {
        this.$store.commit('setVideoInterrupt', false);
      }
      this.scrollChatToBottom();
    },
    setFormatOfIncomingMessage: function(data) {
      if (data.links && data.links.length > 0) {
        return 'link_button';
      }
      return 'message';
    },
  },
};
