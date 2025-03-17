import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:8000/api/auth/user/';
  private refreshUrl = 'http://127.0.0.1:8000/api/auth/token/refresh/'; // Correction de l'URL

  constructor(private http: HttpClient) {}

  /**
   * Connexion de l'utilisateur
   */
  login(username: string, password: string): Observable<any> {
    return this.http.post<{ access: string, refresh: string }>(this.apiUrl, { username, password }).pipe(
      tap(response => {
        if (response.access) {
          this.setToken(response.access, response.refresh);
        }
      }),
      catchError(error => {
        console.error("Erreur de connexion :", error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Stocke les tokens dans localStorage
   */
  private setToken(access: string, refresh: string) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  /**
   * Récupère le token d'accès
   */
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Récupère le refresh token
   */
  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  /**
   * Vérifie si l'utilisateur est connecté
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  /**
   * Déconnexion de l'utilisateur
   */
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  /**
   * Rafraîchit le token d'accès quand il expire
   */
  refreshToken(): Observable<any> {
    const refresh = this.getRefreshToken();
    if (!refresh) {
      console.error("Aucun refresh token trouvé !");
      return throwError(() => new Error("Aucun refresh token disponible"));
    }

    return this.http.post<{ access: string }>(this.refreshUrl, { refresh }).pipe(
      tap(response => {
        console.log("Réponse du rafraîchissement :", response);
        if (response.access) {
          localStorage.setItem('access_token', response.access);
        }
      }),
      catchError(error => {
        console.error("Erreur de rafraîchissement :", error);
        return throwError(() => error);
      })
    );
  }
}
