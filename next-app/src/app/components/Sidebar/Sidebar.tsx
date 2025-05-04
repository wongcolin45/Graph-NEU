'use client';
import styles from './Sidebar.module.css';
import React, {JSX, useState} from "react";


import SetSource from "@/app/components/SetSource/SetSource";
import SetDepartment from "@/app/components/SetDepartment/SetDepartment";
import SetCourseRange from "@/app/components/SetCourseRange/SetCourseRange";
import SetNUPath from "@/app/components/SetNUPath/SetNUPath";



const Sidebar = (): JSX.Element => {


    return (
        <div className={styles.sidebar}>
            <div className={styles.content}>
                <h1>Customize Graph</h1>
                <p>Modify your graph here.</p>
                <SetSource/>
                <SetDepartment/>
                <SetCourseRange/>
                <SetNUPath/>
            </div>
        </div>
);
};

export default Sidebar;
