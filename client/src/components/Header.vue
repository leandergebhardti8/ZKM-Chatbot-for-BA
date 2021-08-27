<template>
	<div class="header">
		<div class="row">
			<div :class="name_provided ? 'col' : 'col text-left'">
				<span class="tooltiptext">{{ tooltipText }}</span>
				<div
					class="hamburger-container"
					:class="menuOpen ? 'active' : ''"
					@click="toggleMenuStatus"
				>
					<div class="bar1"></div>
					<div class="bar2"></div>
					<div class="bar3"></div>
				</div>
				<div
					class="refresh-container"
					@click="
						sendTriggerToBot({
							text: 'Chat neu starten',
							payload: 'RESTART',
							action_type: 'trigger'
						})
					"
				>
				</div>
			</div>
			<div :class="name_provided ? 'col' : 'col text-left'">
				<span class="tooltiptext">{{ tooltipText }}</span>
				<div 
					class="qr-code-icon" 
					@click="toggleQRCodeReader"
				>
				<div 
					class="scann-bar"
					:class="qrOpen ? 'active' : ''"
				>
				</div>
					<img 
						src="../assets/icons/icon_qr_code.svg" 
						alt="icon-qr-code" 
						height="27.5px" 
						width="27.5px"
					>
				</div>
			</div>
			<div class="col-5 text-center header-content-wrapper">
				<img  id="header-logo" src="../assets/icons/zkm-logo.svg" />
			</div>
			<div class="col text-right" >
				<img v-if="!menuOpen" style="cursor: pointer;pointer-events: all;" id="close-chatbot" 
				src="../assets/icons/close-btn.svg" alt="close chat" role="button"/>
			</div> 
		</div>
	</div>
</template>

<script>
import { mapGetters } from 'vuex';
import MessageHandlerMixin from '../mixins/MessageHandlerMixin';

export default {
	name: 'Header',
	mixins: [MessageHandlerMixin],
	data() {
		return {
			menuOpen: false,
			menuAllowOpen: false,
			fadeAnimation: false,
			tooltipText: 'Bitte starte erst den Chatbot und gebe deinen Namen an.'
		};
	},
	computed: {
		...mapGetters([
			'mainMenuOpen',
			'mainMenuAllowOpen',
			'qrOpen',
			]),
		name_provided() {
            return this.$store.getters.name_provided
        }
	},
	watch: {
		mainMenuOpen: function(val) {
			console.log('MAIN: ', val);
			if (this.menuOpen !== val) {
				this.menuOpen = val;
			}
		},
		qrOpen: function(val) {
			console.log('QR-Reader: ', val);
			if (this.qrOpen !== val) {
				this.qrOpen = val;
			}
		},
		name_provided: function(val) {
			console.log('ALLOW MAIN MENU TO OPEN: ', val);
			if (this.menuAllowOpen !== val) {
				this.menuAllowOpen = val;
			}
		}
	},
	methods: {
		toggleMenuStatus: function() {
			if (this.fadeAnimation) {
				console.log('Still animating');
			} else if (!this.fadeAnimation) {
				if (!this.menuOpen && this.menuAllowOpen && !this.qrOpen) {
					this.menuOpen = true;
					this.$store.commit('setMainMenuOpen', true);
				} else {
					this.menuOpen = false;
					this.$store.commit('setMainMenuOpen', false);
				}
			}
		},
		toggleQRCodeReader: function() {
			if (!this.qrOpen && this.menuAllowOpen && !this.menuOpen) {
				this.$store.commit('setQrOpen', true);
			} else {
				this.$store.commit('setQrOpen', false);
			}

		}
	}
};
</script>

<style lang="scss" scoped>
$avatarBG: #ebf8ff;
#app .header {
	position: absolute;
	top: 0;
	height: 45px;
	width: 100%;
	padding: 0 10px 0 10px;
	line-height: 42px;
	z-index: 11;
	display: grid;
	grid-template-columns: auto;
	border-bottom: 2px solid #70CDB2;
	background: black;
	.hamburger-container {
		display: inline-block;
		vertical-align: middle;
		cursor: pointer;
		.bar1,
		.bar2,
		.bar3 {
			width: 25px;
			height: 1px;
			background-color: $avatarBG;
			margin: 6px 0;
			transition: 0.4s;
		}
		&.active > .bar1 {
			-webkit-transform: rotate(-45deg) translate(-4px, 5px);
			transform: rotate(-45deg) translate(-4px, 5px);
		}
		&.active > .bar2 {
			opacity: 0;
		}
		&.active > .bar3 {
			-webkit-transform: rotate(45deg) translate(-5px, -5px);
			transform: rotate(45deg) translate(-5px, -5px);
		}
	}
	.header-content-wrapper {
		#header-logo {
			height: 18px;
			color: white;
		}
	}
	#header-logo, #close-chatbot {
		display: inline-block;
	}

	.qr-code-icon {
		cursor: pointer;
	}

	.scann-bar {
		visibility: hidden;
		width: 27.5px;
		height: 1px;
		background-color: red;
		margin: 6px 0;
		transition: 0.4s;
		position: absolute;

		&.active {
			visibility: visible;
			animation: scan 3s linear infinite alternate;
		}

		@keyframes scan {
			0%, 100% {
				-webkit-transform: translate(0, 0);
				transform: translate(0, 0);
			}
			
			50% {
				-webkit-transform: translate(0, 27.5px);
				transform: translate(0, 27.5px);
			}
		}
	}

	.text-left > .tooltiptext {
		visibility: hidden;
		width: 240px;
		background-color: black;
		color: #fff;
		text-align: center;
		border: 1px solid white;
		line-height: 16px;
		padding: 5px 0;

		/* Position the tooltip */
		position: absolute;
		z-index: 1;
		top: 5px;
		left: 110%;

		&::after {
			content: "";
			position: absolute;
			top: 50%;
			right: 100%;
			margin-top: -5px;
			border-width: 5px;
			border-style: solid;
			border-color: transparent white transparent transparent;
		}
	}

	.col > .tooltiptext {
		visibility: hidden;
		position: absolute;
	}

	.text-left:hover .tooltiptext{
		visibility: visible;
	}

	.placeholder {
		height: 27.5px;
		width: 27.5px;
	}
}
</style>
