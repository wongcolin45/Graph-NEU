import { create } from 'zustand';

type CourseFilterState = {
    departments: Set<string>;
    setDepartments: (departments: string[]) => void;
    minCourseID: number;
    maxCourseID: number;
    setMinCourseID: (minCourseCode: number) => void;
    setMaxCourseID: (maxCourseCode: number) => void;
};

const useCourseFilterStore = create<CourseFilterState>((set) => ({

    departments: new Set<string>(),
    setDepartments: (departments: string[]): void => {
        const newDepartments = new Set(departments);
        set({ departments: newDepartments });
    },

    minCourseID: 0,
    maxCourseID: 8000,
    setMinCourseID: (minCourseCode: number) => {set({ minCourseID: minCourseCode })},
    setMaxCourseID: (maxCourseCode: number) => {set({ maxCourseID: maxCourseCode })}
}));

export default useCourseFilterStore;
