'use client';


import 'reactflow/dist/style.css';

import './globals.css';
import {JSX} from "react";



const Home = (): JSX.Element => {


    return (
        <div className='home'>
            <h1>Overview</h1>
            <p>
                This site transforms Northeastern’s tangle of course prerequisites into a clear, living graph. By
                marking the classes they’ve already taken, students see the remaining nodes light up—revealing which
                courses are now within reach and how each path connects to their degree goals. The graph provides a
                concise, objective map of prerequisite pathways, making it straightforward to spot viable course
                sequences and plan future semesters.
            </p>
            <h1>Tech Stack</h1>
            <span>
                <strong>{'Frontend: '}</strong>
                Built in Next.js mainly CSR to display graphs and get user's filtering preferences
            </span>
            <br></br>
            <br></br>
            <span>
                <strong>{'Backend: '}</strong>
                Built in FastAPI utilizing SQL Alchemy's ORM for databse queries and NetworkX for graph logic.
            </span>
            <br></br>
            <br></br>
            <span>
                <strong>{'Database: '}</strong>
                Storing all Northeastern course information in a PostgreSQL database.  I built a webscraper in python utilizing Beautiful soup to populate this.
            </span>

        </div>

    )
}

export default Home;