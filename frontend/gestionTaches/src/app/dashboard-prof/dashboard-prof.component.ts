import { Component, OnInit } from '@angular/core';
import { ProjectService } from '../services/project.service';
import { TaskService } from '../services/task.service';
import { StatisticsService } from '../services/statistics.service';
import { forkJoin } from 'rxjs';
import { Project } from '../model/project.model';
import { Task } from '../model/task.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard-prof',
  templateUrl: './dashboard-prof.component.html',
  standalone: false,
  styleUrls: ['./dashboard-prof.component.css']
})
export class DashboardProfComponent implements OnInit {
  currentUser: any;
  projects: Project[] = [];
  tasks: Task[] = [];
  taskStats: any = { completion_rate: 0 };
  selectedPeriod = 'trimester';
  loading = true;
  chartData: any;
  tasksByStatus: { todo: number; in_progress: number; completed: number } = { todo: 0, in_progress: 0, completed: 0 };

  constructor(
    private projectService: ProjectService,
    private taskService: TaskService,
    private statisticsService: StatisticsService,
    private router: Router
  ) {}

  ngOnInit(): void {
    console.log('✅ DashboardProfComponent chargé');
    this.loadDashboardData();
    this.loadCurrentUser();
  }

  loadCurrentUser(): void {
    this.currentUser = {
      username: 'Prof. Martin',
      email: 'martin@education.fr',
      avatar: null
    };
  }

  loadDashboardData(): void {
    this.loading = true;
    forkJoin({
      projects: this.projectService.getProjects(),
      tasks: this.taskService.getTasks({ assigned_to: 'me' }),
      taskStats: this.statisticsService.getTaskCompletionStats(this.selectedPeriod)
    }).subscribe({
      next: (results) => {
        this.projects = results.projects as Project[];
        this.tasks = results.tasks as Task[];
        this.taskStats = results.taskStats || { completion_rate: 0 };
        console.log("Task Stats récupérés :", this.taskStats);
        this.calculateTasksByStatus();
        this.prepareChartData();
        this.loading = false;
      },
      error: (error) => {
        console.error('Erreur lors du chargement des données:', error);
        this.loading = false;
      }
    });
  }

  calculateTasksByStatus(): void {
    this.tasksByStatus = { todo: 0, in_progress: 0, completed: 0 };
    this.tasks.forEach(task => {
      if (task.status === 'todo') this.tasksByStatus.todo++;
      else if (task.status === 'in_progress') this.tasksByStatus.in_progress++;
      else if (task.status === 'completed') this.tasksByStatus.completed++;
    });
    console.log("Répartition des tâches :", this.tasksByStatus);
  }

  prepareChartData(): void {
    this.chartData = {
      completionRates: {
        labels: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin'],
        datasets: [
          {
            label: 'Taux de complétion (%)',
            data: [65, 72, 80, 76, 85, this.taskStats.completion_rate || 0],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }
        ]
      }
    };
  }

  changePeriod(period: string): void {
    this.selectedPeriod = period;
    this.loadDashboardData();
  }
}
