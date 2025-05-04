'use client';

import 'reactflow/dist/style.css';
import './globals.css';

import styles from './Home.module.css';
import {JSX} from "react";



const Home = (): JSX.Element => {
    return (
        <div className={styles.container}>
            {/* ── Overview ───────────────────────── */}
            <section className={styles.section}>
                <h1 className={styles.title}>Overview</h1>
                <p className={styles.lead}>
                    This site transforms Northeastern’s tangle of course prerequisites into a clear, living graph.
                    Mark the classes you’ve completed and watch new nodes light up—revealing the courses that are now
                    within reach and how every path connects to your degree goals.
                </p>
            </section>

            {/* ── Tech Stack ─────────────────────── */}
            <section className={styles.section}>
                <h2 className={styles.heading}>Tech&nbsp;Stack</h2>

                <dl className={styles.techList}>
                    <div>
                        <dt>Frontend</dt>
                        <dd>
                            <strong>Next.js</strong>&nbsp;(client‑side) to render interactive graphs and collect user filters.
                        </dd>
                    </div>

                    <div>
                        <dt>Backend</dt>
                        <dd>
                            <strong>FastAPI</strong> with SQLAlchemy ORM for database access and&nbsp;
                            <strong>NetworkX</strong> for graph logic.
                        </dd>
                    </div>

                    <div>
                        <dt>Database</dt>
                        <dd>
                            <strong>PostgreSQL</strong>{' storing all Northeastern course data, populated by a '}
                            <strong>Beautiful Soup</strong> web‑scraper.
                        </dd>
                    </div>
                </dl>
            </section>

            {/* ── Roadmap ────────────────────────── */}
            <section className={styles.section}>
                <h2 className={styles.heading}>Future Improvements</h2>
                <ul className={styles.list}>
                    <li>Reduce edge‑crossing by pre‑computing graph coordinates.</li>
                    <li>Populate a MongoDB store with major/minor requirements.</li>
                    <li>Build a schedule‑planning tool on top of meta‑graphs.</li>
                    <li>Add user accounts so students can save their graphs.</li>
                </ul>
            </section>
        </div>
    );
}

export default Home;
