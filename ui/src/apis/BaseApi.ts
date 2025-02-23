import type { AxiosRequestConfig } from 'axios';
import type { AxiosResponse } from 'axios';
import axios from 'axios';
export class BaseApi {
  private apiEndpoint = function () {
    if (location.origin.includes('sakura0moti')) {
      return 'https://holomoti-api.sakura0moti.com';
    } else {
      return 'http://localhost:5000';
    }
  };

  private config = {
    headers: {
      'Content-Type': 'application/json',
    },
  } as AxiosRequestConfig;

  public apiPath = (path: string) => {
    return this.apiEndpoint() + path;
  };

  public async httpPost<T, U>(url: string, request: T): Promise<U | null> {
    try {
      const res = await axios.post<T, AxiosResponse<U, null>>(url, request, this.config);
      return res.data;
    } catch (e) {
      console.log('httpPost err', e);
      return null;
    }
  }

  public async httpGet<T>(url: string): Promise<T | null> {
    try {
      const res = await axios.get<null, AxiosResponse<T>>(url);
      return res.data;
    } catch (e) {
      console.log('httpGet err', e);
      return null;
    }
  }
}
