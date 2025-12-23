import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function StudentDashboard({data}){
  const [studentSubjects, setStudentSubjects] = useState(data?.subjects || []);
  const [allSubjects, setAllSubjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(()=>{
    const fetch = async ()=>{
      try{
        const r = await axios.get('http://localhost:8000/api/subjects/');
        setAllSubjects(r.data);
        // refresh student subjects from protected endpoint
        const token = localStorage.getItem('token');
        const hdr = { headers: { Authorization: 'Token ' + token } };
        const s = await axios.get('http://localhost:8000/api/student/', hdr).catch(()=>null);
        if(s && s.data) setStudentSubjects(s.data.subjects || []);
      }catch(e){ console.error(e) }
      setLoading(false);
    }
    fetch();
  },[])

  const isEnrolled = (subject)=> {
    return studentSubjects.some(s => s.id === subject.id);
  }

  const enroll = async (subjectId)=>{
    const token = localStorage.getItem('token');
    const hdr = { headers: { Authorization: 'Token ' + token } };
    try{
      const resp = await axios.post(`http://localhost:8000/api/subjects/${subjectId}/enroll/`, {}, hdr);
      // update local state: add to studentSubjects
      setAllSubjects(prev => prev.map(s => s.id===resp.data.id ? resp.data : s));
      setStudentSubjects(prev => [...prev, resp.data]);
      alert('Enrolled successfully');
    }catch(e){ alert('Enroll failed'); }
  }

  return (
    <div>
      <h2>Student Dashboard</h2>
      <p>Welcome — here are your enrolled subjects and available courses to enroll.</p>

      <div style={{marginTop:10}}>
        <h3>Your Subjects</h3>
        {studentSubjects.length===0 ? <p>No subjects enrolled.</p> : (
          <ul>{studentSubjects.map(s=> <li key={s.id}>{s.name}</li>)}</ul>
        )}
      </div>

      <div style={{marginTop:10}}>
        <h3>Available Courses</h3>
        {loading ? <p>Loading...</p> : (
          <ul>
            {allSubjects.map(s => (
              <li key={s.id} style={{marginBottom:8}}>
                <strong>{s.name}</strong> — {s.professor}
                {' '}
                {isEnrolled(s) ? <em style={{marginLeft:8}}>Enrolled</em> : (
                  <button className="button" onClick={()=>{ if(window.confirm('Enroll in this course?')) enroll(s.id) }} style={{marginLeft:8}}>Enroll</button>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

    </div>
  )
}