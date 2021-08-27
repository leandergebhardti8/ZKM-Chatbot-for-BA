<template>
	<div class="incoming-msg msg-div row">
		<div class="col-12 text-left float-left">
			<div class="incoming-dot float-left">
				<div style="
				height: 9px; width: 9px; 
				background: #70CDB2;
				border-radius: 4.5px;">
				</div>
			</div>
			<div class="message-content float-left">
				<p>{{ message }}</p>
			</div>
		</div>
	</div>
</template>

<script>
/* Dependencies */
import { mapGetters } from "vuex";
/* Mixins */
import MessageHandlerMixin from "../mixins/MessageHandlerMixin";
import Three from "./Three";
export default {
	name: 'IncomingMessage',
	components: {
		Three
	},
	mixins: [MessageHandlerMixin],
	props: {
		message: {
			type: String,
			required: true
		}
	}
};
</script>

<style scoped lang="scss">
#app .incoming-msg {
	.message-content {
			display: inline-block;
			max-width: 85%;
			-ms-flex-item-align: center;
			align-self: center;
			margin: 10px 0 10px 0;
			padding: 11px;
			border-top: 1px solid white;
			border-right: 1px solid white;
			border-bottom: 1px solid white;
			border-left: none;

		p {
			display: inline-block;
			color: #ffffff;
			font-size: 16px;
			line-height: 20px;
			letter-spacing: -0.05rem;
			margin: 0;
			word-break: break-word;
			white-space: pre-wrap;       /* css-3 */
			white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
			white-space: -pre-wrap;      /* Opera 4-6 */
			white-space: -o-pre-wrap;    /* Opera 7 */
			word-wrap: break-word;       /* Internet Explorer 5.5+ */
		}
		:before {
			display: block;
			content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='10' viewBox='0 0 9.078 7.953'%3E%3Cpath id='Pfad_115' data-name='Pfad 115' d='M664.218,110.7h-7.693l7.187,6.987' transform='translate(-655.54 -110.305)' fill='none' stroke='%23fff' stroke-linecap='round' stroke-width='0.8'/%3E%3C/svg%3E ");
			position: absolute;
			left: 5px;
			right: auto;
			top: 6px;
			bottom: auto;
			// border: 8px solid;
			// border-color: white transparent transparent transparent;
		}

		:after {
			content: '';
			position: absolute;
			width: 0;
			height: calc(100% - 30px);
			left: 15px;
			right: auto;
			top: 19px;
			bottom: auto;
			border-left: 1px solid white;
		}
	}


	

	.incoming-dot {
		display: none;
		align-items: center;
  		justify-content: center;
		height: 100%;
		width: 10px;
	}
}
</style>
