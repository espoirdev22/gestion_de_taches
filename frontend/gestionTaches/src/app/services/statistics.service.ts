import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StatisticsService {
  private apiUrl = 'http://localhost:8000/api/stats';

  constructor(private http: HttpClient) { }

  getPersonalStats(period?: string): Observable<any> {
    let params = new HttpParams();
    if (period) {
      params = params.append('period', period);
    }
    return this.http.get<any>(`${this.apiUrl}/me/`, { params });
  }

  getTeamStats(period?: string): Observable<any[]> {
    let params = new HttpParams();
    if (period) {
      params = params.append('period', period);
    }
    return this.http.get<any[]>(`${this.apiUrl}/team/`, { params });
  }

  getTaskCompletionStats(period?: string): Observable<any> {
    let params = new HttpParams();
    if (period) {
      params = params.append('period', period);
    }
    return this.http.get<any>(`${this.apiUrl}/task-completion/`, { params });
  }

  getBonusEligibility(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/bonus-eligibility/`);
  }
}

