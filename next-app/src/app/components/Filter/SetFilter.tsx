'use client';
import {JSX, useEffect, useState} from "react";
import styles from './SetFilter.module.css';
import {BASE_URL} from "@/app/api";
import axios from "axios";


interface DepartmentInfo {
    prefix: string,
    name: string
}


const SetFilter = (): JSX.Element => {

    const [selected, setSelected] = useState<string>('');
    const [departments, setDepartments] = useState<DepartmentInfo[]>([]);
    const [departmentSelection, setDepartmentSelection] = useState<DepartmentInfo>();
    const [editingDepartment, setEditingDepartment] = useState<boolean>(false);

    useEffect(() => {
        const updateDepartments = async () => {
            try {
                const url = `${BASE_URL}/api/departments/all`;
                const response = await axios.get(url);
                setDepartments(response.data);
            } catch (error) {
                console.error(error);
            }
        }
        updateDepartments();
    },[])


    const handleDropdownClick = (item: DepartmentInfo): void => {
        setDepartmentSelection(item);
        setEditingDepartment(false)
    }

    const renderInputSection = (): JSX.Element => {
        return (
            <div> 
                <select
                    id="department"
                    value={selected}
                    onChange={(e) => setSelected(e.target.value)}
                >
                    <option value="">-- Select Department --</option>
                    {departments.map((info: DepartmentInfo, index: number) => (
                        <option key={index} value={info.name}>
                            {`${info.prefix}: ${info.name}`}
                        </option>
                    ))}
                </select>
            </div>
        );
    }


    return (
        <div className={styles.setFilter}>
            <h2>Filters</h2>
            <h4>Department</h4>
            {renderInputSection()}

        </div>
    )
}

export default SetFilter