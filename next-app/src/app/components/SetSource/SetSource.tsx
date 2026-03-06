import React, {JSX, useState, useEffect} from "react";
import styles from '@/app/components/SetSource/SetSource.module.css';
import useGraphStore from '@/app/store/useGraphStore';
import {BASE_URL} from "@/app/api";
import axios from "axios";
import {useRouter} from "next/navigation";


interface CourseResult {
    course: string,
    name: string
}



const SetSource = (): JSX.Element => {

    const setSource: (newSource: string) => void = useGraphStore(s => s.setSource);
    const source: string = useGraphStore(s => s.source);
    const router = useRouter();

    const [input, setInput] = useState<string>('');
    const [editingSource, setEditingSource] = useState<boolean>(false);
    const [sourceSelection, setSourceSelection] = useState<CourseResult>();
    const [closestResults, setClosestResults] = useState<CourseResult[]>([]);

    // Sync sidebar display when source is set externally (e.g. direct URL navigation)
    useEffect((): void => {
        if (!source) { setSourceSelection(undefined); return; }
        if (sourceSelection?.course === source) return;
        const fetchCourse = async (): Promise<void> => {
            try {
                const url = `${BASE_URL}/api/course/search/${encodeURIComponent(source)}/1`;
                const response = await axios.get(url);
                if (response.data.length > 0) {
                    setSourceSelection(response.data[0]);
                }
            } catch (error) {
                console.error(error);
            }
        };
        fetchCourse();
    }, [source]);

    useEffect((): void => {
        const updateClosestResults: () => void = async (): Promise<void> => {
            try {
                const limit: number = 10;
                const url = `${BASE_URL}/api/course/search/${input}/${limit}`;
                const response = await axios.get(url);
                setClosestResults(response.data);
            } catch (error) {
                console.error(error);
            }
        }

        if (input) {
            updateClosestResults();
        }


    }, [input]);

    useEffect((): void => {
        console.log("checking editing source "+editingSource);
        setInput('');
        if (editingSource) {
            console.log('set input to 0');
        } else {
            setClosestResults([]);
        }
    },[editingSource])


    const handleDropdownClick = (result: CourseResult): void => {
        setSource(result.course);
        setEditingSource(false);
        setSourceSelection(result);
        router.push(`/explore/${encodeURIComponent(result.course)}`);
    }

    const handleKeyDown = (e: React.KeyboardEvent): void => {
        if (e.key === 'Enter') {
            setEditingSource(false)
        }
    }

    const handleEditClick = (): void => {
        setEditingSource(prev => !prev);
    }

    const handleResetClick = (): void => {
        setInput('');
        setSource('');
        setSourceSelection(undefined);
        router.push('/explore');
    }


    const showClosestResults = (): JSX.Element => {
        if (closestResults.length === 0) {
            return <></>
        }
        return (
            <ul className={styles.dropdown}>
                {
                    closestResults.map((item: CourseResult, index: number) => {
                        const name = `${item.course.replace(/([a-zA-Z])(\d)/g, "$1 $2")}: ${item.name}`;
                        return <li key={index} onClick={() => handleDropdownClick(item)}>{name}</li>
                    })
                }
            </ul>
        )
    }

    const renderSource = (): JSX.Element => {
        if (editingSource) {
            return (
                <div className={styles.inputContainer}>
                    <input
                            value={input}
                           onChange={(e): void => setInput(e.target.value)}
                           onKeyDown={(e: React.KeyboardEvent): void => handleKeyDown(e)}>
                    </input>
                    {showClosestResults()}
                </div>
            )
        }

        if (sourceSelection === undefined) {
            return (
                <span className={styles.unselectedSource}>
                    {'N/A'}
                </span>
            )
        }

        const {course, name} = sourceSelection;

        return (
            <span className={styles.sourceSelection}>
                <strong>{`${course}: `}</strong>{name}
            </span>
        )
    }

    return (
        <div className={styles.setSource}>
            <h2>{'Root Node'}</h2>
            <div className={styles.sourceRow}>
                {renderSource()}

            </div>
            <div className={styles.buttonGroup}>
                <button className={styles.editButton} onClick={handleEditClick}>{'Edit'}</button>
                <button className={styles.clearButton} onClick={handleResetClick}>{'Clear'}</button>
            </div>
        </div>
    )
}

export default SetSource;