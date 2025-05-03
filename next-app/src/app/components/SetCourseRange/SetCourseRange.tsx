// RangeSlider.tsx
import { useState, useEffect } from "react";
import Slider from "@mui/material/Slider";
import Box from "@mui/material/Box";
import styles from "./SetCourseRange.module.css";
import useCourseFilterStore from "@/app/store/useCourseFilterStore";

const marks = Array.from({ length: 11 }, (_, i) => ({
    value: i * 1000,
    label: `${i * 1000}`
}));

const SetCourseRange = () => {

    const setMinCourseID = useCourseFilterStore((s) => s.setMinCourseID);
    const setMaxCourseID = useCourseFilterStore((s) => s.setMaxCourseID);

    const [value, setValue] = useState<number[]>([0, 8000]);

    useEffect(() => {
        setMinCourseID(value[0]);
        setMaxCourseID(value[1]);
    }, [value]);

    const handleChange = (_event: Event, newValue: number | number[]) => {
        setValue(newValue as number[]);
    };

    return (
        <div className={styles.setCourseRange}>
            <h2>Course ID Range</h2>
            <Box sx={{ width: '330px', marginLeft: '10px' }}>
                <Slider
                    value={value}
                    onChange={handleChange}
                    valueLabelDisplay="auto"
                    min={0}
                    max={8000}
                    step={1000}
                    marks={marks}
                    disableSwap
                />
             </Box>
        </div>
    );
}
// npm install @mui/material @emotion/react @emotion/styled
export default SetCourseRange;

