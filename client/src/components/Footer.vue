<template>
  <!-- Footer: Input field + button -->
  <footer class="footer-send" :class="{ active: inputVisible, blurred: mainMenuOpen }">
    <form
      class="container-fluid"
      style="height: 100%"
      @submit.prevent="submitMessage(currentInput)"
    >
      <div class="row" style="height: 100%">
        <!-- Wenn dateSelection nicht gesetzt ist, wird der normale Text Input angezeigt -->
        <div v-if="!dateSelection" class="col-12" style="align-self: center">
          <input
            id="messenger_input"
            name="messageInput"
            ref="text_input"
            v-model="setInput"
            :class="{ input_disabled: !inputVisible }"
            placeholder="Bitte gib deine Nachricht hier ein..."
            type="text"
            autocomplete="off"
            :disabled="inputVisible ? false : true"
          />
          <button
            id="send-message-button"
            :class="{ input_disabled: !inputVisible }"
            class="float-right"
            :disabled="inputVisible ? false : true"
          >
            <font-awesome-icon :icon="['fa', 'long-arrow-alt-right']" />
          </button>
        </div>
        <!-- Wenn dateSelection gesetzt ist, wird statt des Inputs der Kalender angezeigt -->
        <div v-else-if="dateSelection" class="col-12" style="align-self: center">
          <datepicker
            id="date_picker"
            v-if="dateSelection"
            v-model="selectedDate"
            name="datepicker"
            placeholder="Datum wählen"
          ></datepicker>
          <!-- TO DO: Der Button soll den Wert von selectedDate an Rasa übertragen. -->
          <button
            id="send-message-button"
            :class="{ input_disabled: !inputVisible }"
            class="float-right"
            :disabled="inputVisible ? false : true"
            v-on:click="submitMessage(moment(selectedDate).format('DD.MM.YYYY'))"
            type="button"
          >
            <font-awesome-icon :icon="['fa', 'long-arrow-alt-right']" />
          </button>
        </div>
      </div>
    </form>
  </footer>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import MessageHandlerMixin from "../mixins/MessageHandlerMixin";
/* Components */
import Datepicker from "./DatePicker";
import DateInput from "./DateInput";
import moment from 'moment';

export default {
  name: "Footer",
  components: {
    Datepicker,
    DateInput
  },
  mixins: [MessageHandlerMixin],
  computed: {
    ...mapGetters([
      "inputVisible",
      "currentInput",
      "mainMenuOpen",
      "dateSelection",
      "dateInput"
    ]),
    ...mapState(["currentInput"]),
    setInput: {
      set(val) {
        this.$store.commit("setCurrentInput", val);
      },
      get() {
        return this.currentInput;
      }
    }
  },
  watch: {
    selectedDate: function(val) {
		var formattedDate = moment(val).format('DD.MM.YYYY');
		console.log("Changing input to => ", formattedDate);
		this.$store.commit("setCurrentInput", formattedDate);
	}
  },
  mounted() {
    this.$refs.text_input.focus();
  },
  data: function() {
    return {
      bgstyle: {
        color: "red",
        fontSize: "13px"
      },
      selectedDate: "",
	  DateInput: "",
	  moment: moment
    };
  },
  methods: {
    submitMessage: function(text) {
      console.log("SENDING: ", text);
      if (text.length > 1) {
        this.sendMessageToBot(text);
      //  this.$store.commit("setCurrentInput", text.toString().slice(3,15));
      // setTimeout(() => this.$store.commit("setInputVisible", false), 1000);
        this.$store.commit("setInputVisible", false);
      }
    }
  }
};
</script>

<style lang="scss" scoped>
#app .footer-send {
  display: block;
  opacity: 0;
  position: absolute;
  bottom: 0;
  width: 100%;
  font-size: 1.2em;
  /* border-top: 3px solid #eee; */
  padding: 0;
  z-index: 3;
  transition: 0.7s all ease-in-out;
  &.blurred {
    filter: blur(2px);
    -webkit-filter: blur(2px);
  }
  #send-message-button {
    border: none;
    background: none;
    color: white;
    cursor: pointer;
    transition: all 1s ease-in-out;
    padding: 0 0 0 0;
    position: absolute;
    right: 25px;
    top: 11px;
    height: 35px;
    // width: 35px;
    // padding-left: 10px;
    width: 25px;
    margin-left: 10px;
    transition: 0.25s opacity ease-in-out;
    &:hover {
      opacity: 0.75;
    }
  }
  #messenger_input {
    margin: auto;
    font-size: 14px;
    font-family: "Univers Next Pro Regular";
    border: 0;
    outline: none;
    width: 100%;
    border-radius: 0;
    padding: 12px;
    padding-right:40px;
    background: #292929;
    color: white;
    height: 50px;
    margin-bottom: 25px;
    -webkit-transition: all 1s ease-in-out;
    -moz-transition: all 1s ease-in-out;
    -ms-transition: all 1s ease-in-out;
    -o-transition: all 1s ease-in-out;
    transition: all 1s ease-in-out;
    &::placeholder {
      color: white;
    }
    &:focus::-webkit-input-placeholder { color:transparent; }
    &:focus:-moz-placeholder { color:transparent; } /* Firefox 18- */
    &:focus::-moz-placeholder { color:transparent; } /* Firefox 19+ */
    &:focus:-ms-input-placeholder { color:transparent; } /* oldIE 😉 */

    #date_picker {
    &::placeholder {
      color: white;
    }
  }
  }

  

  &.active {
    display: block;
    background: transparent;
    opacity: 1;
  }
}
</style>
