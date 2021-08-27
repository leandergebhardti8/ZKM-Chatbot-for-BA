<template>
    <div class="quote-wrapper">
        <div class="quote-container">
            <div class="quote-card">
                <img v-if="imageSource!=''" class="quote-image" :src="imageSource" />
                <p 
                    class="img-quote-subtitle"
                    
                >
                    {{ this.subtitle }}
                </p>
                <div class="quote-details">
                    <p class="quote-text"><i class="fas fa-quote-left"></i><br>{{ quotetext }}</p>
                    <p class="quote-author">{{ author }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import MessageHandlerMixin from '../mixins/MessageHandlerMixin'

export default {
  props: [
      'quote'
  ],
  mixins: [MessageHandlerMixin],
  components: {

  },
  data () {
    return {
        imageSource: this.quote.quoteimage,
        author: this.quote.author == ""? "" : this.quote.author,
        quotetext: this.quote.quotetext,
        subtitle: this.quote.subtitle,
    }
  }
}
</script>

<style lang="scss" scoped>
    #app {
        $text: rgb(255, 255, 255);
        $black: #121212;
        $white: rgba(248, 243, 230, 0.308);
        $border: #ebebeb;
        $shadow: rgba(0, 0, 0, 0.2);

        @mixin transition($args...) {
            transition: $args;
        }

        * {
        box-sizing: border-box;
            &::before, &::after {
                box-sizing: border-box;
            }
        }

        .quote-container {
            max-width: 100%;
        }

        .quote-wrapper {
            display: flex;
            float: left;
            color: $text;
            text-rendering: optimizeLegibility;
            font-family: "Helvetica Neue", sans-serif;
            font-weight: 800;
            max-width: 100%;
            height: auto;
            margin: 10px 0;
            align-items: center;
            justify-content: left;
            background-color: black;
        }

        .quote-card {
            display: flex;
            flex-direction: row;
            // box-shadow: 0 0.1875rem 1.5rem $shadow;
            border: 1px solid white;
            overflow: hidden;
            .img-quote-subtitle {
                font-size: 10px;
                line-height: 1.2em;
                margin: 1px 7px 0;
                word-break: break-word;
            }
        }

        .quote-image {
            display: block;
            width: 100%;
            max-height: 15vw;
            object-fit: cover;
            @media screen and (max-width: 768px) {
					max-height: 80vw;
            }
        }



        .quote-details {
            padding: 11px;
        }

        .quote-text {
            font-size: 18px;
            line-height: 24px;
        }

        p.quote-author {
            text-transform: uppercase;
            margin: 0 0 0.75rem;
            font-size: 15px;
            color: #919191;
            font-weight: bold;
        }

        .quote-card {
            flex-wrap: wrap;
        }
    }
</style>