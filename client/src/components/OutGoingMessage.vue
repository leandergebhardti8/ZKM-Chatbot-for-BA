<template>
	<div class="outgoing-msg msg-div row">
		<div class="col-10 offset-2 float-right">
			<div class="outgoing-dot float-right">
				<div style="height: 9px; width: 9px; background-color: #ffffff99; border-radius: 4.5px;"></div>
			</div>
			<div class="message-content float-right">
				<p style="float: right;">{{ message }}</p>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'OutgoingMessage',
	props: {
		message: {
			type: String,
			required: true
		}
	}
};
</script>

<style scoped lang="scss">

#app .outgoing-msg {
	.outgoing-dot {
		display: none;
		align-items: center;
  		justify-content: center;
		height: 100%;
	}
	.message-content {
			display: inline-block;
			-ms-flex-item-align: center;
			align-self: center;
			margin: 10px 0 10px 0;
			padding: 11px;
			border-top: 1px solid white;
			border-right: none;
			border-bottom: 1px solid white;
			border-left: 1px solid white;
		p {
			color: white;
			display: inline-block;
			width: 100%;
			font-size: 16px;
			line-height: 20px;
			letter-spacing: -0.05rem;
			margin: 0;
			text-align: right;
			word-break: break-word;
			white-space: pre-wrap;       /* css-3 */
			white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
			white-space: -pre-wrap;      /* Opera 4-6 */
			white-space: -o-pre-wrap;    /* Opera 7 */
			word-wrap: break-word;       /* Internet Explorer 5.5+ */
		}
		:before {
			display: block;
			content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='10' viewBox='0 0 9.078 7.953'%3E%3Cpath id='Pfad_115' data-name='Pfad 115' d='M656.525,110.7h7.693l-7.187,6.987' transform='translate(-656.125 -110.305)' fill='none' stroke='%23fff' stroke-linecap='round' stroke-width='0.8'/%3E%3C/svg%3E ");
			position: absolute;
			right: 5px;
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
			right: 15px;
			top: 19px;
			bottom: auto;
			border-right: 1px solid white;
		}
	}
}
</style>
