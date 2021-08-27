<template>
  <div class="modal-wrapper">
    <transition name="modal">
      <div v-if="isOpen" class="modal-inner-wrapper">
        <div 
          class="overlay" 
          @click="isOpen = false"
          :class="{isOpen}"
          >
          <div class="modal-box">
            <i
              v-if="isOpen"
              class="close-button"
              @click="isOpen = false"
            >
              <svg
                style="width:24px;height:24px"
                viewBox="0 0 24 24"
              >
                <path
                  fill="#FFFFFF"
                  d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"
                />
              </svg>
            </i>
            <h1>{{modalTitle}}</h1>
            <img class="modal-img" :src="modalImg">
            <p class="modal-subtitle">{{ subtitle }}</p>
            <p>{{ modalText }}</p>
          </div>
        </div>
      </div>
    </transition>
    <div class="modal-button">
      <p v-if="modalTitle != 'Ukiyo-E'" @click="isOpen = !isOpen;">
        {{ isOpen ?"Pop-up schließen" : "Wer ist " + modalTitle + "?"}}
      </p>
      <p v-else-if="modalTitle === 'Ukiyo-E'" @click="isOpen = !isOpen;">
        {{ isOpen ?"Pop-up schließen" : "Was ist " + modalTitle + "?"}}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Modal",
  props: ['modalText', 'modal'],
  data: function() {
    return {
      isOpen: false,
      expanded: true,
      subtitle: this.modal.subtitle,
      modalImg: this.modal.img,
      modalTitle: this.modal.title,
    };
  }
};
</script>

<style lang="scss" scoped>
#app {
  .modal-wrapper {
    height: 100%;
    position: relative;
    width: 100%;
    overflow: auto;
  }
   .modal-inner-wrapper {
      position: fixed;
      right: 30px;
      bottom: 90px;
      height: 769px;
      max-height: 78%;
      width: 375px;
      z-index: 1;

      .overlay {
          // position: fixed;
          // top: 0;
          // left: 0;
          display: flex;
          justify-content: center;
          align-items: center;
          width: 100%;
          height: 100%;
          background: #00000094;
          z-index: 999;
          transition: all 1s ease;
          padding: 0 5%;

          .isOpen {
            .avatar-container {
              height: 112px;
            }
          }

      .modal-box {
          width: 100%;
          max-width: 480px;
          height: auto;
          max-height: 100vh;
          margin: auto;
          padding: 20px;
          background-color: black;
          border-radius: 0;
          transition: all 0.2s ease-in;
          border: 1px solid white;
          z-index: 7 !important;

          @media screen and (device-aspect-ratio: 40/71), (device-aspect-ratio: 375/667), (device-aspect-ratio: 9/16) {
            margin-top: 9.25rem; 
            max-height: 70.5vh;
            overflow: auto;
          }

        h1 {
          font-size: 1.5rem;
          text-transform:uppercase;
        }

        p {
          word-break: break-word;
          white-space: pre-wrap;
        }
        
        .modal-img {
          position: relative;
          max-height: 30vh;
          max-width: 300px;
          margin-bottom: 5px;
        }

        .modal-subtitle {
          font-size: 8px;
          word-break: break-word;
          line-height: 10px;
        }

        .close-button {
          float: right;
          cursor: pointer;
        }
        }
      }
    }

  .fadeIn-enter {
    opacity: 0;
    transition: all 1s step-end;
  }

  .fadeIn-leave-active {
    opacity: 0;
    transition: all 1s step-end;
  }

  .fadeIn-enter .modal,
  .fadeIn-leave-active.modal {
    transform: scale(1.1);
  }
  
  .modal-button {
		display: block;
    width: 90%;
    height: 40px;
		max-width: 100%;
		min-height: 38px;
    padding: 10px 15px;
    margin: 0px auto 5px;
    background-color: rgba(56, 101, 88, 0.8);
    color: white;
    text-align: center;
    font-family: 'Univers Next Pro Regular';
    letter-spacing: -0.05rem;
    box-sizing: border-box;
    animation: fade-in 0.5s ease;
    transition: all 0.25s ease;
		border-radius: 0;
		box-sizing: border-box;
		cursor: pointer;
    transition: 0.25s all ease-in-out;
    
		&:hover {
      background-color: rgba(58, 143, 119, 0.8);
		}

		p {
			line-height: 18.4px;
      font-stretch: expanded;
      font-size: 16px;
      font-weight: 400;
      margin: 0;
		}
  }

  @media (max-width: 576px) {
    .modal-wrapper {
      .modal-inner-wrapper {
        right: 0;
        bottom: 0;
        height: 100%;
        max-height: 100%;
        width: 100%;
      }
    }
  }
}
</style>