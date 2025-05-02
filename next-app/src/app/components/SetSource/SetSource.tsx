import React, {JSX, useState, useEffect} from "react";
import styles from '@/app/components/SetSource/SetSource.module.css';
import useGraphStore from '@/app/store/useGraphStore';
import {BASE_URL} from "@/app/api";
import axios from "axios";


interface CourseResult {
    course: string,
    name: string
}



const SetSource = (): JSX.Element => {

    const setSource: (newSource: string) => void = useGraphStore(s => s.setSource);

    const [input, setInput] = useState<string>('');
    const [editingSource, setEditingSource] = useState<boolean>(false);
    const [sourceSelection, setSourceSelection] = useState<CourseResult>();
    const [closestResults, setClosestResults] = useState<CourseResult[]>([]);

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
    }

    const handleKeyDown = (e): void => {
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
                    <input value={input}
                           onChange={(e): void => setInput(e.target.value)}
                           onKeyDown={(e): void => handleKeyDown(e)}>
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
            <h2>{'Source Node'}</h2>
            <div className={styles.sourceRow}>
                {renderSource()}
                <div className={styles.buttonGroup}>
                    <button className={styles.editButton} onClick={handleEditClick}>{'✏️'}</button>
                    <button className={styles.clearButton} onClick={handleResetClick}>{'🗑️'}</button>
                </div>
            </div>
        </div>
    )
}

export default SetSource;