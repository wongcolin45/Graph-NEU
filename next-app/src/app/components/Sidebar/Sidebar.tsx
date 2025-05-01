'use client';
import styles from './Sidebar.module.css';
import React, {JSX, useState} from "react";
import useSidebarStore from "@/app/store/useSidebarStore";
import useGraphStore from "@/app/store/useGraphStore";




const Sidebar = (): JSX.Element => {

    const sidebarOpen: boolean = useSidebarStore((state) => state.sidebarOpen);
    const source: string = useGraphStore((s => s.source));
    const setSource: (newSource: string) => void = useGraphStore(s => s.setSource);

    const [input, setInput] = useState<string>('');
    const [editingSource, setEditingSource] = useState<boolean>(false);

    if (!sidebarOpen) {
        return <></>
    }

    const updateSource = () => setSource(input);

    const renderSource = () => {
        if (editingSource) {
            return (
                <input value={input}
                       onChange={(e) => setInput(e.target.value)}
                       onKeyDown={updateSource}>
                </input>
            )
        }
        return <h4>{source}</h4>
    }

    return (
        <div className={styles.sidebar}>
            <div className={styles.content}>
                <h2>Customize Graph</h2>
                <p>Modify your graph here.</p>

                <div className={styles.setSource}>
                    <h4>{'Source: '}</h4>
                    {renderSource()}
                    <button onClick={() => setEditingSource(prev => !prev)}>{'✏️'}</button>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
