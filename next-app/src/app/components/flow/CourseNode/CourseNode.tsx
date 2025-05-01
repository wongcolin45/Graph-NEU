'use client'
import {Handle, Position} from 'reactflow';
import styles from './CourseNode.module.css'
import React, {JSX, useEffect, useState, useCallback} from 'react';
import axios from 'axios';
import {createPortal} from "react-dom";
import type {CourseStatusMap, CourseStatus} from "@/app/explore/page";
import useUserDataStore from "@/app/store/useUserDataStore";

interface CourseData {
    label: string
    course: string,
    name: string,
    description: string,
    credits: number,
    attributes: string,
    courseStatusMap: CourseStatusMap
}

const CourseNode = ({ data }: { data: CourseData}) => {

    const {label, course, name, description, credits, attributes, courseStatusMap} = data;

    // import global state from Zustand
    const coursesTaken = useUserDataStore((state) => state.coursesTaken);
    const addCourse = useUserDataStore((state) => state.addCourse);
    const removeCourse = useUserDataStore((state) => state.removeCourse);


    const canTake = useCallback((): boolean => {
        const id = course.replace(/\s+/g, '');
        const status: CourseStatus | undefined = courseStatusMap.get(id);
        return status != undefined && status.satisfied;
    }, [course, courseStatusMap]);

    useEffect(() => {
        if (coursesTaken.has(course) && !canTake()) {
            removeCourse(course);
        }
    }, [coursesTaken, canTake]);

    const [showCourseInfo, setShowCourseInfo] = useState<boolean>(false);

    const handleNodeClick = () => {
        if (canTake()) {
            if (coursesTaken.has(course)){
                removeCourse(course);
            } else {
                addCourse(course);
            }
            return
        }
        const status: CourseStatus | undefined = courseStatusMap.get(course.replace(/\s+/g, ''));

        if (status != undefined) {
            console.log('status ' + status.message)
            alert(status.message);
        } else {
            console.log('status not found for '+course);
        }
    };

    const handleCourseInfoClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        setShowCourseInfo(prev => !prev);
    }

    const courseInfo = (): JSX.Element => {
        if (!showCourseInfo) {
            return <></>
        }
        return (
            <div className={styles.courseInfo}>
                <h3>{label}</h3>
                <p>{description}</p>
                <span><strong>{'Attribute(s): '}</strong>{attributes}</span>
            </div>
        )
    }

    const nodeStyle = () =>{
        if (coursesTaken.has(course)) {
            return { backgroundColor: '#e0e0e0', opacity: 0.8 };
        }

        if (canTake()) {
            return { backgroundColor: '#e6f7ff', border: '2px solid #2196f3' };
        }

        return { backgroundColor: '#f5f5f5', border: '2px dashed #ccc', opacity: 0.5 };

    }

    //div style={{position: 'relative', display: 'inline-block'}}
    return (
        <>
            {courseInfo()}
            <div className={styles.node} style={nodeStyle()} onClick={handleNodeClick}>
                <span>
                    <strong>{course}</strong>{`: ${name}`}
                </span>
                    <button onClick={(e) => handleCourseInfoClick(e)}>📖</button>
                    <Handle type="target" position={Position.Top}/>
                    <Handle type="source" position={Position.Bottom}/>
            </div>
        </>
    );



}

export default CourseNode;
