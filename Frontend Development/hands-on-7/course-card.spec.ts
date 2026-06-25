import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CourseCard } from '../course-card/course-card';

@Component({
  selector: 'app-course-list',
  standalone: true,
  imports: [CommonModule, CourseCard],
  templateUrl: './course-list.html',
  styleUrl: './course-list.css'
})
export class CourseList {
  courses = [
    {
      name: 'Data Structures',
      code: 'CS101',
      credits: 4,
      grade: 'A'
    },
    {
      name: 'Database Management',
      code: 'CS102',
      credits: 3,
      grade: 'A+'
    },
    {
      name: 'Web Development',
      code: 'CS103',
      credits: 4,
      grade: 'B+'
    }
  ];
}