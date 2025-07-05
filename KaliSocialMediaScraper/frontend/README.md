# Kali OSINT Platform - Frontend

Advanced OSINT Social Media Scraper Platform Frontend built with React, TypeScript, and Tailwind CSS.

## Features

### 🎨 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark Mode**: Toggle between light and dark themes
- **Professional Design**: Clean, modern interface with cyberpunk aesthetics
- **Accessibility**: WCAG compliant with keyboard navigation support

### 📊 Dashboard & Analytics
- **Real-time Statistics**: Live updates of investigation progress
- **Threat Scoring**: Visual indicators for threat levels
- **Progress Tracking**: Real-time progress bars for investigations
- **System Health**: Monitor platform status and performance

### 🔍 Investigation Management
- **Investigation Creation**: Start new OSINT investigations
- **Status Tracking**: Monitor investigation progress and status
- **Results Visualization**: Interactive charts and graphs
- **Export Capabilities**: Generate reports in multiple formats

### 📱 Social Media Analysis
- **Multi-platform Support**: Twitter, Facebook, Instagram, LinkedIn, etc.
- **Profile Analysis**: Deep dive into social media profiles
- **Post Analysis**: Sentiment and threat analysis of posts
- **Network Mapping**: Visualize social connections

### 🛡️ Threat Intelligence
- **Threat Assessment**: Automated threat scoring
- **Pattern Recognition**: Identify suspicious patterns
- **Anomaly Detection**: Flag unusual activities
- **Intelligence Fusion**: Correlate data across sources

### 📈 Advanced Analytics
- **Network Graphs**: Interactive network visualizations
- **Timeline Analysis**: Chronological event tracking
- **Geographic Mapping**: Location-based intelligence
- **Trend Analysis**: Historical pattern analysis

## Technology Stack

### Core Framework
- **React 18**: Latest React with concurrent features
- **TypeScript**: Type-safe development
- **React Router**: Client-side routing

### UI & Styling
- **Tailwind CSS**: Utility-first CSS framework
- **Heroicons**: Beautiful SVG icons
- **Framer Motion**: Smooth animations
- **Headless UI**: Accessible UI components

### State Management
- **React Query**: Server state management
- **Zustand**: Lightweight state management
- **React Hook Form**: Form handling

### Data Visualization
- **Recharts**: Chart library for React
- **D3.js**: Advanced data visualization
- **React Flow**: Network graph visualization
- **Three.js**: 3D visualizations

### Development Tools
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **TypeScript**: Type checking
- **Vite**: Fast development server

## Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Backend API running on localhost:8000

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start development server**
   ```bash
   npm start
   # or
   yarn start
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

### Build for Production

```bash
npm run build
# or
yarn build
```

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm lint` - Run ESLint
- `npm lint:fix` - Fix ESLint errors
- `npm format` - Format code with Prettier
- `npm type-check` - Run TypeScript type checking

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   ├── pages/             # Page components
│   ├── services/          # API services
│   ├── utils/             # Utility functions
│   ├── styles/            # Global styles
│   ├── assets/            # Images, fonts, etc.
│   ├── App.tsx           # Main app component
│   └── index.tsx         # Entry point
├── package.json           # Dependencies and scripts
├── tailwind.config.js    # Tailwind configuration
└── tsconfig.json         # TypeScript configuration
```

## Key Components

### Layout System
- **Responsive Sidebar**: Collapsible navigation
- **Header Bar**: User controls and notifications
- **Dark Mode Toggle**: Theme switching
- **Mobile Navigation**: Touch-friendly mobile menu

### Dashboard
- **Statistics Cards**: Key metrics display
- **Recent Investigations**: Latest activity
- **Quick Actions**: Common tasks
- **System Status**: Health monitoring

### Investigation Interface
- **Investigation Form**: Create new investigations
- **Progress Tracking**: Real-time updates
- **Results Display**: Findings visualization
- **Export Options**: Report generation

## API Integration

The frontend communicates with the backend API through:

- **RESTful Endpoints**: Standard HTTP methods
- **WebSocket Connections**: Real-time updates
- **File Uploads**: Report and data import
- **Authentication**: JWT token management

## Styling System

### Tailwind CSS Classes
- **Custom Components**: Pre-built component classes
- **Dark Mode**: Automatic theme switching
- **Responsive Design**: Mobile-first approach
- **Custom Animations**: Smooth transitions

### Color Scheme
- **Primary**: Blue (#0ea5e9)
- **Success**: Green (#22c55e)
- **Warning**: Yellow (#f59e0b)
- **Danger**: Red (#ef4444)
- **Neutral**: Gray scale

## Performance Optimizations

- **Code Splitting**: Lazy loading of components
- **Image Optimization**: WebP format support
- **Bundle Analysis**: Webpack bundle analyzer
- **Caching**: React Query caching
- **Virtual Scrolling**: Large data sets

## Security Features

- **Input Validation**: Client-side validation
- **XSS Protection**: React's built-in protection
- **CSRF Protection**: Token-based protection
- **Content Security Policy**: CSP headers

## Browser Support

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Contact the development team 