<template>
  <q-page class="">
    <div>
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
          <q-btn label="検索" icon="search" color="primary" :loading="isLoading" @click="search" />
        </div>
      </div>
    </div>
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
    const { isLoading, page, condition, search } = useTwitterSearchModel();
    return {
      isLoading,
      page,
      condition,
      search,
    };
  },
});
</script>
<style>
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
</style>
