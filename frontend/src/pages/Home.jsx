import React, {useState} from "react";
import {Form, Button} from "react-bootstrap"
import axios from "axios"

export default function Home() {

    const [query, setQuery] = useState("");
    const [answer, setAnswer] = useState("");

    const submitQuery = (e) => {
        e.preventDefault();
        if (query) {
            setAnswer("generating response...")
            axios.post("http://localhost:8000/ask", {"question": query})
                .then((res) => {
                    setAnswer(res?.data?.answer)
                })
                .catch((err) => {
                    console.error(err)
                })
        } else {
            alert("Please enter query")
        }
    }

    return (
        <div className="page">
            <div className="card">
                <h1 className="title">Nutrition AI</h1>
                <Form onSubmit={submitQuery}>
                    <Form.Label className="label">Enter your nutrition query below: </Form.Label>
                    <Form.Control className="input" placeholder="Type query here" value={query} onChange={(e)=>{
                        setQuery(e.target.value);
                        setAnswer("")
                    }} />
                    <Button className="button" variant="success" type="submit" >Submit</Button>
                </Form>
                <p className="answerBox">{answer? answer:<br />}</p>
            </div>
        </div>
        
    )
}