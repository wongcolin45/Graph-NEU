import { create } from 'zustand';

type UserDataState = {
    coursesTaken: Set<string>;
    addCourse: (course: string) => void;
    removeCourse: (course: string) => void;
};

const useUserDataStore = create<UserDataState>((set) => ({
    coursesTaken: new Set<string>(),

    addCourse: (course: string) =>
        set((state) => {
            const updated = new Set(state.coursesTaken);
            updated.add(course);
            return { coursesTaken: updated };
        }),

    removeCourse: (course: string) =>
        set((state) => {
            const updated = new Set(state.coursesTaken);
            updated.delete(course);
            return { coursesTaken: updated };
        }),
}));

export default useUserDataStore;
