<template>
	<div class="slider-wrapper">
		<vue-slider 
		v-if="Object.keys(this.options).length <= 3"
		v-model="value"
		:lazy="true"
		v-bind="{...slider_options, tooltip: 'none'}"
		/>
		<vue-slider 
			v-if="Object.keys(this.options).length > 3"
			v-model="value"
			:lazy="true"
			v-bind="{...slider_options, tooltip: 'active'}" >
			       <template v-slot:tooltip="{ value, focus }">
        <div :class="['custom-tooltip', { focus }]">{{options[value].title }}</div>
      </template>
		</vue-slider>
	</div>
</template>

<script>
import VueSlider from 'vue-slider-component'
import MessageHandlerMixin from '../mixins/MessageHandlerMixin'

export default {
  props: [
    'options'
  ],
  mixins: [MessageHandlerMixin],
  components: {
    VueSlider
  },
  watch: {
	  value: function(val) {
		this.handleAfterDecision(val);
	}
  },
  data () {
    return {
	  value: `${(Object.keys(this.options).length - 1) / 2}`,
      slider_options: {
        dotSize: 32,
		height: 42,
		min: 0,
		max: Object.keys(this.options).length - 1,
		marks: this.options,
		disabled: false,
		dotStyle: {
			background: '#FF53AF'
		},
		tooltipStyle: {
			background: '#FF53AF'
		},
        sliderStyle: {
			background: '#fff',
			'box-shadow': 'rgba(0, 0, 0, 0.1) 0px 8px 8px'
		},
		railStyle: {
			background: 'rgb(255,255,255)',
			// background: 'linear-gradient(90deg, rgba(0, 18, 74, 1) 0%, rgba(112, 205, 177, 1) 100%)'
		},
		processStyle: {
			background: '#70CDB1',
			// background: 'rgb(0,18,74)',
			// background: 'linear-gradient(90deg, rgba(112, 205, 177, 1) 0%, rgba(0, 18, 74, 1) 100%)'
		},
		labelStyle: {
			margin: '20px 0 0'
		}
      }
    }
  },
  methods: {
	  handleAfterDecision(val) {
			const reply = this.options[val];
			this.slider_options.disabled = true;
			this.sendTriggerToBot({
				text: reply.title,
				payload: reply.payload
			})
		}
  }
}
</script>

<style scoped>
	.slider-wrapper {
		margin: 1rem 4rem 3rem;
	}
	.vue-slider-mark {
		max-width: 10px;
	}
</style>