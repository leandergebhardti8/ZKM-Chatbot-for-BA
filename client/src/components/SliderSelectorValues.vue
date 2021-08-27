<template>
	<div class="slider-wrapper">
		<vue-slider 
			ref="slider"
			v-model="value"
			:lazy="true"
			v-bind="slider_options">
			<template v-slot:tooltip="{ value }">
    			<div class="custom-tooltip">{{ value }}</div>
  			</template>
		</vue-slider>
	</div>
</template>

<script>
import VueSlider from 'vue-slider-component'
import MessageHandlerMixin from '../mixins/MessageHandlerMixin'

export default {
  props: [
	'values',
	'marks'
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
	  value: this.values.min,
      slider_options: {
        dotSize: 32,
        height: 42,
		min: this.values.min,
		max: this.values.max,
        interval: this.values.interval,
		disabled: false,
		tooltip: 'active',
		marks: this.marks,
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
			background: 'rgb(149,193,28)',
			background: 'rgb(255,255,255)'
		},
		processStyle: {
			background: 'rgb(0,18,74)',
			background: '#70CDB1'
		},
		labelStyle: {
			margin: '20px 0 0'
		}
      }
    }
  },
  methods: {
	  handleAfterDecision(val) {
			let reply = {title: `${val} ${this.values.unit}`, payload: '/falsch'};
			let correct = {title: `${val} ${this.values.unit}`, payload: '/richtig'};
			this.slider_options.disabled = true;
			console.log("selected ", val)
			switch (this.values.mode) {
				case 'exact':
					if(val == this.values.solution) {
						reply = correct;
						console.log("correct!");
					}
					break;
				case 'lower':
					if(val < this.values.solution) {
						reply = correct;
						console.log("correct!");
					}
					break;
				case 'bigger':
					if(val > this.values.solution) {
						reply = correct;
						console.log("correct!");
					}
					break;
				case 'between':
					if(val > this.values.solution_min && val < this.values.solution_max) {
						reply = correct;
						console.log("correct!");
					}
					break;
				case 'any':
					reply = correct;
					break;
			}
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
		margin: 3rem 3rem 3rem;
	}
	
	.custom-tooltip {
		padding: 4px;
		border-radius: 0.7rem;
		background: #FF53AF;
	}
/*	 		  _.--""`-..
            ,'          `.
          ,'          __  `.
         /|          " __   \
        , |           / |.   .
        |,'          !_.'|   |
      ,'             '   |   |
     /              |`--'|   |
    |                `---'   |
     .   ,                   |                       ,".
      ._     '           _'  |                    , ' \ `
  `.. `.`-...___,...---""    |       __,.        ,`"   L,|
  |, `- .`._        _,-,.'   .  __.-'-. /        .   ,    \
-:..     `. `-..--_.,.<       `"      / `.        `-/ |   .
  `,         """"'     `.              ,'         |   |  ',,
    `.      '            '            /          '    |'. |/
      `.   |              \       _,-'           |       ''
        `._'               \   '"\                .      |
           |                '     \                `._  ,'
           |                 '     \                 .'|
           |                 .      \                | |
           |                 |       L              ,' |
           `                 |       |             /   '
            \                |       |           ,'   /
          ,' \               |  _.._ ,-..___,..-'    ,'
         /     .             .      `!             ,j'
        /       `.          /        .           .'/
       .          `.       /         |        _.'.'
        `.          7`'---'          |------"'_.'
       _,.`,_     _'                ,''-----"'
   _,-_    '       `.     .'      ,\
   -" /`.         _,'     | _  _  _.|
    ""--'---"""""'        `' '! |! /
                            `" " -'  */
</style>
