// frontend/src/components/AddCourse.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { addCourse } from '../services/api';
import { Course } from '../types';

const AddCourse: React.FC = () => {
  const [course_id, setCourseId] = useState('');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [credits, setCredits] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const newCourse: Course = {
      course_id,
      name,
      description,
      credits: parseInt(credits, 10),
    };

    try {
      await addCourse(newCourse);
      navigate('/'); // Redirect to course list
    } catch (error) {
      console.error('Failed to add course:', error);
      alert('Failed to add course.  See console for details.');
    }
  };

  return (
    <div>
      <h2>Add New Course</h2>
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
        <button type="submit">Add Course</button>
      </form>
    </div>
  );
};

export default AddCourse;
