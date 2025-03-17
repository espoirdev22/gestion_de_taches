import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone:false,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  errorMessage: string = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) return;
  
    const { username, password } = this.loginForm.value;
  
    this.authService.login(username, password).subscribe({
      next: (response) => {
        console.log("Réponse reçue :", response); // 🔍 Debugging
        if (!response || !response.user) {
          this.errorMessage = "Erreur: Réponse invalide du serveur.";
          return;
        }
  
        alert(response.message);
        const userType = response.user.user_type;
  
        if (userType === 'student') {
          this.router.navigate(['/dashboard-prof']);
        } else if (userType === 'professor') {
          this.router.navigate(['/dashboard-prof']);
        } else {
          this.router.navigate(['/']);
        }
      },
      error: (error) => {
        console.error("Erreur API :", error);
        this.errorMessage = 'Identifiants incorrects. Veuillez réessayer.';
      }
    });
  }
  
  
  }
