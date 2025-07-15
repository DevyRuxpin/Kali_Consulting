# Kali OSINT Frontend

> **Commercial-Grade React Frontend for OSINT Investigation Platform**

## 🎯 Overview

This is the frontend application for the Kali OSINT Investigation Platform, built with React 19, TypeScript, and Material-UI. The application provides a modern, responsive interface for comprehensive OSINT investigations.

## 🏗️ Tech Stack

### Core Framework
- **React 19**: Latest React with concurrent features
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and development server

### UI Framework
- **Material-UI 7**: Professional component library
- **Emotion**: CSS-in-JS styling
- **Material Icons**: Comprehensive icon set

### State Management
- **Zustand**: Lightweight state management
- **React Query**: Server state management
- **React Hook Form**: Form handling

### Routing & Navigation
- **React Router DOM**: Client-side routing

### Utilities
- **Axios**: HTTP client for API communication
- **React Hot Toast**: Toast notifications
- **Date-fns**: Date manipulation
- **Yup**: Schema validation
- **Recharts**: Data visualization

## 📦 Optimized Dependencies

### Removed (Unused)
- `@hookform/resolvers` - Not currently used
- `d3` & `@types/d3` - Replaced with Recharts
- `framer-motion` - Not currently used
- `lodash-es` & `@types/lodash-es` - Not currently used
- `react-intersection-observer` - Not currently used
- `react-window` & `@types/react-window` - Not currently used
- `react-virtualized-auto-sizer` - Not currently used

### Added (Missing)
- `prettier` - Code formatting
- `vitest` & `@vitest/ui` - Modern testing framework
- Enhanced scripts for development workflow

## 🚀 Development

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation
```bash
npm install
```

### Development Scripts
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check

# Linting
npm run lint

# Code formatting
npm run format

# Run tests
npm run test

# Run tests with UI
npm run test:ui
```

## 🏗️ Project Structure

```
src/
├── components/          # Reusable UI components
│   └── layout/         # Layout components
├── hooks/              # Custom React hooks
├── pages/              # Page components
├── services/           # API services
├── stores/             # Zustand stores
├── theme/              # Material-UI theme
├── types/              # TypeScript type definitions
├── utils/              # Utility functions
├── App.tsx             # Main app component
└── main.tsx           # App entry point
```

## 🎨 Features

### Core Functionality
- **Authentication**: JWT-based auth with refresh tokens
- **Real-time Updates**: WebSocket integration for live data
- **File Management**: Upload/download with progress tracking
- **Analytics**: Advanced data visualization and analysis
- **Responsive Design**: Mobile-first approach

### Development Features
- **Hot Reloading**: Instant feedback during development
- **Type Safety**: Full TypeScript coverage
- **Code Quality**: ESLint + Prettier configuration
- **Testing**: Vitest for unit and integration tests

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_APP_NAME=Kali OSINT Platform
```

### Vite Configuration
The project uses Vite with React plugin for fast development and optimized builds.

## 📊 Performance Optimizations

- **Code Splitting**: Automatic route-based code splitting
- **Tree Shaking**: Unused code elimination
- **Bundle Analysis**: Built-in bundle analyzer
- **Caching**: Optimized caching strategies

## 🧪 Testing

The project uses Vitest for testing:

```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test -- --watch

# Run tests with UI
npm run test:ui
```

## 📦 Build & Deployment

### Production Build
```bash
npm run build
```

The build output will be in the `dist/` directory, optimized for production deployment.

### Deployment
The application can be deployed to any static hosting service:
- Vercel
- Netlify
- AWS S3
- GitHub Pages

## 🔍 Code Quality

### Linting
ESLint is configured with React-specific rules and TypeScript support.

### Formatting
Prettier is configured for consistent code formatting.

### Type Checking
TypeScript provides compile-time type checking.

## 🚀 Performance Monitoring

The application includes:
- Bundle size monitoring
- Performance metrics
- Error tracking
- User analytics

## 📚 Documentation

- **API Documentation**: Available at `/docs` when backend is running
- **Component Library**: Material-UI components with custom theme
- **Type Definitions**: Comprehensive TypeScript types

## 🤝 Contributing

1. Follow the established code style
2. Write tests for new features
3. Update documentation as needed
4. Use conventional commit messages

## 📄 License

This project is part of the Kali OSINT Investigation Platform.
