import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private apiUrl = 'http://localhost:8000/api/tasks';

  constructor(private http: HttpClient) { }

  getTasks(filters?: any): Observable<any[]> {
    let params = new HttpParams();
    
    if (filters) {
      Object.keys(filters).forEach(key => {
        if (filters[key]) {
          params = params.append(key, filters[key]);
        }
      });
    }
    
    return this.http.get<any[]>(this.apiUrl, { params });
  }

  getTask(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}/`);
  }

  createTask(task: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, task);
  }

  updateTask(id: number, task: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${id}/`, task);
  }

  deleteTask(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}/`);
  }

  updateStatus(id: number, status: string): Observable<any> {
    return this.http.patch<any>(`${this.apiUrl}/${id}/`, { status });
  }
}
