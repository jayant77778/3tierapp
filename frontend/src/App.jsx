import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function App() {
  const [health, setHealth] = useState('checking…');
  const [users, setUsers] = useState([]);
  const [name, setName] = useState('');

  useEffect(() => {
    axios.get('/api/health').then(r => setHealth(r.data.status)).catch(()=>setHealth('down'));
    axios.get('/api/users').then(r => setUsers(r.data)).catch(()=>setUsers([]));
  }, []);

  const addUser = async e => {
    e.preventDefault();
    if (!name.trim()) return;
    await axios.post('/api/users', { name });
    setName('');
    const res = await axios.get('/api/users');
    setUsers(res.data);
  };

  return (
    <div style={{fontFamily:'Inter,system-ui,Arial',padding:'36px',maxWidth:720,margin:'0 auto'}}>
      <h1>🚀 3-Tier CI/CD Demo</h1>
      <p><b>API health:</b> {health}</p>

      <form onSubmit={addUser} style={{marginTop:20,display:'flex',gap:8}}>
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="Add user name"
               style={{flex:1,padding:10,borderRadius:8,border:'1px solid #ddd'}}/>
        <button style={{padding:'10px 16px',borderRadius:8,border:'none',background:'#2563eb',color:'#fff'}}>Add</button>
      </form>

      <h3 style={{marginTop:24}}>Users</h3>
      <ul style={{paddingLeft:18}}>
        {users.map(u => <li key={u.id}>{u.name}</li>)}
      </ul>

      <footer style={{marginTop:40,color:'#666'}}>Frontend served by Nginx, API via Flask, DB PostgreSQL.</footer>
    </div>
  );
}
