import React from 'react';

export default function ProfessorDashboard({data}){
  const subjects = data?.subjects || [];
  return (
    <div>
      <h2>Professor Dashboard</h2>
      <p>Welcome, professor. Here are your subjects and enrolled students:</p>
      {subjects.length===0 ? <p>No subjects assigned.</p> : (
        <div>
          {subjects.map(s=> (
            <div key={s.id} style={{border:'1px solid #ddd', padding:10, marginBottom:10}}>
              <h4>{s.name}</h4>
              <p><strong>Faculty:</strong> {s.faculty?.name || '-'}</p>
              <p><strong>Enrolled Students:</strong></p>
              {(!s.students || s.students.length===0) ? <p>No students enrolled.</p> : (
                <ul>{s.students.map((st, idx)=> <li key={idx}>{st}</li>)}</ul>
              )}
            </div>
          ))}
        </div>
      )}
      <div>
        <h3>Raw data</h3>
        <pre>{JSON.stringify(data || {}, null, 2)}</pre>
      </div>
    </div>
  )
}