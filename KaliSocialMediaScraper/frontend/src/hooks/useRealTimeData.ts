import { useEffect, useRef, useState } from 'react';
import { useDashboardStore } from '../stores/dashboardStore';
import { createWebSocketConnection } from '../services/api';

interface RealTimeData {
  type: 'investigation_update' | 'threat_alert' | 'system_status' | 'metric_update';
  data: any;
  timestamp: string;
}

export const useRealTimeData = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<RealTimeData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const maxReconnectAttempts = 5;

  const { setSystemHealth, setRealTimeMetrics } = useDashboardStore();

  const connect = () => {
    try {
      const ws = createWebSocketConnection();
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        reconnectAttemptsRef.current = 0;
        console.log('WebSocket connected');
      };

      ws.onmessage = (event) => {
        try {
          const message: RealTimeData = JSON.parse(event.data);
          setLastMessage(message);

          // Handle different message types
          switch (message.type) {
            case 'investigation_update':
              // Update investigation data
              break;
            case 'threat_alert':
              // Show threat notification
              break;
            case 'system_status':
              setSystemHealth(message.data);
              break;
            case 'metric_update':
              setRealTimeMetrics(message.data);
              break;
            default:
              console.log('Unknown message type:', message.type);
          }
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      ws.onclose = (event) => {
        setIsConnected(false);
        console.log('WebSocket disconnected:', event.code, event.reason);
        
        // Attempt to reconnect
        if (reconnectAttemptsRef.current < maxReconnectAttempts) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000);
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttemptsRef.current++;
            connect();
          }, delay);
        } else {
          setError('Failed to reconnect to real-time data feed');
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setError('WebSocket connection error');
      };
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      setError('Failed to establish real-time connection');
    }
  };

  const disconnect = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    setIsConnected(false);
  };

  const sendMessage = (message: any) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  // Connect on mount
  useEffect(() => {
    connect();

    // Cleanup on unmount
    return () => {
      disconnect();
    };
  }, []);

  // Manual reconnect
  const reconnect = () => {
    disconnect();
    reconnectAttemptsRef.current = 0;
    connect();
  };

  return {
    isConnected,
    lastMessage,
    error,
    reconnect,
    sendMessage,
  };
}; 