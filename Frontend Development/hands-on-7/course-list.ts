import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { CourseCard } from '../course-card/course-card';
import { CourseService } from '../course.service';

@Component({
  selector: 'app-course-list',
  standalone: true,
  imports: [CommonModule, FormsModule, CourseCard],
  templateUrl: './course-list.html',
  styleUrl: './course-list.css'
})
export class CourseList implements OnInit {

  searchTerm = '';

  loading = true;

  courses: any[] = [];

  constructor(private courseService: CourseService) {}

  ngOnInit() {
    this.loading = true;

    this.courseService.getCourses().subscribe({
      next: (data) => {
        console.log('API Data:', data);

        this.courses = data.map((post: any, index: number) => ({
          name: post.title,
          code: 'CS10' + index,
          credits: 4,
          grade: 'A'
        }));

        console.log('Courses:', this.courses);

        this.loading = false;
      },

      error: (err) => {
        console.error(err);

        this.loading = false;
      }
    });
  }

  get filteredCourses() {
    return this.courses.filter(course =>
      course.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
}