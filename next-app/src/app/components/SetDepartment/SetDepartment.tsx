'use client';
import {JSX, useEffect, useState} from "react";
import styles from './SetDepartment.module.css';
import {BASE_URL} from "@/app/api";
import axios from "axios";
import Select from '../ClientSelect';
import makeAnimated from 'react-select/animated';
import useCourseFilterStore from "@/app/store/useCourseFilterStore";

interface DepartmentData {
    prefix: string,
    name: string
}

interface DepartmentOption {
    label: string,
    value: string
}


const SetDepartment = (): JSX.Element => {

    // const departments: Set<string> = useCourseFilterStore((s) => s.departments);
    const setDepartments = useCourseFilterStore((s) => s.setDepartments)


    const [selected, setSelected] = useState<DepartmentOption[]>([]);
    const [departmentOptions, setDepartmentOptions] = useState<DepartmentOption[]>([]);

    useEffect(() => {
        const updateDepartments = async () => {
            try {
                const url = `${BASE_URL}/api/departments/all`;
                const response = await axios.get(url);
                const data: DepartmentData[] = response.data;
                const options: DepartmentOption[] = data.map((data): DepartmentOption => {
                    return {label: `${data.prefix}: ${data.name}`, value: data.prefix};
                });
                setDepartmentOptions(options);
            } catch (error) {
                console.error(error);
            }
        }
        updateDepartments();
    },[])

    useEffect(() => {
        const newDepartments: string[] = selected.map((option: DepartmentOption): string => {
            return option.value;
        })
        setDepartments(newDepartments);
    }, [selected]);

    const animatedComponents = makeAnimated();

    const renderDepartments= (): JSX.Element => {
        return (
            <div>
                <h2>Departments</h2>
                <Select
                    isMulti
                    options={departmentOptions}
                    components={animatedComponents}
                    value={selected}
                    onChange={(options) => setSelected(options as DepartmentOption[])}
                />
            </div>
        )
    }

    return (
        <div className={styles.setFilter}>
            {renderDepartments()}
        </div>
    )
}

export default SetDepartment