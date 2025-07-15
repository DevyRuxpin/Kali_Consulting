import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { Investigation } from '../types';

interface InvestigationState {
  investigations: Investigation[];
  currentInvestigation: Investigation | null;
  loading: boolean;
  error: string | null;
  filters: {
    status: string;
    targetType: string;
    dateRange: { start: string; end: string } | null;
  };
}

interface InvestigationActions {
  // State setters
  setInvestigations: (investigations: Investigation[]) => void;
  setCurrentInvestigation: (investigation: Investigation | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setFilters: (filters: Partial<InvestigationState['filters']>) => void;
  
  // Actions
  addInvestigation: (investigation: Investigation) => void;
  updateInvestigation: (id: string, updates: Partial<Investigation>) => void;
  deleteInvestigation: (id: string) => void;
  clearError: () => void;
  resetFilters: () => void;
  
  // Computed
  getFilteredInvestigations: () => Investigation[];
  getInvestigationById: (id: string) => Investigation | undefined;
}

export const useInvestigationStore = create<InvestigationState & InvestigationActions>()(
  devtools(
    persist(
      (set, get) => ({
        // Initial state
        investigations: [],
        currentInvestigation: null,
        loading: false,
        error: null,
        filters: {
          status: '',
          targetType: '',
          dateRange: null,
        },

        // Actions
        setInvestigations: (investigations) => set({ investigations }),
        setCurrentInvestigation: (investigation) => set({ currentInvestigation: investigation }),
        setLoading: (loading) => set({ loading }),
        setError: (error) => set({ error }),
        setFilters: (filters) => set((state) => ({ 
          filters: { ...state.filters, ...filters } 
        })),

        addInvestigation: (investigation) => set((state) => ({
          investigations: [investigation, ...state.investigations],
        })),

        updateInvestigation: (id, updates) => set((state) => ({
          investigations: state.investigations.map((inv) =>
            String(inv.id) === String(id) ? { ...inv, ...updates } : inv
          ),
          currentInvestigation: String(state.currentInvestigation?.id) === String(id)
            ? { ...(state.currentInvestigation as Investigation), ...updates }
            : state.currentInvestigation,
        })),

        deleteInvestigation: (id) => set((state) => ({
          investigations: state.investigations.filter((inv) => String(inv.id) !== String(id)),
          currentInvestigation: String(state.currentInvestigation?.id) === String(id)
            ? null
            : state.currentInvestigation,
        })),

        clearError: () => set({ error: null }),
        resetFilters: () => set({ 
          filters: { status: '', targetType: '', dateRange: null } 
        }),

        // Computed
        getFilteredInvestigations: () => {
          const { investigations, filters } = get();
          return investigations.filter((inv) => {
            if (filters.status && inv.status !== filters.status) return false;
            if (filters.targetType && inv.target_type !== filters.targetType) return false;
            if (filters.dateRange) {
              const invDate = new Date(inv.created_at);
              const startDate = new Date(filters.dateRange.start);
              const endDate = new Date(filters.dateRange.end);
              if (invDate < startDate || invDate > endDate) return false;
            }
            return true;
          });
        },

        getInvestigationById: (id) => {
          const { investigations } = get();
          return investigations.find((inv) => String(inv.id) === String(id));
        },
      }),
      {
        name: 'investigation-store',
        partialize: (state) => ({
          investigations: state.investigations,
          currentInvestigation: state.currentInvestigation,
          filters: state.filters,
        }),
      }
    )
  )
); 