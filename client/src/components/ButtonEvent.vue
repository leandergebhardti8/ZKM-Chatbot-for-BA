<template>
	<div class="incoming-msg msg-div row text-center">
		<div class="col-12">
			<div
				class="buttons-wrapper"
			>
				<div
				v-for="(button, index) in buttons"
				:key="button.title + index" 
				class="button-event row">
				<a
					v-if="button.content_type === 'link'"
					class="button-link col-12"
					:href="button.payload"
					target="”_blank”"
					>
					<div class="button-desc-wrapper">
						<p class="button-title">{{button.title}}</p>
						<p class="button-description">{{button.description}}</p>
					</div>
					<img src="../assets/icons/link-out.svg">
				</a>
				<a
					v-if="button.content_type === 'email'"
					class="button-link col-12"
					:href="'mailto:' + button.payload"
					>
					<div class="button-desc-wrapper">
						<p class="button-title">{{button.title}}</p>
						<p class="button-description">{{button.description}}</p>
					</div>
					<img src="../assets/icons/zkm_email_icon.svg">				
				</a>
				<a
					v-if="button.content_type === 'phone'"
					class="button-link col-12"
					:href="'tel:' + button.payload"
					>
					<div class="button-desc-wrapper">
						<p class="button-title">{{button.title}}</p>
						<p class="button-description">{{button.description}}</p>
					</div>
					<img src="../assets/icons/zkm_phone_icon.svg">
				</a>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'ButtonEvent',
	props: {
		buttons: {
			type: Array,
			required: true
		}
	},
	mounted() {},
	methods: {
	}
};
</script>

<style lang="scss" scoped>
$thyOrange: #ffb400;
$thyBlue: #00a0f0;

#app .incoming-msg {
	padding: 10px 0;
	.buttons-wrapper {
		font-family: 'Univers Next Pro Regular';
		box-sizing: border-box;
		animation: fade-in 0.5s ease;
		padding: 0 15px;
		background: transparent;
		height: 100%;
		display: block;
		box-sizing: border-box;
		cursor: pointer;
		transition: 0.25s all ease-in;
		border-radius: 0;
		max-width:250px;

	.button-event {
		padding:15px 10px;
		border: 1px solid white;
		background-color: rgba(255, 83, 175, 0.8);
		background: linear-gradient(125deg, rgba(255, 83, 175, 0.8) 36%, rgba(105,67,163,1) 100%);
		a {
			color: white;
			display: flex;
			justify-content: space-between;
			img {
				width: 30px;
				height: 30px;
				margin-top: auto;
				margin-bottom: auto;
			}
		}
		&:hover {
			filter: brightness(75%);
		}
	}

	.button-title {
		font-size:16px;
		font-weight:800;
		line-height:1.2;
		margin-bottom: .5rem;
	}
	.button-description {
		margin-bottom: 0;
		margin-right: 20px;
	}

	.button-desc-wrapper{
		text-align:left;
	}

		.button-link {
			transition: all 0.25s ease-in-out;

			&:hover {
				color: black;
			}

			#doc-image {
				max-width: 100px;
			}
		}
	}
}
</style>
