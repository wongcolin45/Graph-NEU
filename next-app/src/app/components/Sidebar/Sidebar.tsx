'use client';
import styles from './Sidebar.module.css';
import React, {JSX, useState} from "react";
import useSidebarStore from "@/app/store/useSidebarStore";
import useGraphStore from "@/app/store/useGraphStore";
import SetSource from "@/app/components/SetSource/SetSource";




const Sidebar = (): JSX.Element => {

    const sidebarOpen: boolean = useSidebarStore((state) => state.sidebarOpen);




    if (!sidebarOpen) {
        return <></>
    }





    return (
        <div className={styles.sidebar}>
            <div className={styles.content}>
                <h1>Customize Graph</h1>
                <p>Modify your graph here.</p>
                <SetSource/>
            </div>
        </div>
    );
};

export default Sidebar;
