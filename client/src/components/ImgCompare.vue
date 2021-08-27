<template>
  <VueCompareImage
    leftImage= "compareObject.imgLeft"
    rightImage= compareObject.imgRight
    hover
  />
</template>

<script>
  import VueCompareImage from 'vue-compare-image';


export default {
  name: 'ImgCompare',
  components: { VueCompareImage },
  props: {
    compareObject: {
      type: Array
    }
  }
};
</script>


