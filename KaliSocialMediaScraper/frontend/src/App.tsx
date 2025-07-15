import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './theme';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { Layout } from './components/layout/Layout';
import { ErrorBoundary } from './components/ErrorBoundary';

// Import pages
import { Dashboard } from './pages/Dashboard';
import { Investigations } from './pages/Investigations';
import { DomainAnalysis } from './pages/DomainAnalysis';
import { SocialMedia } from './pages/SocialMedia';
import { ThreatAnalysis } from './pages/ThreatAnalysis';
import { Reports } from './pages/Reports';
import { Settings } from './pages/Settings';

// Create a query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider>
          <Router>
            <Layout>
              <Routes>
                {/* Redirect root to dashboard */}
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                
                {/* Main routes */}
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/investigations" element={<Investigations />} />
                <Route path="/investigations/:id" element={<Investigations />} />
                <Route path="/domain-analysis" element={<DomainAnalysis />} />
                <Route path="/social-media" element={<SocialMedia />} />
                <Route path="/threat-analysis" element={<ThreatAnalysis />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="/settings" element={<Settings />} />
                
                {/* Catch all route */}
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </Layout>
            <Toaster 
              position="top-right" 
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#363636',
                  color: '#fff',
                },
              }}
            />
          </Router>
        </ThemeProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;
