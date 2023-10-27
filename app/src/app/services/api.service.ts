import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

export interface CrawlerResult {
  data: any;
  status: string;
}

export interface PostResult {
  data: any;
  times: any;
  status: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getCrawlerData(url: string): Observable<CrawlerResult> {
    const params = new HttpParams({
      fromObject: {
        url: url
      }
    });

    return this.http.get<CrawlerResult>(
      `${this.apiUrl}/crawl`,
      { params: params }
    );
  }

  analyzeFrequencies(payload: any): Observable<PostResult> {
    return this.http.post<PostResult>(
      `${this.apiUrl}/frequencies`,
      { 
        text: payload.text,
      }
    );
  }

  runSearch(payload: any): Observable<PostResult> {
    return this.http.post<PostResult>(
      `${this.apiUrl}/search`,
      { 
        text: payload.text,
        term: payload.term
      }
    );
  }
}
