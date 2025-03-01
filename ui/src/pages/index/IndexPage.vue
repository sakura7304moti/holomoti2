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

      <!--Hot!-->
      <div class="q-mt-md" style="margin-bottom: 48px">
        <div class="hot-subtitle sub-title" @click="onClickTopFanart">
          <span class="cursor-pointer">Hot!<q-tooltip> 再取得する </q-tooltip></span>

          <q-spinner v-if="topFanartLoading" />
        </div>
        <div :class="{ fadeRight: !topFanartLoading }">
          <div class="fanart-base hot-fanart">
            <div v-for="us in topFanartState.users" :key="us.userId">
              <user-icon :state="us" class="q-mb-xs" />
              <div class="row q-gutter-md wrap q-ml-md q-mb-md">
                <div
                  v-for="item in topFanartState.records.filter((it) => it.user.userId == us.userId)"
                  :key="item.tweet.id"
                >
                  <tweet-card :state="item" class="tweet-card" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!--New!-->
      <div>
        <div class="new-subtitle sub-title" @click="onClickNewFanart">
          <span class="cursor-pointer">New!<q-tooltip> 再取得する </q-tooltip></span>

          <q-spinner v-if="newFanartLoading" />
        </div>
        <div :class="{ fadeRight: !newFanartLoading }">
          <div class="fanart-base new-fanart">
            <div
              v-for="item in newFanartState.records"
              :key="item.tweet.id"
              style="margin-bottom: 32px; margin-right: 32px"
            >
              <tweet-card :state="item" class="tweet-card" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useIndexModel } from 'src/pages/index/useIndexModels';
import TweetCard from 'src/components/twitter/TweetCard.vue';
import UserIcon from 'src/components/twitter/UserIcon.vue';

export default defineComponent({
  name: 'index-page',
  components: {
    TweetCard,
    UserIcon,
  },
  setup() {
    const {
      newFanartLoading,
      topFanartLoading,
      newFanartPage,
      newFanartState,
      topFanartState,
      getNewFanart,
      getTopFanart,
    } = useIndexModel();

    const onClickNewFanart = function () {
      void getNewFanart();
    };

    const onClickTopFanart = function () {
      void getTopFanart();
    };
    return {
      newFanartLoading,
      topFanartLoading,
      newFanartPage,
      newFanartState,
      topFanartState,
      onClickNewFanart,
      onClickTopFanart,
    };
  },
});
</script>
<style>
@import url('/src/css/fade.css');
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
    border-radius: 10px 10px 0 0;
  }
  .new-subtitle {
    color: rgb(178, 222, 224);
  }
  .hot-subtitle {
    color: rgb(178, 222, 224);
  }
  .fanart-base {
    border-radius: 0px 10px 10px 10px;
    padding: 16px;
  }
  .new-fanart {
    display: flex;
    flex-wrap: wrap;
    background-color: rgba(234, 246, 251, 0.5);
  }
  .hot-fanart {
    background-color: rgba(234, 246, 251, 0.5);
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

@media (max-width: 800px) {
  .content-text {
    .tweet-card {
      max-width: calc(100vw - 32px);
      max-height: 400px;
    }
  }
}
.display-none {
  display: none;
}
</style>
