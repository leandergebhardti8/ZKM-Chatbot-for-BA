<template>
    <div class="video-wrapper row">
		<div class="col-12 text-left float-left">
            <div class="video-content float-left"> 
                <div class="video float-left">
                    <video 
                        type="video/mp4"
                        ref="video"
                        controls preload="auto" autoplay=true
                        class="video-js col-12"
                        :src="videoObject" 
                    />
                </div>
                <div>
                    <p>{{ subtitle }}</p>
                </div>
            </div>
		</div>
	</div>
</template>

<script>
import videojs from 'video.js';
import 'video.js/dist/video-js.css'
import MessageHandlerMixin from "../mixins/MessageHandlerMixin";

export default {
	name: "VideoPlayer",
    mixins: [MessageHandlerMixin],
    computed: {
        videoStop() {
            return this.$store.getters.videoInterrupt
        }
    },
    props: [
        'videoObject',
        'videoSubtitle'
    ],
    watch: {
        videoStop(){
            let video = this.$refs['video'].pause();
            if(this.videoInterrupt){
                video.stop();
            }
        }
    },
    data() {
        return {
            subtitle: this.videoSubtitle == ""? "" : this.videoSubtitle,
        }
    }, 
};
</script>

<style lang="scss" scoped>
#app .video-wrapper {
	.video-content {
        display: inline-block;
        width: 100%;
        -ms-flex-item-align: center;
        align-self: center;
        margin: 10px 0 10px 0;
        border: 1px solid white;

        .video-js {
            height: auto;
        }

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
	}
}
</style>