<template>
  <q-card>
    <q-card-section class="tw-card" style="padding: 0">
      <div v-if="st.media[0]" class="tw-card">
        <div v-if="st.media[0].mediaType == 'image'" class="tw-card">
          <img :src="st.media[0].mediaUrl" class="tw-img" />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>
<script lang="ts">
import { computed, defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'tweet-card',
  props: {
    state: {
      type: Object as () => SearchTweetVo,
      required: true,
    },
  },
  setup(props) {
    const st = computed(() => props.state);
    const dialogOpen = ref(false);
    return { st, dialogOpen };
  },
});
interface Tweet {
  id: number;
  tweetText: string;
  tweetUrl: string;
  likeCount: number;
}

interface Media {
  mediaType: string;
  mediaUrl: string;
  thumbnailUrl: string;
}

interface User {
  userId: string;
  userImage: string;
  userName: string;
}

interface SearchTweetVo {
  hashtags: string[];
  media: Media[];
  tweet: Tweet;
  user: User;
}
</script>
<style>
.tw-img {
  max-width: 100%;
  width: auto;
  max-height: 100%;
  height: auto;
  object-fit: contain;
}
.tw-card {
  max-height: 100%;
  height: 100%;
}
</style>
