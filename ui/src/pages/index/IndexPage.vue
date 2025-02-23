<template>
  <q-page class="">
    <div class="content-text">
      <!--トップメッセージ-->
      <div class="top-message-box">
        <div class="main-content">
          <div>
            <hr />
            <div>なんでもありのホロライブ非公式サイト！</div>
            <div>いろんなコンテンツをまとめました</div>
            <div class="text-right link">APIのドキュメントはこちら</div>
            <hr />
          </div>
          <div></div>
        </div>
      </div>

      <!--New!-->
      <div class="q-mt-md">
        <div class="sub-title" @click="onClickNewFanart">
          <span class="cursor-pointer">New!<q-tooltip> 再取得する </q-tooltip></span>

          <q-spinner v-if="newFanartLoading" />
        </div>
        <div class="q-ml-md" v-if="!newFanartLoading">
          <div class="new-fanart">
            <div
              v-for="item in pageNewFanart"
              :key="item.tweet.id"
              style="margin-bottom: 32px; margin-right: 32px"
            >
              <tweet-card :state="item" class="tweet-card" />
            </div>
          </div>

          <div style="display: flex; justify-content: center; align-items: center">
            <q-pagination v-model="newFanartPage" :max="4" />
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useIndexModel } from './useIndexModels';
import TweetCard from 'src/components/twitter/TweetCard.vue';

export default defineComponent({
  name: 'index-page',
  components: {
    TweetCard,
  },
  setup() {
    const {
      newFanartLoading,
      newFanartPage,
      newFanartState,
      topFanartState,
      pageNewFanart,
      getNewFanart,
    } = useIndexModel();

    const onClickNewFanart = function () {
      void getNewFanart();
    };
    return {
      newFanartLoading,
      newFanartPage,
      newFanartState,
      topFanartState,
      pageNewFanart,
      onClickNewFanart,
    };
  },
});
</script>
<style>
.content-text {
  font-size: 20px;
  color: #063f5c;
  .link {
    font-weight: 700;
    font-size: 0.7em;
    cursor: pointer;
  }
  .link:hover {
    transition: 0.3s;
    color: rgb(178, 222, 224);
  }
  .top-message-box {
    margin: 0 auto;
    max-width: 400px;
  }
  .sub-title {
    font-size: 1.5em;
    font-weight: 600;
    color: rgb(178, 222, 224);
  }
  .new-fanart {
    display: flex;
    flex-wrap: wrap;
  }
  .tweet-card {
    max-width: 300px;
    width: 100%;
    max-height: 300px;
    height: 100%;
  }
}
@media (max-width: 500px) {
  .content-text {
    font-size: 16px;
    .link {
      font-size: 0.9em;
    }
  }
}
@media (max-width: 750px) {
  .content-text {
    .tweet-card {
      max-width: calc(100vw - 32px);
      max-height: 700px;
    }
  }
}
</style>
