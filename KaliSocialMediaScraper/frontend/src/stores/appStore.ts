import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { AppState, Notification, User } from '@/types';

interface AppStore extends AppState {
  // Actions
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void;
  removeNotification: (id: string) => void;
  markNotificationAsRead: (id: string) => void;
  clearNotifications: () => void;
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useAppStore = create<AppStore>()(
  devtools(
    persist(
      (set) => ({
        // Initial state
        theme: 'dark',
        sidebarOpen: true,
        notifications: [],
        user: null,
        loading: false,
        error: null,

        // Actions
        setTheme: (theme) => {
          set({ theme });
          localStorage.setItem('theme', theme);
        },

        toggleSidebar: () => {
          set((state) => ({ sidebarOpen: !state.sidebarOpen }));
        },

        setSidebarOpen: (open) => {
          set({ sidebarOpen: open });
        },

        addNotification: (notification) => {
          const newNotification: Notification = {
            id: Date.now().toString(),
            timestamp: new Date().toISOString(),
            read: false,
            ...notification,
          };
          set((state) => ({
            notifications: [newNotification, ...state.notifications],
          }));
        },

        removeNotification: (id) => {
          set((state) => ({
            notifications: state.notifications.filter((n) => n.id !== id),
          }));
        },

        markNotificationAsRead: (id) => {
          set((state) => ({
            notifications: state.notifications.map((n) =>
              n.id === id ? { ...n, read: true } : n
            ),
          }));
        },

        clearNotifications: () => {
          set({ notifications: [] });
        },

        setUser: (user) => {
          set({ user });
        },

        setLoading: (loading) => {
          set({ loading });
        },

        setError: (error) => {
          set({ error });
        },

        clearError: () => {
          set({ error: null });
        },
      }),
      {
        name: 'app-store',
        partialize: (state) => ({
          theme: state.theme,
          sidebarOpen: state.sidebarOpen,
          user: state.user,
        }),
      }
    )
  )
); 