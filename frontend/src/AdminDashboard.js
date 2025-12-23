import React, {useEffect, useState} from 'react';
import axios from 'axios';

export default function AdminDashboard({data}){
  const [profs, setProfs] = useState([]);
  const [students, setStudents] = useState([]);

  useEffect(()=>{
    const token = localStorage.getItem('token');
    const hdr = { headers: { Authorization: 'Token ' + token } };
    const fetch = async ()=>{
      try{
        const p = await axios.get('http://localhost:8000/api/admin/professors/', hdr);
        setProfs(p.data);
        const s = await axios.get('http://localhost:8000/api/admin/students/', hdr);
        setStudents(s.data);
      }catch(e){ console.error(e) }
    }
    fetch();
  },[])

  return (
    <div>
      <h2>Administrator Dashboard</h2>
      <p>Welcome, this dashboard is for administrators.</p>

      <div style={{marginTop:10}}>
        <h3>Professors</h3>
        {profs.length===0 ? <p>No professors yet.</p> : (
          <ul>{profs.map(p=> <li key={p.id}>{p.username} — {p.title} ({p.faculty})</li>)}</ul>
        )}
      </div>

      <div style={{marginTop:10}}>
        <h3>Students</h3>
        {students.length===0 ? <p>No students yet.</p> : (
          <ul>{students.map(s=> <li key={s.id}>{s.username} — Year {s.year} ({s.faculty})</li>)}</ul>
        )}
      </div>

      <div>
        <h3>Raw data</h3>
        <pre>{JSON.stringify(data || {}, null, 2)}</pre>
      </div>
    </div>
  )
}