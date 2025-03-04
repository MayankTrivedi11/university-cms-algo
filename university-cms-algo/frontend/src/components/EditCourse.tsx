// frontend/src/components/EditCourse.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getCourse, updateCourse } from '../services/api';
import { Course } from '../types';

const EditCourse: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [course_id, setCourseId] = useState('');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [credits, setCredits] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCourse = async () => {
      if (!id) return;
      try {
        const data = await getCourse(id);
        setCourseId(data.course_id);
        setName(data.name);
        setDescription(data.description);
        setCredits(data.credits.toString()); // Convert number to string
      } catch (error) {
        console.error('Failed to fetch course:', error);
        alert('Failed to fetch course.  See console for details.');
      }
    };

    fetchCourse();
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!id) return;

    const updatedCourse: Course = {
      course_id,
      name,
      description,
      credits: parseInt(credits, 10),
    };

    try {
      await updateCourse(id, updatedCourse);
      navigate('/'); // Redirect to course list
    } catch (error) {
      console.error('Failed to update course:', error);
      alert('Failed to update course. See console for details.');
    }
  };

  return (
    <div>
      <h2>Edit Course</h2>
      <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="course_id">Course ID:</label>
            <input
              type="text"
              id="course_id"
              value={course_id}
              onChange={(e) => setCourseId(e.target.value)}
              required
            />
          </div>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="credits">Credits:</label>
          <input
            type="number"
            id="credits"
            value={credits}
            onChange={(e) => setCredits(e.target.value)}
            required
          />
        </div>
        <button type="submit">Update Course</button>
      </form>
    </div>
  );
};

export default EditCourse;
