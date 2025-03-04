// frontend/src/components/CourseDetails.tsx
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getCourse } from '../services/api';
import { Course } from '../types';

const CourseDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCourse = async () => {
      if (!id) {
        setError("Course ID is missing.");
        setLoading(false);
        return;
      }

      try {
        const data = await getCourse(id);
        setCourse(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch course details');
        console.error("Error fetching course details:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCourse();
  }, [id]);

  if (loading) {
    return <p>Loading course details...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  if (!course) {
    return <p>Course not found.</p>;
  }

  return (
    <div>
      <h2>{course.name}</h2>
      <p>Description: {course.description}</p>
      <p>Credits: {course.credits}</p>
      <Link to={`/edit-course/${course.course_id}`}>Edit Course</Link>
      <Link to="/">Back to Course List</Link>
    </div>
  );
};

export default CourseDetails;
