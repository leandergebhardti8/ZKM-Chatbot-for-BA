<template>
	<div id="current-toggle-switch" class="msg-div">
		<div class="toggle-switch-wrapper row text-center">
			<div class="col-4 text-right">
				<span
					class="option-label"
					:class="{ active: !switchActive }"
					@click="setSwitchTo(false)"
				>
					<img
						v-if="currentQuickReply.formatType === 'contact_option'"
						class="contact-icon"
						src=""
					/>
					<img
						v-else-if="currentQuickReply.formatType === 'rating'"
						class="contact-icon"
						src=""
					/>
				</span>
			</div>
			<div
				class="col-4 text-center"
				style="display: flex; align-items: center; justify-content: center;"
			>
				<label class="switch">
					<input v-model="switchActive" type="checkbox" />
					<div class="slider"></div>
				</label>
			</div>
			<div class="col-4 text-left">
				<span
					class="option-label"
					:class="{ active: switchActive }"
					@click="setSwitchTo(true)"
				>
					<img
						v-if="currentQuickReply.formatType === 'contact_option'"
						class="contact-icon"
						src=""
					/>
					<img
						v-else-if="currentQuickReply.formatType === 'rating'"
						class="contact-icon"
						src=""
					/>
				</span>
			</div>
		</div>
		<div class="confirm-button">
			<input type="button" value="Bestätigen" @click="sendToggle(currentActiveData)" />
			<!-- @click="sendQrPayloadToBot(currentActiveData)" -->
		</div>

		<div v-if="showEmoji" class="emoji-wrapper">
			<div v-if="currentActiveData.text === 'Ja'" class="happy text-center">
				<img class="rate-emoji" src="" />
				<p>Super!</p>
			</div>
			<div v-else-if="currentActiveData.text === 'Nein'" class="happy text-center">
				<img class="rate-emoji" src="" />
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from 'vuex';
import { setTimeout } from 'timers';
import MessageHandlerMixin from '../mixins/MessageHandlerMixin';

export default {
	name: 'ToggleSwitch',
	mixins: [MessageHandlerMixin],
	data() {
		return {
			switchActive: false,
			currentActiveData: {
				text: undefined,
				payload: undefined
			},
			showEmoji: false
		};
	},
	computed: {
		...mapGetters(['currentQuickReply'])
	},
	watch: {
		switchActive: async function() {
			if (!this.switchActive) {
				this.currentActiveData = {
					text: this.currentQuickReply.quickReplies[0].title,
					payload: this.currentQuickReply.quickReplies[0].payload
				};
			} else {
				this.currentActiveData = {
					text: this.currentQuickReply.quickReplies[1].title,
					payload: this.currentQuickReply.quickReplies[1].payload
				};
			}
		}
	},
	async mounted() {
		console.log('QR: ', this.currentQuickReply);
		this.currentActiveData.text = this.currentQuickReply.quickReplies[0].title;
		this.currentActiveData.payload = this.currentQuickReply.quickReplies[0].payload;
	},

	methods: {
		setSwitchTo: function(status) {
			this.switchActive = status;
		},
		sendToggle: function(data) {
			if (data.text === 'Ja' || data.text === 'Nein') {
				this.showEmoji = true;
				setTimeout(() => {
					this.scrollChatToBottom();
					setTimeout(() => {
						$('#current-toggle-switch').fadeOut(1000);
					}, 1000);

					setTimeout(() => {
						this.sendQrPayloadToBot(data);
					}, 2000);
				}, 250);
			} else {
				this.sendQrPayloadToBot(data);
			}
		}
	}
};
</script>

<style lang="scss" scoped>
$thyBlue: #00a0f0;
$thyWhite: #fafafa;
#app .msg-div {
	padding-bottom: 25px;
	.confirm-button {
		text-align: center;
		margin-top: 46px;

		& > input {
			max-width: 282px;
			width: 100%;
			height: 44px;
			background-color: $thyBlue;
			color: $thyWhite;
			border-radius: 5px;
			transition: all 0.3s ease;
			outline: none;
			cursor: pointer;
			&:hover {
				opacity: 0.65;
			}
		}
	}
	.emoji-wrapper {
		margin-top: 46px;
		animation: fade-in 1s ease;
		.happy {
			.rate-emoji {
				width: 81px;
			}

			& > p {
				color: $thyBlue;
				margin-top: 16px;
			}
		}
	}
	.toggle-switch-wrapper {
		margin: auto;
		margin-top: 15px;
		margin-bottom: 15px;
		.option-label {
			font-size: 30px;
			line-height: 30px;
			cursor: pointer;
			transition: all 0.35s ease;
			opacity: 0.6;
			filter: grayscale(1);
			@media only screen and (max-width: 350px) {
				font-size: 26px;
				line-height: 26px;
			}
			.contact-icon {
				height: 40px;
				max-width: 100%;
			}
		}
		.option-label.active {
			opacity: 1;
			filter: grayscale(0);
		}
		.switch {
			position: relative;
			display: inline-block;
			width: 50px;
			height: 25px;
			input {
				display: none;
			}
			.slider {
				position: absolute;
				cursor: pointer;
				top: 0;
				left: 0;
				right: 0;
				bottom: 0;
				border: solid 1px $thyBlue;
				background-color: $thyBlue;
				border-radius: 25px;
				-webkit-transition: 0.4s;
				transition: 0.4s;
			}
			.slider:before {
				position: absolute;
				content: '';
				height: 23px;
				width: 23px;
				border-radius: 50%;
				left: 0px;
				bottom: 0px;
				background-color: white;
				border: solid 1px #00a0f0;
				-webkit-transition: 0.4s;
				transition: 0.4s;
				box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.2);
				@media only screen and (max-width: 384px) {
					height: 23px;
					width: 23px;
				}
			}
			input:focus + .slider {
				box-shadow: 0 0 1px #2196f3;
			}
			input:checked + .slider:before {
				-webkit-transform: translateX(25px);
				-ms-transform: translateX(25px);
				transform: translateX(25px);
			}
		}
	}
}
</style>
