<template>
    <div class="swiper-card">
        <div class="card-instance" @click="openLinkInNewWindow(items.link)">
            <div v-if="items.image_url" class="top-card"
                :style="{ backgroundImage: 'url(' + items.image_url + ')' }"
            ></div>
             <div v-else class="top-card"
                :style="{ backgroundImage: 'url(https://zkm-chatbot.s3.eu-central-1.amazonaws.com/chatbot/assets/zkm_placholder_wide.png)' }"
            ></div>
            <div class="bottom-card">
                <div class="bottom-header">
                    <h1 v-if="items.creator_name">Künstler/in / Künstlergruppe</h1>
                    <h2 v-if="items.creator_name">{{items.creator_name}}</h2>
                    <h1>Titel</h1>
                    <h2>{{items.title? items.title : items.name }}</h2>
                    <h1 v-if="items.creation_date">Jahr</h1>
                    <h2>{{items.creation_date}}</h2>
                    <small>{{items.subtitle}}</small>
                </div>
                <p v-if="items.date"><small>{{toGermanDate(items.date.start)}} bis {{toGermanDate(items.date.end)}}</small></p>
                <!-- <a v-bind:href="items.link" target="_blank"> Mehr Infos </a> -->
                <!-- <p>{{items.text}}</p> -->
            </div>
        </div>
    </div>
</template>

<script>
//TODO change background image url from static to dynamic
    export default {
        data() {
            return {}
        },
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
            openLinkInNewWindow: function(href){
                window.open(href, "_blank");
            }
        }
    }
</script>

<style lang="scss" scoped>
#app {
    .swiper-card {
        width: 100%;
        height: 100%;
        .card-instance {
            max-width: 300px;
            height: 100%;
            margin: auto;
            &:hover{
                filter: opacity(65%);
            }
            .top-card {
                // border-radius: 10px 10px 0 0;
                // filter: grayscale(100%); /* Current draft standard */
                // -webkit-filter: grayscale(100%); /* New WebKit */
                // -moz-filter: grayscale(100%);
                // -ms-filter: grayscale(100%); 
                // -o-filter: grayscale(100%); /* Not yet supported in Gecko, Opera or IE */
                // filter: gray; /* IE */
                // -webkit-filter: grayscale(1); /* Old WebKit */
                height: 50%;
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
                    // height:25px;
                    font-weight: 600;
                }
                h2{
                    font-size: 17px;
                } 
                small {
                    font-size: 10px;
                    line-height: 1;
                }
                p {
                    height: 25px;
                    margin-top: 5px;
                    margin-bottom: 0;
                    overflow: hidden;
                    color: #A3A3A3;
                    font-size: 11px;
                }

                .bottom-header{
                    height:120px;
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