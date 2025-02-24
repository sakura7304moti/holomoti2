import { useQuasar } from 'quasar';
import { TwitterApi } from 'src/apis/twitterApi';
import { ref } from 'vue';
export const useIndexModel = function () {
  const quasar = useQuasar();
  const twitterApi = new TwitterApi();
  const newFanartLoading = ref(false);
  const topFanartLoading = ref(false);
  const newFanartPage = ref(1); // 1 ~ 4
  const newFanartState = ref({
    totalCount: -1,
    records: [],
  } as SearchVo);

  const topFanartState = ref({
    totalCount: -1,
    records: [],
    users: [],
  } as HotSearchVo);

  const getNewFanart = async function () {
    newFanartLoading.value = true;
    await twitterApi
      .newFanart()
      .then((response) => {
        if (response) {
          console.log('new fanart response', response);
          newFanartState.value.records.splice(0);
          newFanartPage.value = 1;
          newFanartState.value.records = response.records;
        }
      })
      .catch((err) => {
        console.log('newFanart err', err);
        quasar.notify({
          color: 'negative',
          message: 'New!の取得でエラーになりました...',
          position: 'top',
        });
      });
    newFanartLoading.value = false;
  };

  const getTopFanart = async function () {
    topFanartLoading.value = true;
    await twitterApi
      .hotFanart()
      .then((response) => {
        if (response) {
          console.log('top fanart response', response);
          topFanartState.value.records.splice(0);
          topFanartState.value.users.splice(0);
          topFanartState.value.records = response.records;
          response.records.forEach((rec) => {
            const user = rec.user;
            if (
              topFanartState.value.users.find((it) => it.userId == rec.user.userId) == undefined
            ) {
              topFanartState.value.users.push(user);
            }
          });
          console.log('top fanart result', topFanartState.value);
        }
      })
      .catch((err) => {
        console.log('topFanart err', err);
        quasar.notify({
          color: 'negative',
          message: 'Hot!の取得でエラーになりました...',
          position: 'top',
        });
      });
    topFanartLoading.value = false;
  };

  void getNewFanart();
  void getTopFanart();

  return {
    newFanartLoading,
    topFanartLoading,
    newFanartPage,
    newFanartState,
    topFanartState,
    getNewFanart,
    getTopFanart,
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
interface HotSearchVo extends SearchVo {
  users: User[];
}
