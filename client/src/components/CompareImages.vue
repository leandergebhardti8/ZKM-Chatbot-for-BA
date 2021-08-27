<template>
	<div class="image-container">
		<div class="cocoen">
			<img class="slider-img" :src="img1" />
			<img class="slider-img" :src="img2" />
		</div>
		<div class="compare-image-button" @click="sendFinalImgToChatbot(sliderPercentage)">
			<div class="button-text">
				<p>Bestätigen</p>
			</div>
		</div>
	</div>
</template>

<script>
import MessageHandlerMixin from '../mixins/MessageHandlerMixin';
import { mapGetters } from 'vuex';
import Cocoen from 'cocoen';
import 'cocoen/dist/css/cocoen.min.css';

export default {
	name: 'CompareImages',
	components: {},
	mixins: [MessageHandlerMixin],
	data() {
		return {
			sliderPercentage: 50,
			darkerImageRatio: 0.55,
			img1: "https://zkm-chatbot.s3.eu-central-1.amazonaws.com/chatbot/assets/2020_chatbot_meme-002.png",
			img2: "https://zkm-chatbot.s3.eu-central-1.amazonaws.com/chatbot/assets/2020_chatbot_meme-001.png"
		};
	},
	watch: {
		// sliderPercentage: function(val) {
		// 	this.onSliderValueChange(val);
		// }
	},
	mounted() {
		const coco = new Cocoen(document.querySelector('.cocoen'));

		this.observeSlider();

		// if (this.getCurrentScreenObject.userChoice.sliderPercentage) {
		// 	this.sliderPercentage = this.getCurrentScreenObject.userChoice.sliderPercentage;
		// }
		// this.onSliderValueChange(this.sliderPercentage);

		const sliderDiv = document.getElementsByClassName('cocoen-drag')[0];
		const firstImageDiv = document.querySelector(
			'.cocoen > div:first-child, picture .cocoen > div'
		);

		sliderDiv.style.left = 100 - this.sliderPercentage + '%';
		firstImageDiv.style.width = 100 - this.sliderPercentage + '%';
	},
	methods: {
		observeSlider: function() {
			/* Select slider */
			const sliderDiv = document.getElementsByClassName('cocoen-drag')[0];
			/* Observer options (style tracking)*/
			const config = {
				attributes: true,
				attributeFilter: ['style']
			};

			/* Event callback definition */
			const onChangeCallback = mutations => {
				this.sliderPercentage = 100 - parseInt(mutations[0].target.style.left);
			};

			/* Start the observer */
			const observer = new MutationObserver(onChangeCallback);
			observer.observe(sliderDiv, config);
		},
		ConsoleLog(val){
			console.log(val);
		},
		sendFinalImgToChatbot(val) {
			let reply = {img: null, payload: '/affirm'};
			let image1 = {img: this.img1, payload: '/affirm'};
			let image2 = {img: this.img2, payload: '/affirm'};
			if (val === 50) {
			
			} else if (val < 50) {
				reply = image1;
			} else if (val > 50) {
				reply = image2;
			}
			// console.log(reply.img, reply.payload);
			this.sendTriggerToBot({
				img: reply.img,
				payload: reply.payload
			})
		}
	}
};
</script>

<style lang="scss" scoped>
#app {
	.image-container {
		max-width: 100%;

		.cocoen {
			.slider-img {
				transition: filter 0.55s ease;
				pointer-events: none;
			}
		}
	}
	.compare-image-button {
		font-family: 'Univers Next Pro Regular';
		letter-spacing: -0.05rem;
		box-sizing: border-box;
		animation: fade-in 0.5s ease;
		max-width: 90%;
		margin-top: 10px;
		text-align: center;
		margin: 15px auto;
		border: solid 1px white;
		background: white;
		color: black;
		min-height: 38px;
		display: block;
		box-sizing: border-box;
		cursor: pointer;
		transition: 0.25s all ease-in-out;

		&:hover {
			opacity: 0.75;
			background: none;
			color: white;
		}
		
		.button-text {
			padding: 10px 15px;
		}

		p {
			line-height: 18.4px;
			font-stretch: expanded;
			font-size: 16px;
			font-weight: 600;
			margin-bottom: 0px !important;
		}
	}
}
</style>
