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
        <div>
            <h1>Nutrition AI</h1>
            <Form onSubmit={submitQuery}>
                <Form.Label>Enter your nutrition query below: </Form.Label>
                <Form.Control placeholder="Type query here" value={query} onChange={(e)=>{
                    setQuery(e.target.value);
                    setAnswer("")
                }} />
                <Button variant="success" type="submit" >Submit</Button>
            </Form>
            <p>{answer? answer:<br />}</p>
        </div>
        
    )
}