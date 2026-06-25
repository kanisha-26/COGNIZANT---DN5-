import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CourseService {

  constructor(private http: HttpClient) {}

  getCourses() {
    return this.http.get<any[]>(
      'https://jsonplaceholder.typicode.com/posts?_limit=5'
    );
  }
}