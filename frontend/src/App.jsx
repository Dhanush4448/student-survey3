import { useEffect, useState } from "react";
import axios from "axios";
import { API_BASE } from "./api";

export default function App() {
  const [rows, setRows] = useState([]);
  const [form, setForm] = useState({
    first_name:"", last_name:"", street_address:"", city:"", state:"",
    zip:"", telephone:"", email:"", date_of_survey:"",
    liked_most:"", how_interested:"", recommend_likelihood:""
  });

  const load = async () => {
    try {
      const r = await axios.get(`${API_BASE}/surveys`);
      setRows(r.data);
    } catch (e) {
      console.error(e);
      alert("Failed to load surveys. Is the backend running?");
    }
  };
  useEffect(() => { load(); }, []);

  const submit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE}/surveys`, form);
      await load();
      alert("Submitted!");
      setForm({
        first_name:"", last_name:"", street_address:"", city:"", state:"",
        zip:"", telephone:"", email:"", date_of_survey:"",
        liked_most:"", how_interested:"", recommend_likelihood:""
      });
    } catch (e) {
      console.error(e);
      alert("Submit failed. Check backend/API_BASE.");
    }
  };

  return (
    <div style={{padding:24, maxWidth:720, margin:"0 auto"}}>
      <h2>Student Survey</h2>
      <form onSubmit={submit} style={{display:"grid", gap:8}}>
        <input required placeholder="First Name" value={form.first_name} onChange={e=>setForm({...form, first_name:e.target.value})}/>
        <input required placeholder="Last Name" value={form.last_name} onChange={e=>setForm({...form, last_name:e.target.value})}/>
        <input required placeholder="Street Address" value={form.street_address} onChange={e=>setForm({...form, street_address:e.target.value})}/>
        <input required placeholder="City" value={form.city} onChange={e=>setForm({...form, city:e.target.value})}/>
        <input required placeholder="State" value={form.state} onChange={e=>setForm({...form, state:e.target.value})}/>
        <input required placeholder="Zip" value={form.zip} onChange={e=>setForm({...form, zip:e.target.value})}/>
        <input required placeholder="Telephone" value={form.telephone} onChange={e=>setForm({...form, telephone:e.target.value})}/>
        <input required type="email" placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})}/>
        <input required type="date" placeholder="Date of Survey" value={form.date_of_survey} onChange={e=>setForm({...form, date_of_survey:e.target.value})}/>
        <input required placeholder="Liked Most (students/location/...)" value={form.liked_most} onChange={e=>setForm({...form, liked_most:e.target.value})}/>
        <input required placeholder="How Interested (friends/television/...)" value={form.how_interested} onChange={e=>setForm({...form, how_interested:e.target.value})}/>
        <input required placeholder="Recommend (Very Likely/Likely/Unlikely)" value={form.recommend_likelihood} onChange={e=>setForm({...form, recommend_likelihood:e.target.value})}/>
        <button type="submit">Submit</button>
      </form>

      <h3 style={{marginTop:24}}>All Surveys</h3>
      <table border="1" cellPadding="6" style={{borderCollapse:"collapse"}}>
        <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Date</th></tr></thead>
        <tbody>
          {rows.map(r => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.first_name} {r.last_name}</td>
              <td>{r.email}</td>
              <td>{r.date_of_survey}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
