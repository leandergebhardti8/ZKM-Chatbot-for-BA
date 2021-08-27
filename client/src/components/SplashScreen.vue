<template>
	<div class="splash-screen">
		<div class="splash-wrapper">
			<div class="upper-wrapper">
				<div class="avatar-wrapper text-center">
					<img
						class="avatar-img"
						src=""
					/>
				</div>
			</div>
			<div class="lower-wrapper">
				<div class="welcome-text text-center">
					<div class="heading">
						<h2>Hi, mein Name ist Data.</h2>
					</div>
					<div class="content">
						<p>
							Ich möchte dich heute durchs ZKM begleiten. <br/>
							Bist Du bereit?
						</p>
					</div>
				</div>
				<div class="start-btn-wrapper">
					<div class="text-center">
						<QuickReplies
							v-if="currentQuickReply"
							:quickReplies="currentQuickReply.quickReplies"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from 'vuex';
import QuickReplies from './QuickReplies.vue';

export default {
	name: 'SplashScreen',
	components: {
		QuickReplies
	},
	computed: {
		...mapGetters(['currentQuickReply'])
	}
};
</script>

<style lang="scss" scoped>

#app .splash-screen {
	height: 100%;
	width: 100%;
	z-index: 10000;
	display: flex;
	align-items: center;
	overflow-y: hidden;
	overflow-x: hidden;

	.splash-wrapper {
		height: 100%;
		width: 100%;
		position: absolute;

		.upper-wrapper {
			top: 0;
			width: 100%;
			height: 50%;
			position: absolute;
			display: flex;
			align-items: center;
			justify-content: center;
			flex-direction: column;
		}
		.lower-wrapper {
			bottom: 0;
			width: 100%;
			height: 50%;
			position: absolute;
			.welcome-text {
				max-width: 400px;
				position: relative;
				margin:auto;
				@media screen and (max-width: 768px) {
					max-width: 100%;
				}
				@media screen and (device-aspect-ratio: 2/3) {
					margin-top: 60px;
				}
				@media screen and (device-aspect-ratio: 2/3) {
					margin-top: 16px;
				}

				.heading {
					//font-family: 'Univers Next Pro Regular';
					//margin: 2rem 0 1rem 0;
					color: #fff;
					transition: 0s all ease-in-out;
				}
				.content {
					color: white;
					font-family: 'Univers Next Pro Regular';
					//line-height: 1.4;

					p{
						font-size:16px;
						line-height: 1.2;
					}
				}
			}

			.start-btn-wrapper {
				width: 100%;
				height: 50%;
				@media screen and (max-height: 568px) {
					& .quick-reply-single-wrapper {
						height: 40px;

						p {
							line-height: 42px;
						}
					}
				}
			}
		}
	}
}
</style>
