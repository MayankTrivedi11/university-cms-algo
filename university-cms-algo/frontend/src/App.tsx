import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CourseList from './components/CourseList';
import CourseDetails from './components/CourseDetails';
import AddCourse from './components/AddCourse';
import EditCourse from './components/EditCourse';
import StudentList from './components/StudentList';
import './App';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>University Course Management</h1>
        <Routes>
          <Route path="/" element={<CourseList />} />
          <Route path="/courses/:id" element={<CourseDetails />} />
          <Route path="/add-course" element={<AddCourse />} />
          <Route path="/edit-course/:id" element={<EditCourse />} />
          <Route path="/students" element={<StudentList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;