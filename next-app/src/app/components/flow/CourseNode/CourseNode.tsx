'use client'
import {Handle, Position} from 'reactflow';
import styles from './CourseNode.module.css'
import React, {JSX, useEffect, useState, useCallback} from 'react';
import type {CourseStatusMap, CourseStatus} from "@/app/explore/ExploreView";
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
    const [toast, setToast] = useState<string | null>(null);

    const handleNodeClick = () => {
        if (canTake()) {
            if (coursesTaken.has(course)) {
                removeCourse(course);
            } else {
                addCourse(course);
            }
            return;
        }
        const status: CourseStatus | undefined = courseStatusMap.get(course.replace(/\s+/g, ''));
        if (status != undefined) {
            setToast(status.message);
            setTimeout(() => setToast(null), 3500);
        }
    };

    const handleInfoClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        setShowCourseInfo(prev => !prev);
    };

    const handleCloseInfo = (e: React.MouseEvent) => {
        e.stopPropagation();
        setShowCourseInfo(false);
    };

    const nodeStyle = () => {
        if (coursesTaken.has(course)) {
            return { background: '#f3f4f6', borderColor: '#d1d5db', opacity: 0.75 };
        }
        if (canTake()) {
            return { background: '#eff6ff', borderColor: '#3b82f6', borderStyle: 'solid' };
        }
        return { background: '#fafafa', borderColor: '#e5e7eb', borderStyle: 'dashed', opacity: 0.6 };
    };

    const courseInfoPopup = (): JSX.Element => {
        if (!showCourseInfo) return <></>;
        return (
            <div className={styles.courseInfo}>
                <div className={styles.courseInfoHeader}>
                    <div>
                        <span className={styles.courseInfoCode}>{course}</span>
                        <h3 className={styles.courseInfoName}>{name}</h3>
                    </div>
                    <button className={styles.closeBtn} onClick={handleCloseInfo}>✕</button>
                </div>
                <div className={styles.courseInfoBody}>
                    {description && <p className={styles.courseInfoDesc}>{description}</p>}
                    <div className={styles.courseInfoMeta}>
                        {credits > 0 && (
                            <span className={`${styles.metaPill} ${styles.metaPillBlue}`}>
                                {credits} {credits === 1 ? 'credit' : 'credits'}
                            </span>
                        )}
                        {attributes && attributes.split(',').map((attr, i) => (
                            <span key={i} className={styles.metaPill}>{attr.trim()}</span>
                        ))}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <>
            {courseInfoPopup()}
            {toast && <div className={styles.toast}>{toast}</div>}
            <div className={styles.node} style={nodeStyle()} onClick={handleNodeClick}>
                <div className={styles.nodeContent}>
                    <span className={styles.courseCode}>{course}</span>
                    <span className={styles.courseName}>{name}</span>
                </div>
                <button className={styles.infoBtn} onClick={handleInfoClick}>i</button>
                <Handle type="target" position={Position.Top}/>
                <Handle type="source" position={Position.Bottom}/>
            </div>
        </>
    );
};

export default CourseNode;
