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

const CourseNode = ({ data }: { data: CourseData }) => {

    const { label, course, name, description, credits, attributes, courseStatusMap } = data;

    const coursesTaken = useUserDataStore((state) => state.coursesTaken);
    const addCourse    = useUserDataStore((state) => state.addCourse);
    const removeCourse = useUserDataStore((state) => state.removeCourse);

    const getStatus = useCallback((): CourseStatus | undefined =>
        courseStatusMap.get(course.replace(/\s+/g, '')),
    [course, courseStatusMap]);

    const canTake = useCallback((): boolean => {
        const s = getStatus();
        return s != null && s.satisfied;
    }, [getStatus]);

    // Auto-remove if prerequisites were revoked
    useEffect(() => {
        if (coursesTaken.has(course) && !canTake()) {
            removeCourse(course);
        }
    }, [coursesTaken, canTake]);

    // Auto-close prereq modal once node becomes unlocked
    useEffect(() => {
        if (canTake()) setShowPrereqs(false);
    }, [canTake]);

    const [showInfo,    setShowInfo]    = useState(false);
    const [showPrereqs, setShowPrereqs] = useState(false);

    const handleNodeClick = () => {
        const status = getStatus();

        // Status map not loaded yet — do nothing
        if (status === undefined) return;

        if (status.satisfied) {
            coursesTaken.has(course) ? removeCourse(course) : addCourse(course);
            return;
        }

        // Explicitly locked — show prereq helper
        setShowPrereqs(prev => !prev);
        setShowInfo(false);
    };

    const handleInfoClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        setShowInfo(prev => !prev);
        setShowPrereqs(false);
    };

    const nodeStateClass = () => {
        if (coursesTaken.has(course)) return styles.nodeTaken;
        if (canTake())               return styles.nodeAvailable;
        return styles.nodeLocked;
    };

    /* ── Course info popup ─────────────────────── */
    const courseInfoPopup = (): JSX.Element => {
        if (!showInfo) return <></>;
        return (
            <div className={styles.courseInfo}>
                <div className={styles.courseInfoHeader}>
                    <div>
                        <span className={styles.courseInfoCode}>{course}</span>
                        <h3 className={styles.courseInfoName}>{name}</h3>
                    </div>
                    <button className={styles.closeBtn} onClick={(e) => { e.stopPropagation(); setShowInfo(false); }}>✕</button>
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

    /* ── Missing prerequisites modal ───────────── */
    const prereqModal = (): JSX.Element => {
        if (!showPrereqs) return <></>;
        const status = getStatus();
        if (!status || status.satisfied) return <></>;

        const groups = status.missing_groups ?? [];
        const allMissing = groups.flat();

        return (
            <div className={styles.prereqModal} onClick={e => e.stopPropagation()}>
                <div className={styles.prereqHeader}>
                    <div>
                        <p className={styles.prereqTitle}>Missing prerequisites</p>
                        <p className={styles.prereqSubtitle}>Click a course to mark it as completed</p>
                    </div>
                    <button className={styles.closeBtn} onClick={(e) => { e.stopPropagation(); setShowPrereqs(false); }}>✕</button>
                </div>

                <div className={styles.prereqBody}>
                    {groups.length > 0 ? groups.map((group, gi) => (
                        <div key={gi}>
                            {gi > 0 && <div className={styles.andDivider}>and</div>}
                            <div className={styles.prereqGroup}>
                                {group.map((prereq, pi) => (
                                    <React.Fragment key={prereq}>
                                        {pi > 0 && <span className={styles.orLabel}>or</span>}
                                        <button
                                            className={`${styles.prereqBtn} ${coursesTaken.has(prereq) ? styles.prereqBtnTaken : ''}`}
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                coursesTaken.has(prereq) ? removeCourse(prereq) : addCourse(prereq);
                                            }}
                                        >
                                            {coursesTaken.has(prereq) && <span className={styles.checkmark}>✓</span>}
                                            {prereq}
                                        </button>
                                    </React.Fragment>
                                ))}
                            </div>
                        </div>
                    )) : (
                        <p className={styles.prereqSubtitle}>{status.message}</p>
                    )}
                </div>

                {allMissing.length > 0 && (
                    <div className={styles.prereqFooter}>
                        <button
                            className={styles.markAllBtn}
                            onClick={(e) => { e.stopPropagation(); allMissing.forEach(c => addCourse(c)); }}
                        >
                            Mark all as completed
                        </button>
                    </div>
                )}
            </div>
        );
    };

    return (
        <>
            {courseInfoPopup()}
            {prereqModal()}
            <div className={`${styles.node} ${nodeStateClass()}`} onClick={handleNodeClick}>
                <div className={styles.nodeContent}>
                    <span className={styles.courseCode}>
                        {coursesTaken.has(course) && (
                            <span className={styles.checkBadge}>✓</span>
                        )}
                        {course}
                    </span>
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
