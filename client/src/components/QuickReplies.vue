<template>
	<div class="incoming-msg msg-div row">
		<div class="qr-container col-12">
			<!-- Multiple primary quick replies  -->
			<div class="quick-reply-stack">
				<div
					v-for="(reply, index) in quickReplies"
					:key="reply.title + index"
					class="quick-reply-single-wrapper"
					:class="(reply.active === false) ? 'not-selected': ''"
				>
					<div class="quick-reply">
						<div id="hide-me">
							<p
								v-if="reply.active"
								class="qr-title"
							>
								{{ reply.title }}
							</p>
							<p
								v-else
								class="qr-title"
								@click="handleAfterClick(reply, index)"
							>
								{{ reply.title }}
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from 'vuex';
import MessageHandlerMixin from '../mixins/MessageHandlerMixin';

export default {
	name: 'QuickReplies',
	mixins: [MessageHandlerMixin],
	props: {
		quickReplies: {
			type: Array,
			required: true
		}
	},
	computed: {
		...mapGetters(['currentQuickReply'])
	},
	methods: {
		handleAfterClick(reply, index) {
			let activeQuickReplies = []
			for(let item in this.quickReplies){
				if(item != index){
					activeQuickReplies.push({
						title: this.quickReplies[item].title,
						payload: this.quickReplies[item].payload,
						active: false
					})
				}else{
					activeQuickReplies.push({
						title: reply.title,
						payload: reply.payload,
						active: true
					})
				}
			}
			this.$store.commit("storeNewMessage", {
				format: "message",
				type: "out",
				text:reply.title,
				quickReplies: activeQuickReplies
			});
			this.sendQrPayloadToBot({
				text: reply.title,
				payload: reply.payload
			})
		}
	},
};
</script>

<style lang="scss" scoped>

#app .quick-reply-stack {
	font-family: 'Univers Next Pro Regular';
	letter-spacing: -0.05rem;
	box-sizing: border-box;
	animation: fade-in 0.5s ease;
	transition: all 0.25s ease;
	max-width: 90%;
	margin: auto;
	margin-top: 10px;
	border-radius: 0;

	.quick-reply-single-wrapper {
		text-align: center;
		margin: 15px 0 15px 0;
		border: solid 1px white;
		background: white;
		border-radius: 0;
		color: black;
		min-height: 38px;
		display: block;
		box-sizing: border-box;
		width: 100%;
		max-width: 100%;
		cursor: pointer;
		transition: 0.25s all ease-in-out;

		&:hover {
			opacity: 0.75;
			background: none;
			color: white;
		}

		p {
			line-height: 18.4px;
			font-stretch: expanded;
			font-size: 16px;
			font-weight: 600;
			margin: 0;
		}

		&.not-selected {
			opacity: 0.2;
			display:none;
		}

		.quick-reply {
			padding: 10px 15px;
		}
	}
}
</style>
