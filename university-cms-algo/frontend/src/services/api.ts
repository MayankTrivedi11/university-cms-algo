// frontend/src/services/api.ts
import axios from 'axios';
import { Course, Student } from '../types';

const API_BASE_URL = 'http://localhost:5000'; // Backend address

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Generic error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Courses
export const getCourses = async () => {
  const response = await api.get('/courses/');
  return response.data;
};

export const getCourse = async (id: string) => {
  const response = await api.get(`/courses/${id}`);
  return response.data;
};

export const addCourse = async (course: Course) => {
  const response = await api.post('/courses/', course);
  return response.data;
};

export const updateCourse = async (id: string, course: Course) => {
  const response = await api.put(`/courses/${id}`, course);
  return response.data;
};

export const deleteCourse = async (id: string) => {
  await api.delete(`/courses/${id}`);
};

// Students
export const getStudents = async () => {
  const response = await api.get('/students/');
  return response.data;
};

export const getStudent = async (id: string) => {
  const response = await api.get(`/students/${id}`);
  return response.data;
};

export const addStudent = async (student: Student) => {
  const response = await api.post('/students/', student);
  return response.data;
};

export const updateStudent = async (id: string, student: Student) => {
  const response = await api.put(`/students/${id}`, student);
  return response.data;
};

export const deleteStudent = async (id: string) => {
  await api.delete(`/students/${id}`);
};

export default api; // Export the axios instance
