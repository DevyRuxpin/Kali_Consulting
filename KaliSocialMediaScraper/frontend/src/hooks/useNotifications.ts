import { useEffect } from 'react';
import { useNotificationStore } from '../stores/notificationStore';
import type { Notification } from '../types';

export const useNotifications = () => {
  const {
    notifications,
    unreadCount,
    settings,
    addNotification,
    markAsRead,
    markAllAsRead,
    removeNotification,
    clearAll,
    setSettings,
  } = useNotificationStore();

  // Request notification permission on mount
  useEffect(() => {
    if (settings.enabled && settings.desktop && 'Notification' in window) {
      if (Notification.permission === 'default') {
        Notification.requestPermission();
      }
    }
  }, [settings.enabled, settings.desktop]);

  // Show desktop notification
  const showDesktopNotification = (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    if (settings.enabled && settings.desktop && 'Notification' in window && Notification.permission === 'granted') {
      new Notification(notification.title, {
        body: notification.message,
        icon: '/favicon.ico',
        // tag: notification.id, // Remove or replace with a valid property
      });
    }
  };

  // Add notification with desktop notification
  const addNotificationWithDesktop = (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    addNotification(notification);
    showDesktopNotification(notification);
  };

  // Play notification sound
  const playNotificationSound = () => {
    if (settings.enabled && settings.sound) {
      try {
        const audio = new Audio('/notification.mp3');
        audio.play().catch(() => {
          // Fallback: create a simple beep
          const context = new (window.AudioContext || (window as any).webkitAudioContext)();
          const oscillator = context.createOscillator();
          const gainNode = context.createGain();
          
          oscillator.connect(gainNode);
          gainNode.connect(context.destination);
          
          oscillator.frequency.value = 800;
          gainNode.gain.value = 0.1;
          
          oscillator.start();
          setTimeout(() => oscillator.stop(), 200);
        });
      } catch (error) {
        console.warn('Could not play notification sound:', error);
      }
    }
  };

  // Add notification with sound
  const addNotificationWithSound = (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    addNotification(notification);
    playNotificationSound();
  };

  // Add notification with both desktop and sound
  const addNotificationComplete = (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    addNotification(notification);
    showDesktopNotification(notification);
    playNotificationSound();
  };

  return {
    notifications,
    unreadCount,
    settings,
    addNotification,
    addNotificationWithDesktop,
    addNotificationWithSound,
    addNotificationComplete,
    markAsRead,
    markAllAsRead,
    removeNotification,
    clearAll,
    setSettings,
    playNotificationSound,
  };
}; 