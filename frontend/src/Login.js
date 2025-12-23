import React, {useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';

function Login(){
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    try{
      const resp = await axios.post('http://localhost:8000/api/login/', {username, password});
      localStorage.setItem('token', resp.data.token);
      localStorage.setItem('username', resp.data.username);
      localStorage.setItem('userid', resp.data.id);
      localStorage.setItem('role', resp.data.role || '');
      navigate('/dashboard');
    }catch(e){
      alert('login failed');
    }
  }

  return (
    <div style={{maxWidth:400, margin:'20px auto'}}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <div>
          <label>Username</label>
          <input value={username} onChange={e=>setUsername(e.target.value)} />
        </div>
        <div>
          <label>Password</label>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  )
}

export default Login;