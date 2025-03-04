// frontend/src/components/CourseList.tsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getCourses } from '../services/api';
import { Course } from '../types';

const CourseList: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const data = await getCourses();
        setCourses(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch courses');
        console.error("Error fetching courses:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  if (loading) {
    return <p>Loading courses...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <div>
      <h2>Course List</h2>
      <ul>
        {courses.map((course) => (
          <li key={course.course_id}>
            <Link to={`/courses/${course.course_id}`}>{course.name}</Link>
          </li>
        ))}
      </ul>
      <Link to="/add-course">Add New Course</Link>
    </div>
  );
};

export default CourseList;
