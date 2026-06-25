import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { Header } from './header/header';
import { CourseList } from './course-list/course-list';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [Header, RouterOutlet, CourseList],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('student-portal-angular');
}