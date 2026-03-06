'use client';

import 'reactflow/dist/style.css';
import './globals.css';

import styles from './Home.module.css';
import {JSX} from "react";
import Link from 'next/link';



const Home = (): JSX.Element => {
    return (
        <div className={styles.container}>
            {/* Hero */}
            <section className={styles.hero}>
                <h1 className={styles.title}>Visualize Your Path at Northeastern</h1>
                <p className={styles.lead}>
                    Turn Northeastern's web of course prerequisites into a clear, interactive graph.
                    Mark courses you've completed and instantly see which classes you're now eligible
                    for — and how every step connects to your degree.
                </p>
                <Link href="/explore" className={styles.cta}>Start Exploring</Link>
            </section>

            {/* How it works */}
            <section className={styles.section}>
                <h2 className={styles.heading}>How It Works</h2>
                <ol className={styles.list}>
                    <li><strong>Search</strong> for any course in the sidebar to load its prerequisite graph.</li>
                    <li><strong>Click a node</strong> to mark a course as completed — eligible courses light up.</li>
                    <li><strong>Filter</strong> by department, course level, or NUPath attribute to focus your view.</li>
                </ol>
            </section>
        </div>
    );
}

export default Home;
