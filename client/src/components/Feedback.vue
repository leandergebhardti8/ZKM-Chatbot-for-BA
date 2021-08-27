<template>
	<div class="col-12 feedback-row">
                <span>{{feedbackData.text}}</span>
				<span
					v-for="(reply, index) in feedbackData.buttons"
					:key="reply.title + index"
					class="feedback-link"
					:class="(reply.active === false) ? 'not-selected': ''"
				>
							<span
								v-if="reply.active"
								class=""
							>
								{{ reply.title }}
							</span>
							<span
								v-else
								class=""
								@click="handleAfterClick(reply, index)"
							>
								{{ reply.title }}
							</span>
				</span>
	</div>
</template>

<script>
import MessageHandlerMixin from '../mixins/MessageHandlerMixin';

export default {
    name: "Feedback",
    mixins: [MessageHandlerMixin],
    props: {
        feedbackData: {
            type: Object,
            default() {
                return {
                text: "",
                buttons: [{title: "", payload: ""}]
                }
            }
        }
    },
    	methods: {
		handleAfterClick(reply) {
			this.$store.commit("storeNewMessage", {
				format: "message",
				type: "out",
				text: reply.title
			});
			this.sendQrPayloadToBot({
				text: reply.title,
				payload: reply.payload
            })
            this.$store.commit("setFeedback", undefined);
		}
	},
}
</script>

<style lang="scss" scoped>
#app .feedback-row {
	font-family: 'Univers Next Pro Regular';
	font-size:12px;
	box-sizing: border-box;
	animation: fade-in 0.5s ease;
	transition: all 0.25s ease;
	background: none;
	color: white;
	// margin-top: -15px;

	.feedback-link {
		text-decoration:underline;
		padding:0 3px;
	}
}
</style>