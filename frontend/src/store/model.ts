import { create } from "zustand";
import { persist } from "zustand/middleware";

interface ModelStore {
  activeModelKey: string;
  setActiveModel: (key: string) => void;
}

export const useModelStore = create<ModelStore>()(
  persist(
    (set) => ({
      activeModelKey: "ollama-phi3",
      setActiveModel: (key) => set({ activeModelKey: key }),
    }),
    { name: "overlay-model" }
  )
);
