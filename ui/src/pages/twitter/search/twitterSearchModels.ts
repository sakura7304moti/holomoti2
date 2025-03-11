import { ref } from 'vue';
import { TwitterApi } from 'src/apis/twitterApi';
import { useQuasar } from 'quasar';

export const useTwitterSearchModel = function () {
  const quasar = useQuasar();
  const api = new TwitterApi();
  const isLoading = ref(false);
  const page = ref(1);
  const condition = ref({
    keyword: '',
    hashtag: '',
    likeCount: 100,
    userId: '',
  } as SearchCondition);
  const dataState = ref({
    tweets: [],
    totalCount: 0,
  } as SearchVo);

  const search = async function () {
    isLoading.value = true;
    await api
      .searchFanart(condition.value, page.value)
      .then((response) => {
        if (response) {
          console.log('search response', response);
          if (page.value <= 1) {
            dataState.value.tweets.splice(0);
          }
          response.records.forEach((r) => dataState.value.tweets.push(r));
          dataState.value.totalCount = response.totalCount;
        }
      })
      .catch((err) => {
        console.log('search err', err);
        quasar.notify({
          position: 'top',
          color: 'negative',
          message: '検索でエラーになった...',
        });
      });
    isLoading.value = false;
  };
  return {
    isLoading,
    page,
    condition,
    dataState,
    search,
  };
};

interface SearchCondition {
  keyword: string;
  hashtag: string;
  likeCount: number;
  userId: string;
}
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
interface SearchVo {
  tweets: SearchTweetVo[];
  totalCount: number;
}
