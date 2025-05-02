'use client';
import styles from './Sidebar.module.css';
import React, {JSX, useState} from "react";
import useSidebarStore from "@/app/store/useSidebarStore";

import SetSource from "@/app/components/SetSource/SetSource";
import SetFilter from "@/app/components/Filter/SetFilter";



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
                <SetFilter/>
            </div>
        </div>
    );
};

export default Sidebar;
