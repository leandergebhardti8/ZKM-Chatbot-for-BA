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
							placeholder="Deine E-Mail Adresse"
						/>
					</div>
					<div v-if="!emailValid" class="col-12 small-message">
						Bitte gültige Email-Adresse eingeben
					</div>
					<!-- Message -->
					<div class="col-12 email-content-wrapper input-style-wrapper">
						<!-- <label style="display: block">Deine Nachricht an uns:</label> -->
						<textarea
							id="email-content"
							v-model="emailContent"
							class="input-style"
							placeholder="Deine Nachricht an uns"
						></textarea>
					</div>
					<div v-if="!contentValid" class="col-12 small-message">
						Schreiben Sie uns Ihre Anliegen
					</div>
					<!-- Submit/Cancel buttons -->
					<div class="row" style="margin-top:8px;">
						<div class="submit-form-btn-wrapper">
							<button id="submit-form" type="submit" class="form-button" :disabled="!emailValid || !contentValid">
								<font-awesome-icon :icon="['fa', 'play']"/>
							</button>
							<button id="cancel-form" type="reset" class="form-button">
								<font-awesome-icon :icon="['fa', 'times']"/>
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
import MessageHandlerMixin from '../mixins/MessageHandlerMixin';

export default {
	name: 'ContactForm',
	mixins: [MessageHandlerMixin],
	data() {
		return {
			emailFrom: this.userEmail ? this.userEmail : '',
			emailContent: '',
			emailValid: false,
			contentValid: false,
			firstname: '',
			lastname: '',
			isFirstNameValid: false,
			isLastNameValid: false,
			personalnummer: ''
		};
	},
	computed: {
		...mapGetters(['userEmail'])
	},
	watch: {
		emailFrom: function(val) {
			// if (validator.isEmail(val)) {
			// 	this.emailValid = true;
			// 	$('.email-from-wrapper').css('border-color', '#00a0f0');
			// } else this.emailValid = false;

			// if (/[A-Za-z0-9]{2,}(@)/gi.test(val)) {
			// 	this.emailValid = true;
			// } else {this.emailValid = false}
			// if (/<[a-z][\s\S]*>/gi.test(val)) {
			// 	this.emailValid = false;
			// }
			if (!validator.isEmail(val) || /<[a-z][\s\S]*>/gi.test(val)) {
				$('.email-from-wrapper').css('border-color', '#fbd143');
				return this.emailValid = false;
			} 
			$('.email-from-wrapper').css('border-color', '#143F94');
			this.emailValid = true
		},
		emailContent: function(val) {
			if (val.length < 5) {
				this.contentValid = false;
			} else {
				this.contentValid = true;
				$('.email-content-wrapper').css('border-color', '#00a0f0');
			}

			if (/<[a-z][\s\S]*>/gi.test(val)) {
				this.contentValid = false;
			}
		}
	},
	methods: {
		submitFormToBot() {
			if (this.emailValid && this.contentValid) {
				/* FALLBACK:
				Option1: Replace all "\n" with "<br>" so that NodeMailer html can format it correctly
				*** let htmlContent = this.emailContent.replace(/(?:\r\n|\r|\n)/g, "<br>"); ***
				Option2: Add style="white-space: pre-wrap;" to NodeMailer <p> tag
				*/
				// this.sendFormToBot({
				// 	emailFrom: this.emailFrom,
				// 	text: this.emailContent,
				// });
				let message = `/email_direkt_senden{"email":\"${this.emailFrom}\", "guide_title":"direkt", "email_content": \"${this.emailContent.replaceAll("\n", "<br>")}\"}`
			
				this.sendMessageToBot(message);
			}
			if (!this.emailValid) {
				$('.email-from-wrapper').css('border-color', 'red');
			}
			if (!this.contentValid) {
				$('.email-content-wrapper').css('border-color', 'red');
			}
		},
		cancelForm() {
			// this.sendFormToBot({
			// 	text: 'cancel'
			// });
			let message = `/email_direkt_cancel{"email":\"${this.emailFrom}\", "email_content" : \"${this.emailContent}\"}`
	        this.sendMessageToBot(message);	
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
