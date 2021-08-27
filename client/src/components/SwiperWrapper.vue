<template>
    <div id="swiper-wrapper">
        <swiper v-if="!menu" :options="swiperOption" ref="mySwiper">
            <!-- slides -->
                <swiper-slide v-for="(item, index) of items" :key="index"><SwiperCard :items="item"/></swiper-slide>
            <!-- Optional controls -->
            <!-- <div class="swiper-pagination"  slot="pagination"></div>
            <div class="swiper-button-prev" slot="button-prev"></div>
            <div class="swiper-button-next" slot="button-next"></div> -->
        </swiper>
        <swiper v-if="menu" :options="swiperOption" ref="mySwiper">
            <swiper-slide v-for="(item, index) of items" :key="index"><SwiperCardMainMenu :items="item" @clicked="switchToGuideMenu"/></swiper-slide>
        </swiper>
    </div>
</template>

<script>
import 'swiper/dist/css/swiper.css'
import { swiper, swiperSlide } from 'vue-awesome-swiper'
import SwiperCard from './SwiperCard'
import SwiperCardMainMenu from './SwiperCardMainMenu'

import Swiper from 'swiper'
    export default {
        data() {
            return {
                swiperOption: {
                    slidesPerView: 'auto',
                    spaceBetween: 10,
                    centeredSlides: true,
                    pagination: {
                        el: '.swiper-pagination',
                        clickable: true
                    },
                    navigation: {
                        nextEl: '.swiper-button-next',
                        prevEl: '.swiper-button-prev'
                    }
                },
                card: {
                    bgUrl: 'https://upload.wikimedia.org/wikipedia/commons/4/42/Andy_Warhol_1975.jpg',
                    title: 'Andy Warhol, NY 1983',
                    subTitle: 'Gottfried Helnwein, 1983',
                    text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                }
            }
        },
        components: {
            swiper,
            swiperSlide,
            SwiperCard,
            SwiperCardMainMenu,
        },
        props: {
            items: {
                type: Array,
                required: true
            },
            menu: {
                type: Boolean,
                required: false
            }
        },
        methods: {
            switchToGuideMenu(){
                this.$emit('clicked','open werk menu')
            }
        }
        
    }
</script>

<style lang="scss" scoped>
#app #swiper-wrapper{
    width: 100%;
    height: 350px;
    margin: auto;
    .swiper-slide {
        width:50%;
        min-width: 250px;
        height: 350px;
    }
}

</style>