<template>
  <div 
    class="qr-overlay"
    :class="qrOpen ? 'qr-shown' : 'qr-hidden'"
  >
    <div class="qr-wrapper">
      <div
          class="qr-element"
      >
        <p class="qr-item">Scanne einfach den QR Code zu Beginn der Führung</p>
      </div>
      <div class="qr-reader">
        <qrcode-stream 
          @decode="onDecode"
        >
        </qrcode-stream>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import MessageHandlerMixin from "../mixins/MessageHandlerMixin";
import { QrcodeStream } from 'vue-qrcode-reader';

export default {
  name: "QrReader",
  mixins: [MessageHandlerMixin],
  computed: {
    ...mapGetters(["qrOpen"]),
  },
  components: {
    QrcodeStream,
  },
  data() {
    return {
      qrText: '',
    };
  }, 
  methods: {
    // Sendet Payload mit decodedetem Text an den Chatbot.
    onDecode (decodedString) {
      this.qrText = decodedString;
      this.startGuide();
    },
    startGuide (){
      this.$store.commit('setQrOpen', false);
      this.sendTriggerToBot({
        text: 'Starte Guide',
        payload: this.qrText,
      });
    }
  }
};
</script>

<style lang="scss" scoped>
#app .qr-overlay {
  top: 0;
  height: 100%;
  position: absolute;
  width: 100%;

  .qr-wrapper {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background: rgba(0, 0, 0, 0.9);
    .qr-reader {
      margin: 15px;
      border: 1px solid white;
    }
    .qr-element {
      max-width: 350px;
      width: 100%;
      text-align: center;
      margin: 5px 0 5px 0;
      border-radius: 0;
      color: white;
      height: 38px;
      display: block;
      box-sizing: border-box;
      .qr-item {
        font-size: 14px;
        line-height: 24px;
        color: white;
        display: inline;
      }
    }
  }
}
</style>
