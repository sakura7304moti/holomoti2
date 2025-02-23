import { TwitterApi } from 'src/apis/twitterApi';
import { computed, ref } from 'vue';
const NEWFANART_PAGE_COUNT = 3;
export const useIndexModel = function () {
  const twitterApi = new TwitterApi();
  const newFanartLoading = ref(false);
  const newFanartPage = ref(1); // 1 ~ 4
  const newFanartState = ref({
    totalCount: -1,
    records: [],
  } as SearchVo);

  const topFanartState = ref({
    totalCount: -1,
    records: [],
  } as SearchVo);

  const pageNewFanart = computed(() => {
    //
    // page = 0 -> start:0, end:3
    // page = 1 -> start:4, end:7
    const page = newFanartPage.value - 1;
    const start = NEWFANART_PAGE_COUNT * page;
    const end = start + NEWFANART_PAGE_COUNT;
    const items = newFanartState.value.records.slice(start, end);
    return items;
  });

  const getNewFanart = async function () {
    newFanartLoading.value = true;
    await twitterApi.newFanart().then((response) => {
      if (response) {
        console.log('new fanart response', response);
        newFanartState.value.records.splice(0);
        newFanartPage.value = 1;
        newFanartState.value.records = response.records;
      }
    });
    newFanartLoading.value = false;
  };

  void getNewFanart();

  return {
    newFanartLoading,
    newFanartPage,
    newFanartState,
    topFanartState,
    pageNewFanart,
    getNewFanart,
  };
};

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
  records: SearchTweetVo[];
  totalCount: number;
}
