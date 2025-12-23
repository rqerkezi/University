import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import AdminDashboard from './AdminDashboard';
import StudentDashboard from './StudentDashboard';
import ProfessorDashboard from './ProfessorDashboard';

function Dashboard(){
  const [username, setUsername] = useState(null);
  const [data, setData] = useState(null);
  const [role, setRole] = useState(null);
  const navigate = useNavigate();

  useEffect(()=>{
    const token = localStorage.getItem('token');
    const uname = localStorage.getItem('username');
    const r = localStorage.getItem('role');
    if(!token) { navigate('/'); return; }
    setUsername(uname);
    setRole(r);
    // fetch role-specific dashboard
    const hdr = { headers: { Authorization: 'Token ' + token } };
    let url = 'http://localhost:8000/api/';
    if(r==='student') url += 'student/';
    else if(r==='professor') url += 'professor/';
    else if(r==='administrator') url += 'admin/';
    else { setData({role: 'Unknown', info: {}}); return; }

    axios.get(url, hdr).then(resp=>setData(resp.data)).catch(()=>{ localStorage.clear(); navigate('/'); });
  },[])

  const doLogout = async ()=>{
    const token = localStorage.getItem('token');
    if(!token){ localStorage.clear(); navigate('/'); return; }
    const hdr = { headers: { Authorization: 'Token ' + token } };
    try{
      await axios.post('http://localhost:8000/api/logout/', {}, hdr);
    }catch(e){ /* ignore errors */ }
    localStorage.clear();
    navigate('/');
  }

  if(!username) return <div>Loading...</div>
  // show different components depending on role
  return (
    <div className="container">
      <div className="card">
        {role==='administrator' && <AdminDashboard data={data} />}
        {role==='student' && <StudentDashboard data={data} />}
        {role==='professor' && <ProfessorDashboard data={data} />}
        {!['administrator','student','professor'].includes(role) && (
          <div>
            <h2>Unknown role</h2>
            <pre>{JSON.stringify(data || {}, null, 2)}</pre>
          </div>
        )}
        <div style={{marginTop:20}}>
          <button className="button" onClick={doLogout}>Logout</button>
        </div>
      </div>
    </div>
  )
}

export default Dashboard;