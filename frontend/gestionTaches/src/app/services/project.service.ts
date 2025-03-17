// import { Injectable } from '@angular/core';
// import { HttpClient, HttpHeaders } from '@angular/common/http';
// import { Observable, throwError } from 'rxjs';
// import { catchError } from 'rxjs/operators';
// import { Project } from '../model/project.model';

// @Injectable({
//   providedIn: 'root'
// })
// export class ProjectService {
//   private apiUrl = 'http://localhost:8000/api/projects';

//   constructor(private http: HttpClient) { }

//   private getHeaders(): HttpHeaders {
//     const token = localStorage.getItem('token'); // Récupérer le token JWT
//     return new HttpHeaders({
//       'Authorization': `Bearer ${token}`,
//       'Content-Type': 'application/json'
//     });
//   }

//   getProjects(): Observable<Project[]> {
//     return this.http.get<Project[]>(this.apiUrl, { headers: this.getHeaders() }).pipe(
//       catchError(this.handleError)
//     );
//   }

  
//   getProject(id: number): Observable<Project> {
//     return this.http.get<Project>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() }).pipe(
//       catchError(this.handleError)
//     );
//   }

//   createProject(project: Project): Observable<Project> {
//     return this.http.post<Project>(this.apiUrl, project, { headers: this.getHeaders() }).pipe(
//       catchError(this.handleError)
//     );
//   }

//   updateProject(id: number, project: Partial<Project>): Observable<Project> {
//     return this.http.put<Project>(`${this.apiUrl}/${id}`, project, { headers: this.getHeaders() }).pipe(
//       catchError(this.handleError)
//     );
//   }

//   deleteProject(id: number): Observable<void> {
//     return this.http.delete<void>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() }).pipe(
//       catchError(this.handleError)
//     );
//   }

//   addMember(projectId: number, userId: number): Observable<Project> {
//     return this.http.post<Project>(`${this.apiUrl}/${projectId}/add_member`, { user_id: userId }, { headers: this.getHeaders() }).pipe(
//       catchError(this.handleError)
//     );
//   }

//   removeMember(projectId: number, userId: number): Observable<Project> {
//     return this.http.post<Project>(`${this.apiUrl}/${projectId}/remove_member`, { user_id: userId }, { headers: this.getHeaders() }).pipe(
//       catchError(this.handleError)
//     );
//   }

//   private handleError(error: any): Observable<never> {
//     console.error('Erreur API:', error);
//     return throwError(() => new Error(error.message || 'Erreur serveur'));
//   }
// }
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Project } from '../model/project.model';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  private apiUrl = 'http://localhost:8000/api/projects';

  constructor(private http: HttpClient) { }

  getProjects(): Observable<Project[]> {
    return this.http.get<Project[]>(this.apiUrl).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: any): Observable<never> {
    console.error('Erreur API:', error);
    return throwError(() => new Error(error.message || 'Erreur serveur'));
  }
  createProject(project: Project): Observable<Project> {
    return this.http.post<Project>(this.apiUrl, project).pipe(
      catchError(this.handleError)
    );
  }
  
  updateProject(id: number, project: Partial<Project>): Observable<Project> {
    return this.http.put<Project>(`${this.apiUrl}/${id}`, project).pipe(
      catchError(this.handleError)
    );
  }
}
