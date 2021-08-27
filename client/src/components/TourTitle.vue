<template>
        <div class="TourTitle">
            <small class="ubersicht-button">— Zur Übersicht</small>
            <div class="title">
                <h1>The Legible City</h1>
                <small>Jeffrey Shaw, 1988</small>
            </div>
        </div>
</template>

<script>
    export default {
        mounted () {
            console.log("Start Title");
        },
    }
</script>

<style lang="scss" scoped>
.TourTitle{
    width: 90%;
    height: 100%;
    background-image: url("https://www.jeffreyshawcompendium.com/wp-content/uploads/2015/03/js44w1989LegibCit1_k000_r.jpg");
    background-size: cover;
    background-position: center;
    filter: grayscale(100%); /* Current draft standard */
    -webkit-filter: grayscale(100%); /* New WebKit */
    -moz-filter: grayscale(100%);
    -ms-filter: grayscale(100%); 
    -o-filter: grayscale(100%); /* Not yet supported in Gecko, Opera or IE */
    filter: gray; /* IE */
    .ubersicht-button{
        margin-top: 80px;
        float: right;
    }
    .title{
        margin-top: 80px;
        float: left;
    }
}
</style>