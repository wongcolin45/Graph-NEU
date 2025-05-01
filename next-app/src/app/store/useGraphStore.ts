
import { create } from 'zustand';

type GraphState = {
    source: string;
    setSource: (newSource: string) => void;
};

const useGraphStore = create<GraphState>((set) => ({
    source: '',
    setSource: (newSource: string) => set({ source: newSource }),
}));

export default useGraphStore;
