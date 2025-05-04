'use client';
import styles from './Sidebar.module.css';
import React, {JSX, useState} from "react";
import useSidebarStore from "@/app/store/useSidebarStore";

import SetSource from "@/app/components/SetSource/SetSource";
import SetDepartment from "@/app/components/SetDepartment/SetDepartment";
import SetCourseRange from "@/app/components/SetCourseRange/SetCourseRange";
import SetNUPath from "@/app/components/SetNUPath/SetNUPath";

import { usePathname} from "next/navigation";

const Sidebar = (): JSX.Element => {

    const sidebarOpen: boolean = useSidebarStore((state) => state.sidebarOpen);


    const pathname: string = usePathname();

    if (!sidebarOpen || !pathname.includes("explore")) {
        return <></>
    }





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
