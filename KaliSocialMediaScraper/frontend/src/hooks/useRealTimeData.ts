import { useState, useEffect, useRef, useCallback } from 'react';
import { DashboardService, createWebSocketConnection } from '../services/api';

interface RealTimeData {
  timestamp: string;
  activeInvestigations: number;
  threatsDetected: number;
  entitiesMonitored: number;
  networkActivity: number;
  anomalyScore: number;
}

interface ThreatAlert {
  id: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  timestamp: string;
  entityId: string;
  confidence: number;
}

interface EntityActivity {
  id: string;
  name: string;
  platform: string;
  activityLevel: number;
  threatScore: number;
  lastSeen: string;
}

interface UseRealTimeDataOptions {
  enableWebSocket?: boolean;
  pollingInterval?: number;
  maxDataPoints?: number;
  autoReconnect?: boolean;
  reconnectDelay?: number;
}

interface UseRealTimeDataReturn {
  data: RealTimeData[];
  threatAlerts: ThreatAlert[];
  entityActivity: EntityActivity[];
  isConnected: boolean;
  isLoading: boolean;
  error: string | null;
  lastUpdate: Date;
  reconnect: () => void;
}

export const useRealTimeData = (options: UseRealTimeDataOptions = {}): UseRealTimeDataReturn => {
  const {
    enableWebSocket = true,
    pollingInterval = 5000,
    maxDataPoints = 50,
    autoReconnect = true,
    reconnectDelay = 3000
  } = options;

  const [data, setData] = useState<RealTimeData[]>([]);
  const [threatAlerts, setThreatAlerts] = useState<ThreatAlert[]>([]);
  const [entityActivity, setEntityActivity] = useState<EntityActivity[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  const wsRef = useRef<WebSocket | null>(null);
  const pollingRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Fetch data from API
  const fetchData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const realTimeData = await DashboardService.getRealTimeData();
      
      setData(prevData => {
        const newData = [...prevData, realTimeData];
        if (newData.length > maxDataPoints) {
          return newData.slice(-maxDataPoints);
        }
        return newData;
      });
      
      setLastUpdate(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch real-time data');
      console.error('Error fetching real-time data:', err);
    } finally {
      setIsLoading(false);
    }
  }, [maxDataPoints]);

  // Initialize WebSocket connection
  const initializeWebSocket = useCallback(() => {
    if (!enableWebSocket) return;

    try {
      const wsUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws';
      const ws = createWebSocketConnection(wsUrl);
      
      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        console.log('WebSocket connected');
      };
      
      ws.onclose = () => {
        setIsConnected(false);
        console.log('WebSocket disconnected');
        
        if (autoReconnect) {
          reconnectTimeoutRef.current = setTimeout(() => {
            console.log('Attempting to reconnect...');
            initializeWebSocket();
          }, reconnectDelay);
        }
      };
      
      ws.onerror = (event) => {
        setError('WebSocket connection error');
        console.error('WebSocket error:', event);
      };
      
      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          
          switch (message.type) {
            case 'real_time_data':
              setData(prevData => {
                const newData = [...prevData, message.data];
                if (newData.length > maxDataPoints) {
                  return newData.slice(-maxDataPoints);
                }
                return newData;
              });
              setLastUpdate(new Date());
              break;
              
            case 'threat_alert':
              setThreatAlerts(prev => [message.data, ...prev.slice(0, 9)]);
              break;
              
            case 'entity_activity':
              setEntityActivity(prev => {
                const updated = prev.filter(e => e.id !== message.data.id);
                return [message.data, ...updated.slice(0, 9)];
              });
              break;
              
            default:
              console.log('Unknown message type:', message.type);
          }
        } catch (err) {
          console.error('Error parsing WebSocket message:', err);
        }
      };
      
      wsRef.current = ws;
    } catch (err) {
      setError('Failed to initialize WebSocket connection');
      console.error('Error initializing WebSocket:', err);
    }
  }, [enableWebSocket, autoReconnect, reconnectDelay, maxDataPoints]);

  // Start polling
  const startPolling = useCallback(() => {
    if (enableWebSocket) return; // Don't poll if WebSocket is enabled
    
    pollingRef.current = setInterval(() => {
      fetchData();
    }, pollingInterval);
  }, [enableWebSocket, pollingInterval, fetchData]);

  // Stop polling
  const stopPolling = useCallback(() => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
  }, []);

  // Manual reconnect function
  const reconnect = useCallback(() => {
    // Clear existing connections
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    stopPolling();
    
    // Reinitialize connection
    if (enableWebSocket) {
      initializeWebSocket();
    } else {
      startPolling();
    }
  }, [enableWebSocket, initializeWebSocket, startPolling, stopPolling]);

  // Initialize on mount
  useEffect(() => {
    // Initial data fetch
    fetchData();
    
    // Start real-time updates
    if (enableWebSocket) {
      initializeWebSocket();
    } else {
      startPolling();
    }
    
    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      
      stopPolling();
    };
  }, [enableWebSocket, fetchData, initializeWebSocket, startPolling, stopPolling]);

  return {
    data,
    threatAlerts,
    entityActivity,
    isConnected,
    isLoading,
    error,
    lastUpdate,
    reconnect
  };
}; 