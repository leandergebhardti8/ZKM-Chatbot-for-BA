<template>
	<div class="incoming-msg msg-div row">
		<div class="col-12">
			<div class="form-wrapper">
				<form
					autocomplete="off"
					class="container-fluid email-form-el"
					style="height: 100%"
					@submit.prevent="submitFormToBot"
					@reset.prevent="cancelForm"
				>
					<div class="row">
						<!-- Email -->
						<div
							class="col-12 email-from-wrapper input-style-wrapper"
							style="align-self: center"
						>
							<!-- <label>Deine E-Mail Adresse:</label> -->
							<input
								id="email-from"
								v-model="emailFrom"
								class="input-style"
								type="text"
								placeholder="E-Mail Adresse"
							/>
							
						</div>
						<div v-if="!emailValid" class="col-12 small-message">
							Bitte gültige Email-Adresse eingeben
						</div>
						
						<!-- Message -->
					</div>
					<div class="row">
						<div class="col-12 email-content-wrapper input-style-wrapper">
							<textarea
								id="email-content"
								v-model="emailContent"
								class="input-style"
								placeholder="Ihre Nachricht an uns"
							></textarea>
						</div>
						
					</div>
					<!-- Submit/Cancel buttons -->
					<div class="row" style="margin-top:8px;">
						<div class="submit-form-btn-wrapper">
							<div class="errorMessage" style="display:inline; width:50%;">{{errorMessage}}</div>
							<button id="btn-form" type="submit" class="form-button" :disabled="!emailValid">
								<font-awesome-icon :icon="['fa', 'play']"/>
								<!--img src="~@/assets/icons/send-arrow.svg" style="height: 18px" /-->
							</button>
							<button id="btn-form" type="reset" class="form-button">
								<font-awesome-icon :icon="['fa', 'times']"/>
								<!--img src="../assets/icons/müll.svg" style="height: 18px;" /-->
							</button>
						</div>
					</div>
				</form>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from 'vuex';
import validator from 'validator';
import messageHandlerMixin from '../mixins/MessageHandlerMixin';

export default {
	name: 'UserInputForm',
	mixins: [messageHandlerMixin],
	data() {
		return {
			emailFrom: this.userEmail ? this.userEmail : '',
			emailContent: this.initialText,
			emailValid: false,
			contentValid: false,
			errorMessage: '',
			guideContext: this.isGuideContext
		};
	},
	props:{
		initialText: {
			type: String,
			default: "",
		},
		email: {
			type: String,
			default: ""
		},
		submitForm: {
			type: Boolean,
			default: false
		}
	},
	computed: {
		...mapGetters(['userEmail','isGuideContext'])
	},
	watch: {
		emailFrom: function(val) {
			console.log("email Valid = ", this.emailValid);
			if (!validator.isEmail(val) || /<[a-z][\s\S]*>/gi.test(val)) {
				$('.email-from-wrapper').css('border-color', '#fbd143');
				return this.emailValid = false;
			} 
			$('.email-from-wrapper').css('border-color', '#143F94');
			this.emailValid = true
		},
		emailContent: function(val) {
			if (val.length < 5 || /<[a-z][\s\S]*>/gi.test(val)) {
				$('.email-content-wrapper').css('border-color', '#fbd143');
				return this.contentValid = false;
			} 
			$('.email-content-wrapper').css('border-color', '#143F94');
			this.contentValid = true;
		}
	},
	methods: {
		submitFormToBot(){
			// this.submitForm = true
			console.log("email_content ", this.emailContent)
			console.log("email_content ", typeof this.emailContent)
			let message = '';
			console.log("guideContext , ", !!this.isGuideContext);
			console.log("guideContexts , ", !!this.guideContext);
			if(!!this.isGuideContext){
				message = `/email_senden_guide{"email":\"${this.emailFrom}\", "email_content": \"${this.emailContent.replaceAll("\n", "<br>")}\"}`
			}else{
				message = `/email_senden{"email":\"${this.emailFrom}\", "email_content": \"${this.emailContent.replaceAll("\n", "<br>")}\"}`
			}
			// let message = `/email_senden{"email":\"${this.emailFrom}\", "email_content": \"${this.emailContent.replaceAll("\n", "")}\"}`
			console.log("asd ", this.isGuideContext);
			console.log("message = ", message);
	        this.sendMessageToBot(message);	
		},
		cancelForm(){
			let message = '';
			// console.log("guideContext , ", !!this.guideContext);
			if(!!this.isGuideContext){
				message = `/email_cancel_guide{"email":\"${this.emailFrom}\", "email_content" : \"${this.emailContent}\"}`
			}else{
				message = `/email_cancel{"email":\"${this.emailFrom}\", "email_content" : \"${this.emailContent}\"}`
			}
			// let message = `/email_cancel{"email":\"${this.emailFrom}\", "email_content" : \"${this.emailContent}\"}`
	        this.sendMessageToBot(message);		
		},
		sendContactFormToBot() {
			if (this.emailValid && this.contentValid) {
                let message = `Die Nutzer Email ist ${this.emailFrom} und seine Nachricht ist ${this.emailContent}`;
                this.$store.state.socket.emit('user_uttered',{message: message})
				this.$store.commit('toggleContactForm', false);
				this.$store.commit('setInputVisible', true);
			}
			if (!this.contentValid){
				this.errorMessage = "Nachricht nicht vollständig"
			}
			if (!this.emailValid){
				this.errorMessage = "E-Mail-Adresse nicht vollständig";
			}
			this.errorAnimation();
		},
		// cancelForm() {
        //     let message = `Cancel`;
        //     this.$store.state.socket.emit('user_uttered',{message: message})
		// 	this.$store.commit('toggleContactForm', false);
		// 	this.$store.commit('setInputVisible', true);
		// },
		errorAnimation() {
				$('.form-wrapper').css('animation', 'shake-anim 2s linear');
				setTimeout(()=> {
					console.log("end shaking");
					$('.form-wrapper').css('animation', '');
				}, 2000)
				
		}
	}
};
</script>


<style lang="scss" scoped>
#app .form-wrapper {
	margin-bottom: 15px;
	max-width: 520px;
	margin: auto;
	.email-form-el {
		background: transparent;
		font-size: 16px;
		color: white;
		& > .row {
			margin-top: 10px;
		}
		label {
			margin: 0 0 0 0;
			font-family: 'Univers Next Pro Regular';
			font-weight: normal;
		}
		.input-style-wrapper {
			margin: 10px 0;
			border: solid 1px #ffffff;
			border-radius: 0;
			line-height: 38px;
			-webkit-transition: all 0.5s ease;
			transition: all 0.5s ease;
			font-size: 16px;
			.input-style {
				display: inline-block;
				color: white;
				outline: none;
				width: 100%;
				background: none;
				border: none;

				&#email-content {
					width: 100% !important;
					display: block;
					height: 100%;
					line-height: 18px;
					padding-top: 10px;
					padding-bottom: 10px;
					min-height: 188px;
				}
			}
			::placeholder {
					color: grey;
				}
			&.email-content-wrapper {
				min-height: 188px;
			}
			
		}

		.submit-form-btn-wrapper {
			margin: auto;
			.form-button {
				background: none;
				display: inline-block;
				color: white;
				border: solid 1px white;
				text-decoration: none;
				font-size: 16px;
				-webkit-transition: all 0.25s ease;
				transition: all 0.25s ease;
				cursor: pointer;
				width: 38px;
				height: 38px;
				border-radius: 19px;
				margin: 10px;
				&:focus {
					background: gray;
				}
			}
		}
		.form-button:hover {
			opacity: 0.7;
		}
	}
	.small-message{
		font-size: 12px;
		color: red;
	}
}

::placeholder {
	color: white;
	font-family: 'Univers Next Pro Regular' !important;
	letter-spacing: -0.05rem;
}

input,
textarea {
	font-family: 'Univers Next Pro Regular' !important;
	letter-spacing: -0.05rem;
	resize: none;
}
</style>
