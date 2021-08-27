<template>
    <div class="swiper-card">
        <div class="card-instance">
            <div v-if="items.image_url" class="top-card"
                :style="{ backgroundImage: 'url(' + items.image_url + ')' }"
            ></div>
             <div v-else class="top-card"
                :style="{ backgroundImage: 'url(https://zkm-chatbot.s3.eu-central-1.amazonaws.com/chatbot/assets/zkm_placholder_wide.png)' }"
            ></div>
            <div class="bottom-card">
                <div class="bottom-header">
                    <h1>{{items.title? items.title : items.name }}</h1>
                </div>
                <div
                    class="nav-element"
                    @click="
                    sendTriggerToBot({
                        text: 'Rundgang starten',
                        payload: 'Starte Tour',
                    })
                    "
                >
                    <p class="menu-item">Rundgang starten</p>
                </div>
                <div
                    class="nav-element"
                    @click="switchToGuideMenu"
                >
                    <p class="menu-item">Karte: Guides 🗺️</p>
                </div>
                <!-- <p>{{items.text}}</p> -->
            </div>
        </div>
    </div>
</template>

<script>
import MessageHandlerMixin from "../mixins/MessageHandlerMixin";

    export default {
        data() {
            return {}
        },
        mixins: [MessageHandlerMixin],
        props: {
		items: {
			type: Object,
            default: () => {}
		}
	},
        methods: {
            toGermanDate: function(date){
                if (!date) return "";
                const dateObj = new Date(date);
                return dateObj.toLocaleDateString("de-De");
            },
            switchToGuideMenu: function(event) {
                this.$emit('clicked','open werk menu'),
                this.sendTriggerToBot({
                    text: '',
                    payload: 'get_guide_info',
                })
            }
        }
    }
</script>

<style lang="scss" scoped>
#app {
    .swiper-card {
        width: 100%;
        height: 100%;
        .nav-element {
        width: 100%;
        text-align: center;
        margin: 5px 0 5px 0;
        border: solid 1px white;
        border-radius: 0;
        color: white;
        height: 38px;
        display: block;
        box-sizing: border-box;
            .menu-item {
                font-size: 14px;
                line-height: 38px;
                color: white;
                display: inline;
                margin: 0 0 0 0;
                transition: all 0.25s ease;
                cursor: pointer;
                &:hover {
                opacity: 0.5;
                }
            }
        }
        .card-instance {
            max-width: 300px;
            max-height: 350px;
            height: 100%;
            margin: auto;
            background: rgba(0, 0, 0, 0.7);
            // border-radius: 10px;
            .top-card {
                // border-radius: 10px 10px 0 0;
                // filter: grayscale(100%); /* Current draft standard */
                // -webkit-filter: grayscale(100%); /* New WebKit */
                // -moz-filter: grayscale(100%);
                // -ms-filter: grayscale(100%); 
                // -o-filter: grayscale(100%); /* Not yet supported in Gecko, Opera or IE */
                // filter: gray; /* IE */
                // -webkit-filter: grayscale(1); /* Old WebKit */
                height: 45%;
                background-position: center;
                background-size: cover;
            }
            .bottom-card {
                height: 50%;
                border-left: 2px solid #70ceb2;
                padding: 20px 20px 10px;
                position: relative;
                h1 {
                    font-size: 16px;
                    margin-bottom: 5px;
                    height: 30px;
                }
                small {
                    font-size: 10px;
                    line-height: 1;
                }
                // p {
                //     height: 25px;
                //     margin-top: 5px;
                //     margin-bottom: 0;
                //     overflow: hidden;
                //     color: #A3A3A3;
                //     font-size: 11px;
                // }
                .bottom-header{
                    padding-bottom: 5px;
                }
                a {
                    color:white;
                }
                .play-button {
                    background: none;
                    display: none;
                    color: white;
                    border: solid 1px white;
                    text-decoration: none;
                    font-size: 16px;
                    -webkit-transition: all 0.25s ease;
                    transition: all 0.25s ease;
                    cursor: pointer;
                    width: 38px;
                    height: 38px;
                    border-radius: 19px;
                    margin: 10px;
                    position: absolute;
                    right: 10px;
                    top: 10px;
                    &:focus {
                        background: gray;
                    }
                }
                .play-button:hover {
                    opacity: 0.7;
                }
            }
        }
    }
}
</style>