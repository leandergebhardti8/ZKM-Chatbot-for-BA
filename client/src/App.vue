<template>
	<div style="height: 100%; width: 100%;">
		<div class="connecting-overlay" :class="!activeConnection ? 'show' : ''">
			<div class="lds-grid active">
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
			</div>
			<p>Waiting for connection ...</p>
		</div>
		<div id="app">
			<Header />
			<Chat />
			<Footer />
		</div>
	</div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';

import Chat from './components/Chat.vue';
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import MessageHandlerMixin from './mixins/MessageHandlerMixin';
import {generateUserId} from './helpers';

export default {
	name: 'App',
	components: {
		Chat,
		Header,
		Footer
	},
	mixins: [MessageHandlerMixin],
	computed: {
		...mapGetters(['activeConnection', 'showSplashScreen']),
	},
	mounted() {
		const uid = generateUserId();
		/* Append a userId to the user */
		this.$store.commit('setUserId', uid);
		/* Init WebSocket Event Listeners */
		this.$socket.onclose = () => {
			console.log('Socket closed ...');
			this.$store.commit('setActiveConnection', false);
			// setTimeout(() => {
			// 	console.log('Websocket reconnect try ...');
			// 	this.initWebSockets();
			// }, 3000);
		};

		this.$socket.onerror = () => {
			this.$store.commit('setActiveConnection', false);
			console.log('Socket error  ...');
		};
	},

	methods: {},
	sockets: {
		connect() {
			console.log('Socket opened for ', this.$store.state.userId);
			this.$store.commit('setActiveConnection', true);
		},
		disconnect() {
			console.log('Socket closed ...');
			this.$store.commit('setActiveConnection', false);
			// setTimeout(() => {
			// 	console.log('Websocket reconnect try ...');
			// 	this.initWebSockets();
			// }, 3000);
		},
		session_confirm(remoteId) {
			console.log(`session_confirm:${this.$socket.id} session_id:${remoteId}`);
			if (this.userId === remoteId) {
				console.log('Checked user id :)');
				this.$socket.emit('user_uttered', {
					message: '/get_started',
					session_id: this.local_id
				});
			}
		},
		bot_uttered(data) {
			/* Set input visibility */
				//this.$store.commit('hideComponentsAfterSend');
				console.log("data entered ", data)
				this.checkAttribute(data);
				if (data.type === 'typing') {
					this.$store.commit('setTypingIndicator', true);
				} else {
					this.$store.commit('setTypingIndicator', false);
					const messageFormat = this.setFormatOfIncomingMessage(data);
					console.log("setting format of data ", messageFormat);
					this.addNewMessage(data, 'in', messageFormat);
				}
		}
	},
};
</script>

<style lang="scss">
@font-face {
	font-family: 'Univers Next Pro Black';
	src: url('~@/assets/fonts/Univers Next Pro/UniversNextPro-Black.ttf')
}

@font-face {
	font-family: 'Univers Next Pro Regular';
	src: url('~@/assets/fonts/Univers Next Pro/UniversNextPro-Regular.ttf')
}

* {
	font-weight: normal;
	/* transition: 1s all ease-in-out; */
}

img {
	-webkit-user-select: none;
	-khtml-user-select: none;
	-moz-user-select: none;
	-o-user-select: none;
	user-select: none;
	-webkit-user-drag: none;
	-khtml-user-drag: none;
	-moz-user-drag: none;
	-o-user-drag: none;
	-webkit-touch-callout: none;
	/* iOS Safari */
	pointer-events: none;
}

#app {
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	width: 100%;
	height: 100%;
	background-color: black;
	color: white;
		font-family: 'Univers Next Pro Regular';
	font-weight: normal;
	font-size: 14px;
	// background: #000;
	margin: 0 !important;
	min-height: 100%;
	overflow: hidden;
	// color: #ffffff;
	-webkit-user-select: none;
	/* Chrome all / Safari all */
	-moz-user-select: none;
	/* Firefox all */
	-ms-user-select: none;
	/* IE 10+ */
	user-select: none;
	/* Likely future */
	@import 'node_modules/bootstrap/scss/bootstrap';
}

.connecting-overlay {
	position: absolute;
	top: 0;
	min-height: 100px;
	height: 100%;
	width: 100%;
	transition: all 0.5s ease-in-out;
	opacity: 0;
	font-family: 'Univers Next Pro Regular';

	&.show {
		z-index: 10000;
		background: rgba(20, 20, 20, 0.92);
		opacity: 1;
	}
	& > p {
		position: absolute;
		top: calc(50% + 80px);
		left: 50%;
		transform: translate(-50%, -50%);
		font-size: 14px;
		width: 100%;
		text-align: center;
		background: linear-gradient(to right, #fff 20%, #000 50%, #fff 100%);
		background-size: 200% auto;
		color: #000;
		background-clip: text;
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		animation: shine 3s linear infinite;
		@keyframes shine {
			to {
				background-position: 200% center;
			}
		}
	}
}

@keyframes slide-up-fade-in {
	0% {
		opacity: 0;
		transform: translate(0px, 40px);
	}
	100% {
		opacity: 1;
		transform: translate(0px, 0px);
	}
}

@keyframes fade-in {
	0% {
		opacity: 0;
	}
	100% {
		opacity: 1;
	}
}

.msg-div {
	animation: fade-in 1s ease;
}

.full-height {
	height: 100%;
	width: 100%;
	overflow: hidden;
}

.lds-grid {
	display: inline-block;
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	width: 96px;
	height: 100px;
	transition: all 0.5s ease-in-out;
	opacity: 0;
	&.active {
		opacity: 1;
	}
	& > div {
		position: absolute;
		width: 26px;
		height: 26px;
		border-radius: 50%;
		background: #fff;
		animation: lds-grid 1.2s linear infinite;
	}
	& > div:nth-child(1) {
		top: 3px;
		left: 0px;
		animation-delay: 0s;
	}
	& > div:nth-child(2) {
		top: 3px;
		left: 35px;
		animation-delay: -0.4s;
	}
	& > div:nth-child(3) {
		top: 3px;
		left: 70px;
		animation-delay: -0.8s;
	}
	& > div:nth-child(4) {
		top: 35px;
		left: 0px;
		animation-delay: -0.4s;
	}
	& > div:nth-child(5) {
		top: 35px;
		left: 35px;
		animation-delay: -0.8s;
	}
	& > div:nth-child(6) {
		top: 35px;
		left: 70px;
		animation-delay: -1.2s;
	}
	& > div:nth-child(7) {
		top: 70px;
		left: 0px;
		animation-delay: -0.8s;
	}
	& > div:nth-child(8) {
		top: 70px;
		left: 35px;
		animation-delay: -1.2s;
	}
	& > div:nth-child(9) {
		top: 70px;
		left: 70px;
		animation-delay: -1.6s;
	}
	@keyframes lds-grid {
		0%,
		100% {
			opacity: 1;
		}
		50% {
			opacity: 0.5;
		}
	}
}
</style>
