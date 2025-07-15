import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { Notification } from '../types';

interface NotificationState {
  notifications: Notification[];
  unreadCount: number;
  settings: {
    enabled: boolean;
    sound: boolean;
    desktop: boolean;
    autoClear: boolean;
    clearAfter: number; // minutes
  };
}

interface NotificationActions {
  // State setters
  setNotifications: (notifications: Notification[]) => void;
  setUnreadCount: (count: number) => void;
  setSettings: (settings: Partial<NotificationState['settings']>) => void;
  
  // Actions
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void;
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  removeNotification: (id: string) => void;
  clearAll: () => void;
  clearOld: () => void;
  
  // Computed
  getUnreadNotifications: () => Notification[];
  getNotificationsByType: (type: Notification['type']) => Notification[];
}

export const useNotificationStore = create<NotificationState & NotificationActions>()(
  devtools(
    persist(
      (set, get) => ({
        // Initial state
        notifications: [],
        unreadCount: 0,
        settings: {
          enabled: true,
          sound: true,
          desktop: true,
          autoClear: true,
          clearAfter: 30, // 30 minutes
        },

        // Actions
        setNotifications: (notifications) => {
          const unreadCount = notifications.filter(n => !n.read).length;
          set({ notifications, unreadCount });
        },

        setUnreadCount: (count) => set({ unreadCount: count }),

        setSettings: (settings) => set((state) => ({
          settings: { ...state.settings, ...settings }
        })),

        addNotification: (notification) => {
          const newNotification: Notification = {
            id: Date.now().toString(),
            timestamp: new Date().toISOString(),
            read: false,
            ...notification,
          };

          set((state) => {
            const newNotifications = [newNotification, ...state.notifications];
            const unreadCount = newNotifications.filter(n => !n.read).length;
            return {
              notifications: newNotifications,
              unreadCount,
            };
          });

          // Auto-clear old notifications if enabled
          const { settings } = get();
          if (settings.autoClear) {
            setTimeout(() => {
              get().clearOld();
            }, settings.clearAfter * 60 * 1000);
          }
        },

        markAsRead: (id) => set((state) => {
          const updatedNotifications = state.notifications.map((n) =>
            n.id === id ? { ...n, read: true } : n
          );
          const unreadCount = updatedNotifications.filter(n => !n.read).length;
          return { notifications: updatedNotifications, unreadCount };
        }),

        markAllAsRead: () => set((state) => {
          const updatedNotifications = state.notifications.map((n) => ({
            ...n,
            read: true,
          }));
          return { notifications: updatedNotifications, unreadCount: 0 };
        }),

        removeNotification: (id) => set((state) => {
          const updatedNotifications = state.notifications.filter((n) => n.id !== id);
          const unreadCount = updatedNotifications.filter(n => !n.read).length;
          return { notifications: updatedNotifications, unreadCount };
        }),

        clearAll: () => set({ notifications: [], unreadCount: 0 }),

        clearOld: () => set((state) => {
          const { settings } = state;
          const cutoffTime = new Date(Date.now() - settings.clearAfter * 60 * 1000);
          const updatedNotifications = state.notifications.filter((n) => {
            const notificationTime = new Date(n.timestamp);
            return notificationTime > cutoffTime;
          });
          const unreadCount = updatedNotifications.filter(n => !n.read).length;
          return { notifications: updatedNotifications, unreadCount };
        }),

        // Computed
        getUnreadNotifications: () => {
          const { notifications } = get();
          return notifications.filter(n => !n.read);
        },

        getNotificationsByType: (type) => {
          const { notifications } = get();
          return notifications.filter(n => n.type === type);
        },
      }),
      {
        name: 'notification-store',
        partialize: (state) => ({
          notifications: state.notifications,
          settings: state.settings,
        }),
      }
    )
  )
); 