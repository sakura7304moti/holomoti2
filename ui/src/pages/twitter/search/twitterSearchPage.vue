<template>
  <q-page class="">
    <!--検索フォーム-->
    <q-form @submit.prevent="onSearchClick" style="margin-bottom: 32px">
      <div class="search-form">
        <div class="search-input">
          <q-input v-model="condition.keyword" label="キーワード" dense />
        </div>
        <div class="search-input">
          <fanart-tag-select v-model="condition.hashtag" />
        </div>
        <div class="search-input">
          <q-select
            v-model="condition.likeCount"
            :options="[100, 1000, 5000, 10000, 20000, 50000]"
            label="♡"
            dense
          />
        </div>
        <div class="search-input search-btn">
          <q-btn label="検索" icon="search" color="primary" :loading="isLoading" type="submit" />
        </div>
      </div>
    </q-form>
    <!--メディア表示-->
    <div>
      <div v-for="item in dataState.tweets" :key="item.tweet.id" style="margin-bottom: 60px">
        <q-chat-message
          :name="item.user.userName"
          :avatar="item.user.userImage"
          style="max-width: 800px"
          bg-color="light-blue-1"
        >
          <div style="font-size: 15px; line-height: 1.5">
            {{ item.tweet.tweetText }}
          </div>
        </q-chat-message>
        <div v-for="md in item.media" :key="md.mediaUrl">
          <img :src="md.mediaUrl" class="tweet-img" v-if="md.mediaType == 'image'" />
        </div>
      </div>
    </div>
    <q-spinner v-if="isLoading" size="md" color="primary" />
  </q-page>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { useTwitterSearchModel } from 'src/pages/twitter/search/twitterSearchModels';
import FanartTagSelect from 'src/components/twitter/FanartTagSelect.vue';

export default defineComponent({
  name: 'twitter-search-page',
  components: {
    FanartTagSelect,
  },
  setup() {
    const { isLoading, page, condition, dataState, search } = useTwitterSearchModel();

    const onSearchClick = function () {
      page.value = 1;
      void search();
    };
    const onPageClick = function () {
      void search();
    };
    const onScrollSearch = function () {
      page.value += page.value;
      void search();
    };

    const handleScroll = () => {
      const bottomOfWindow =
        window.innerHeight + window.scrollY >= document.documentElement.offsetHeight - 200;

      if (bottomOfWindow && !isLoading.value && dataState.value.totalCount > page.value) {
        onScrollSearch();
      }
    };
    const onMount = function () {
      window.addEventListener('scroll', handleScroll);
      void search();
    };

    onMount();

    return {
      isLoading,
      page,
      condition,
      dataState,
      onSearchClick,
      onPageClick,
    };
  },
});
</script>
<style>
/**
 検索フォーム
*/
.search-form {
  display: flex;
  .search-input {
    max-width: 220px;
    width: 100%;
    margin-bottom: 16px;
    margin-right: 16px;
  }
}
@media (max-width: 750px) {
  .search-form {
    flex-wrap: wrap;
    .search-input {
      max-width: 400px;
    }
    .search-btn {
      text-align: right;
    }
  }
}
/**
 ツイート
*/
.tweet-img {
  max-width: 800px;
  width: 100%;
  max-height: 70vh;
  height: 100%;
  object-fit: contain;
}
</style>
