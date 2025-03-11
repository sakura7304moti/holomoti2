import { BaseApi } from 'src/apis/baseApi';

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

  public tags(): Promise<FanartTag[] | null> {
    const path = '/twitter/tags';
    const url = this.apiPath(path);
    return this.httpGet<FanartTag[]>(url);
  }

  public searchFanart(request: SearchRequest, page: number): Promise<SearchVo | null> {
    let path = '/twitter/search';
    if (page > 1) {
      path += `?page=${page}`;
    }
    const url = this.apiPath(path);
    return this.httpPost<SearchRequest, SearchVo>(url, request);
  }
}
/**
 * 検索結果
 */
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

/**
 * ファンアートのタグ
 */
interface FanartTag {
  name: string;
  hashtag: string;
  url: string;
}

/**
 * 検索条件
 */
interface SearchRequest {
  keyword: string | null;
  hashtag: string | null;
  likeCount: number | null;
  userId: string | null;
}
