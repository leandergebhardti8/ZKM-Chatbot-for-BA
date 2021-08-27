<template>
	<div class="intro-wrapper row">
		<div class="col-12 text-left float-left">
			<div class="incoming-dot float-left">
				<div style="
                    height: 9px; width: 9px; 
                    background: #70CDB2;
                    border-radius: 4.5px;">
				</div>
			</div>
            <div class="intro-content">
                <div
                    class="intro-image"
                    :class="{ expanded }"
                    @click="expanded = true">
                    <div class="intro-image-inner-wrapper">
                        <i
                            v-if="expanded"
                            class="close-button"
                        >
                            <svg
                                style="width:24px;height:24px"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    fill="#666666"
                                    d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"
                                />
                            </svg>
                        </i>
                        <i
                            v-else
                            class="expand-button"
                        >
                            <svg
                                style="width:24px;height:24px"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    fill="#FFF"
                                    d="M10,21V19H6.41L10.91,14.5L9.5,13.09L5,17.59V14H3V21H10M14.5,10.91L19,6.41V10H21V3H14V5H17.59L13.09,9.5L14.5,10.91Z"
                                />
                            </svg>
                        </i>
                        <img :src="this.img" alt="">
                        <p 
                        class="img-intro-subtitle"
                        v-if="expanded === true"
                        >
                        {{ this.subtitle }}
                        </p>
                    </div>
                </div>
                <div class="intro-text">
                    <p>{{ this.text }}</p>
                </div>
            </div>
        </div>
	</div>
</template>

<script>
/* Dependencies */
import { mapGetters } from "vuex";
/* Mixins */
import MessageHandlerMixin from "../mixins/MessageHandlerMixin";
export default {
    name: 'GuideIntro',
    inheritAttrs: false,
	mixins: [MessageHandlerMixin],
	props: [
        'intro',
    ],
    data (){
        return {
            expanded: false,
            closeButtonRef: null,
            text: this.intro.text,
            img: this.intro.img,
            subtitle: this.intro.subtitle,
        }
    },
    methods: {
    closeImage (event) {
      this.expanded = false
      event.stopPropagation()
    },
    freezeVp (e) {
      e.preventDefault()
    }
  },

  watch: {
    expanded (status) {
      this.$nextTick(() => {
        if (status) {
          this.cloned = this.$el.cloneNode(true)
          this.cloned = this.cloned.querySelector('.intro-image');
          this.closeButtonRef = this.cloned.querySelector('.close-button')
          this.closeButtonRef.addEventListener('click', this.closeImage)
          document.body.appendChild(this.cloned)
          document.body.style.overflow = 'hidden'
          this.cloned.addEventListener('touchmove', this.freezeVp, false);
          setTimeout(() => {
            this.cloned.style.opacity = 1
          }, 0)
        } else {
          this.cloned.style.opacity = 0
          this.cloned.removeEventListener('touchmove', this.freezeVp, false);
          setTimeout(() => {
            this.closeButtonRef.removeEventListener('click', this.closeImage)
            this.cloned.remove()
            this.cloned = null
            this.closeButtonRef = null
            document.body.style.overflow = 'auto'
          }, 250)
        }
      })
    }
  }
};
</script>

<style scoped lang="scss">
#app {
    .intro-wrapper {
        .incoming-dot {
            display: none;
            align-items: center;
            justify-content: center;
            height: 100%;
            width: 10px;
        }
        .intro-content {
            display: inline-block;
            width: 85%;
            -ms-flex-item-align: center;
            align-self: center;
            margin: 10px 0 10px 0;
            padding: 11px;
            border-top: 1px solid white;
			border-right: 1px solid white;
			border-bottom: 1px solid white;
			border-left: none;
            overflow: hidden;
            transition: 0.25s opacity;
            background: black;

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

            &:before {
                display: block;
                content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='10' viewBox='0 0 9.078 7.953'%3E%3Cpath id='Pfad_115' data-name='Pfad 115' d='M664.218,110.7h-7.693l7.187,6.987' transform='translate(-655.54 -110.305)' stroke='%23fff' stroke-linecap='round' stroke-width='0.8'/%3E%3C/svg%3E ");
                position: absolute;
                left: 5px;
                right: auto;
                top: 9px;
                bottom: auto;
                // border: 8px solid;
                // border-color: white transparent transparent transparent;
		    }

            &:after {
                content: '';
                position: absolute;
                width: 0;
                height: calc(100% - 35px);
                left: 15px;
                right: auto;
                top: 19px;
                bottom: auto;
                border-left: 1px solid white;
            }

            .intro-image {
                position: relative;
                margin-bottom: 1rem;
                &:hover {
                    cursor: zoom-in;
                    .expand-button {
                        opacity: 1;
                    }
                }
                &.expanded {
                    opacity: 1;
                    .close-button, .img-intro-subtitle {
                        display: none;
                    }
                }
                img {
                    width: 100%;
                }

                .expand-button {
                    position: absolute;
                    z-index: 999;
                    right: 0;
                    top: 0;
                    padding: 0px;
                    align-items: center;
                    justify-content: center;
                    padding: 3px;
                    opacity: 0;
                    transition: 0.2s opacity;
                    svg {
                        width: 20px;
                        height: 20px;
                        path {
                            fill: #FFF;
                        }
                    }
                }
            }
        }
    }
}
body {
    > .intro-image {
        &.expanded {
            position: fixed;
            z-index: 999999;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: black;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            opacity: 0;
            padding-bottom: 0 !important;
            cursor: default;
            .intro-image-inner-wrapper {
                width: auto;
                max-width: 80%;
                max-height: 80%;
                display: flex;
                flex-direction: column;
                img {
                    width: 100%;
                    height: 90%;
                    object-fit: contain;
                }
                .close-button {
                    position: fixed;
                    top: 10px;
                    right: 10px;
                    cursor: pointer;
                    svg {
                        fill: #FFF;
                        filter: drop-shadow(1px 1px 1px rgba(0,0,0,0.5));    
                        path {
                            fill: #FFF;
                        }
                    }
                }
                .img-intro-subtitle {
                    font-family: 'Univers Next Pro Regular';
                    color: white;
                    align-self: center;
                }
            }
        }
    }
}
@media (max-width: 497px) {
    body {
        > .intro-image {
            &.expanded {
                .intro-image-inner-wrapper {
                    margin: 20px;
                    max-width: 100%;
                    max-height: 100%;
                    height: 100%;
                    justify-content: center;
                    img {
                        height: auto;
                        max-width: 100%;
                    }
                    .img-intro-subtitle {
                        align-self: center;
                        margin: 1em 0em 1em 0em;
                    }
                }
            }
        }
    }
}
</style>
