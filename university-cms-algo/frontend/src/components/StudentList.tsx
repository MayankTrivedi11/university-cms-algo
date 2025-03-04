// frontend/src/components/StudentList.tsx
import React, { useState, useEffect } from 'react';
import { getStudents } from '../services/api';
import { Student } from '../types';

const StudentList: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const data = await getStudents();
        setStudents(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch students');
        console.error("Error fetching students:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  if (loading) {
    return <p>Loading students...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <div>
      <h2>Student List</h2>
      <ul>
        {students.map((student) => (
          <li key={student.student_id}>
            {student.name} ({student.major}) - {student.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StudentList;
