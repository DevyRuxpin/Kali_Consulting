import { useEffect, useRef, useState, useCallback } from 'react';
import { toast } from 'react-hot-toast';

interface WebSocketOptions {
  url: string;
  onMessage?: (data: any) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
  autoReconnect?: boolean;
}

export interface WebSocketMessage {
  type: 'investigation_update' | 'threat_alert' | 'system_status' | 'metric_update' | 'pong' | 'subscribed' | 'unsubscribed' | 'status_response' | 'error';
  data?: any;
  timestamp: string;
  investigation_id?: number;
}

export const useWebSocket = (options: WebSocketOptions) => {
  const {
    url,
    onMessage,
    onOpen,
    onClose,
    onError,
    reconnectAttempts = 5,
    reconnectInterval = 3000,
    autoReconnect = true,
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const [messageHistory, setMessageHistory] = useState<WebSocketMessage[]>([]);
  
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const shouldReconnectRef = useRef(autoReconnect);
  const pingIntervalRef = useRef<number | null>(null);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        reconnectAttemptsRef.current = 0;
        
        // Start ping interval
        pingIntervalRef.current = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'ping' }));
          }
        }, 30000); // Ping every 30 seconds
        
        onOpen?.();
      };

      ws.onmessage = (event) => {
        try {
          const data: WebSocketMessage = JSON.parse(event.data);
          setLastMessage(data);
          setMessageHistory(prev => [...prev.slice(-50), data]); // Keep last 50 messages
          onMessage?.(data);
          
          // Handle specific message types
          handleMessageType(data);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        
        // Clear ping interval
        if (pingIntervalRef.current) {
          clearInterval(pingIntervalRef.current);
          pingIntervalRef.current = null;
        }
        
        onClose?.();
        
        if (shouldReconnectRef.current && reconnectAttemptsRef.current < reconnectAttempts) {
          const delay = reconnectInterval * Math.pow(2, reconnectAttemptsRef.current);
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttemptsRef.current++;
            connect();
          }, delay);
        } else if (reconnectAttemptsRef.current >= reconnectAttempts) {
          setError('Max reconnection attempts reached');
        }
      };

      ws.onerror = (event) => {
        setError('WebSocket connection error');
        onError?.(event);
      };
    } catch (error) {
      setError('Failed to create WebSocket connection');
      console.error('WebSocket connection error:', error);
    }
  }, [url, onMessage, onOpen, onClose, onError, reconnectAttempts, reconnectInterval]);

  // Handle specific message types
  const handleMessageType = useCallback((message: WebSocketMessage) => {
    switch (message.type) {
      case 'threat_alert':
        toast.error(`Threat Alert: ${message.data?.description || 'New threat detected'}`);
        break;
      case 'investigation_update':
        toast.success(`Investigation ${message.investigation_id} updated`);
        break;
      case 'system_status':
        if (message.data?.status === 'critical') {
          toast.error('System critical status detected');
        }
        break;
      case 'error':
        toast.error(`WebSocket Error: ${message.data?.message || 'Unknown error'}`);
        break;
    }
  }, []);

  const disconnect = useCallback(() => {
    shouldReconnectRef.current = false;
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    if (pingIntervalRef.current) {
      clearInterval(pingIntervalRef.current);
      pingIntervalRef.current = null;
    }
    setIsConnected(false);
  }, []);

  const sendMessage = useCallback((message: any) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
      return true;
    }
    return false;
  }, []);

  const reconnect = useCallback(() => {
    shouldReconnectRef.current = true;
    reconnectAttemptsRef.current = 0;
    disconnect();
    connect();
  }, [disconnect, connect]);

  // Connect on mount
  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    isConnected,
    error,
    lastMessage,
    messageHistory,
    sendMessage,
    reconnect,
    disconnect,
  };
}; 