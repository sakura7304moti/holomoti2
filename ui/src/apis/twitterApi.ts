import { BaseApi } from './baseApi';

export class TwitterApi extends BaseApi {
  public newFanart(): Promise<SearchVo | null> {
    const path = '/twitter/new';
    const url = this.apiPath(path);
    return this.httpGet<SearchVo>(url);
  }

  public hotFanart(): Promise<SearchVo | null> {
    const path = '/twitter/hot';
    const url = this.apiPath(path);
    return this.httpGet<SearchVo>(url);
  }
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
  records: SearchTweetVo[];
  totalCount: number;
}
