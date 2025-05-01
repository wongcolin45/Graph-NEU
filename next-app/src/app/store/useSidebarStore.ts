
import { create } from 'zustand';

type SidebarState = {
    sidebarOpen: boolean;
    toggleSidebar: () => void;
};

const useSidebarStore = create<SidebarState>((set,get) => ({
    sidebarOpen: false,
    toggleSidebar: () => set({ sidebarOpen: !get().sidebarOpen }),
}));

export default useSidebarStore;
