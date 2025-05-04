import {JSX, useState, useEffect} from "react";
import {BASE_URL} from "@/app/api";
import axios from "axios";
import Select from "react-select";
import makeAnimated from "react-select/animated";
import styles from './SetNUPath.module.css'
import useCourseFilterStore from "@/app/store/useCourseFilterStore";

interface AttributeData {
    tag: string;
    name: string;
}

interface AttributeOption {
    label: string,
    value: string
}

const SetNUPath = (): JSX.Element => {

    const setAttributes = useCourseFilterStore((s) => s.setAttributes);

    const [attributeOptions, setAttributeOptions] = useState<AttributeOption[]>([]);
    const [selected, setSelected] = useState<AttributeOption[]>([]);

    useEffect((): void => {
        const fetchAttributes = async () => {
            try {
                const url = `${BASE_URL}/api/attributes`;
                const response = await axios.get(url);
                setAttributeOptions(response.data.map((item: AttributeData): AttributeOption => {
                    return {
                        label: item.tag,
                        value: item.tag
                    }
                }));
            } catch (error) {
                console.error(error);
            }
        }
        fetchAttributes();
    },[])

    useEffect((): void => {
        const attributes: string[] = selected.map((option: AttributeOption) => option.value);
        setAttributes(attributes);
    },[selected])

    const animatedComponents = makeAnimated();

    return (
        <div className={styles.filterContainer}>
            <h2>NU Path</h2>
            <Select
                isMulti
                options={attributeOptions}
                components={animatedComponents}
                value={selected}
                onChange={(options): void => setSelected(options as AttributeOption[])}
            />
        </div>
    )

}

export default SetNUPath