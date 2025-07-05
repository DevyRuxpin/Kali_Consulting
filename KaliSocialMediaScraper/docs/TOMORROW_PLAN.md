# Tomorrow's Plan: Complete Platform Setup

## 🎯 Objective
Get the Kali OSINT Social Media Scraper Platform fully functional with both backend and frontend running successfully in the browser.

## 📊 Current Status Assessment

### ✅ What's Working
- **Backend**: FastAPI server can start and respond to health checks
- **Database**: PostgreSQL connection established
- **Core Services**: All major services implemented and importable
- **API Structure**: Complete API endpoint structure in place
- **Dependencies**: Most Python dependencies installed successfully

### ❌ What's Broken
- **Frontend**: React app cannot start due to `ajv` dependency conflicts
- **Background Tasks**: Celery workers not configured
- **Database**: Some tables may not be created
- **Full Stack**: Backend-frontend communication not tested

## 🚀 Tomorrow's Action Plan

### Phase 1: Frontend Dependency Resolution (Priority 1)

#### 1.1 Complete Frontend Clean Install
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --legacy-peer-deps
```

#### 1.2 Fix ajv Dependency Issues
- **Problem**: `Cannot find module 'ajv/dist/compile/codegen'`
- **Solution**: Install specific ajv version and resolve conflicts
```bash
npm install ajv@^8.17.1 --save
npm install ajv-keywords@^5.1.0 --save
```

#### 1.3 Resolve Package Conflicts
- Check for conflicting peer dependencies
- Update problematic packages to compatible versions
- Use `--force` if necessary for critical packages

#### 1.4 Test Frontend Startup
```bash
npm start
```
- Verify React app starts without errors
- Check if development server runs on port 3000
- Test basic page loading

### Phase 2: Backend Infrastructure Setup (Priority 2)

#### 2.1 Database Setup Verification
```bash
# Check PostgreSQL connection
python3 -c "from app.core.database import engine; print('Database connected')"

# Run database migrations
alembic upgrade head

# Verify tables created
python3 -c "from app.models.database import Base; from app.core.database import engine; Base.metadata.create_all(bind=engine)"
```

#### 2.2 Redis Setup
```bash
# Start Redis server
brew services start redis

# Test Redis connection
python3 -c "import redis; r = redis.Redis(); print('Redis connected:', r.ping())"
```

#### 2.3 Celery Worker Configuration
```bash
# Start Celery worker
celery -A app.core.celery_app worker --loglevel=info

# Test Celery in separate terminal
python3 -c "from app.core.celery_app import celery_app; result = celery_app.send_task('app.tasks.investigation_tasks.test_task'); print('Celery working:', result.id)"
```

### Phase 3: Full Stack Integration (Priority 3)

#### 3.1 Backend Server Startup
```bash
# Start backend with proper configuration
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3.2 Frontend Server Startup
```bash
cd frontend
npm start
```

#### 3.3 Integration Testing
- Test backend health endpoint: `curl http://localhost:8000/health`
- Test frontend loading: `curl http://localhost:3000`
- Test API documentation: Open `http://localhost:8000/docs`
- Test frontend-backend communication

### Phase 4: Advanced Features Enablement (Priority 4)

#### 4.1 Enable Commented Dependencies
- Uncomment `networkit` in requirements.txt
- Test installation: `pip install networkit`
- If successful, enable in code

#### 4.2 Test Advanced Services
```python
# Test GitHub scraper
python3 -c "from app.services.github_scraper import GitHubScraper; scraper = GitHubScraper(); print('GitHub scraper ready')"

# Test social media scraper
python3 -c "from app.services.social_media_scraper import SocialMediaScraper; scraper = SocialMediaScraper(); print('Social media scraper ready')"

# Test intelligence engine
python3 -c "from app.services.intelligence_engine import IntelligenceEngine; engine = IntelligenceEngine(); print('Intelligence engine ready')"
```

#### 4.3 Database Integration Testing
```python
# Test database operations
python3 -c "from app.repositories.investigation_repository import InvestigationRepository; repo = InvestigationRepository(); print('Repository ready')"
```

### Phase 5: User Experience Testing (Priority 5)

#### 5.1 Browser Testing
- Open `http://localhost:3000` in browser
- Test all major pages:
  - Dashboard
  - Investigations
  - Social Media
  - Analysis
  - Reports
  - Settings

#### 5.2 API Testing
- Test all major endpoints via Swagger UI
- Verify data flow between frontend and backend
- Test investigation creation and monitoring

#### 5.3 Error Handling
- Test error scenarios
- Verify proper error messages
- Check logging functionality

## 🔧 Technical Solutions for Known Issues

### Frontend Issues

#### Issue 1: ajv Module Resolution
**Root Cause**: Version conflicts between ajv and ajv-keywords
**Solution**:
```bash
npm uninstall ajv ajv-keywords
npm install ajv@^8.17.1 ajv-keywords@^5.1.0
```

#### Issue 2: React Scripts Compatibility
**Root Cause**: React Scripts version conflicts
**Solution**:
```bash
npm install react-scripts@5.0.1 --save
```

#### Issue 3: TypeScript Configuration
**Root Cause**: TypeScript version conflicts
**Solution**:
```bash
npm install typescript@^4.7.4 --save-dev
```

### Backend Issues

#### Issue 1: Database Connection
**Root Cause**: Missing database user or permissions
**Solution**:
```sql
-- Run in PostgreSQL
CREATE USER kali_user WITH PASSWORD 'kali_password';
CREATE DATABASE kali_osint_db OWNER kali_user;
GRANT ALL PRIVILEGES ON DATABASE kali_osint_db TO kali_user;
```

#### Issue 2: Celery Configuration
**Root Cause**: Redis not running or Celery not configured
**Solution**:
```bash
# Start Redis
brew services start redis

# Start Celery worker
celery -A app.core.celery_app worker --loglevel=info
```

#### Issue 3: Import Errors
**Root Cause**: Python path issues
**Solution**:
```bash
# Run from project root
export PYTHONPATH="${PYTHONPATH}:/Users/marcharriman/Desktop/KaliSocialMediaScraper"
```

## 📋 Success Criteria

### Minimum Viable Product (MVP)
- [ ] Frontend starts without errors
- [ ] Backend responds to health checks
- [ ] Database connection established
- [ ] Basic API endpoints working
- [ ] Frontend can communicate with backend
- [ ] User can access dashboard in browser

### Full Functionality
- [ ] All pages load correctly
- [ ] Investigation creation works
- [ ] Social media scraping functional
- [ ] Data visualization displays
- [ ] Background tasks processing
- [ ] Error handling working
- [ ] Logging functional

## 🚨 Contingency Plans

### If Frontend Still Won't Start
1. **Alternative 1**: Use Create React App with minimal dependencies
2. **Alternative 2**: Build static frontend with Vite
3. **Alternative 3**: Focus on backend API testing first

### If Database Issues Persist
1. **Alternative 1**: Use SQLite for development
2. **Alternative 2**: Mock database responses
3. **Alternative 3**: Focus on API structure without persistence

### If Dependencies Continue to Fail
1. **Alternative 1**: Use Docker for consistent environment
2. **Alternative 2**: Create minimal requirements.txt
3. **Alternative 3**: Focus on core functionality only

## 📊 Progress Tracking

### Phase 1 Progress
- [ ] Frontend clean install completed
- [ ] ajv dependency resolved
- [ ] Package conflicts resolved
- [ ] Frontend starts successfully

### Phase 2 Progress
- [ ] Database connection verified
- [ ] Redis server running
- [ ] Celery worker configured
- [ ] Background tasks working

### Phase 3 Progress
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Integration testing completed
- [ ] Full stack communication verified

### Phase 4 Progress
- [ ] Advanced dependencies enabled
- [ ] Services tested
- [ ] Database operations working
- [ ] All features functional

### Phase 5 Progress
- [ ] Browser testing completed
- [ ] API testing completed
- [ ] Error handling verified
- [ ] User experience validated

## 🎯 Expected Outcomes

By the end of tomorrow, we should have:
1. **Fully functional platform** running in browser
2. **Complete frontend-backend integration**
3. **Working investigation workflow**
4. **Functional social media scraping**
5. **Professional user interface**
6. **Comprehensive error handling**
7. **Production-ready foundation**

## 📝 Notes for Tomorrow

- Start with Phase 1 (Frontend) as it's the blocking issue
- Use `--legacy-peer-deps` flag for npm installs
- Test each component individually before integration
- Keep detailed logs of any errors encountered
- Have contingency plans ready for each phase
- Focus on getting a working MVP first, then add advanced features

## 🔍 Debugging Commands

### Frontend Debugging
```bash
# Check npm version
npm --version

# Check Node.js version
node --version

# Clear npm cache
npm cache clean --force

# Check for port conflicts
lsof -i :3000

# Start with verbose logging
npm start --verbose
```

### Backend Debugging
```bash
# Check Python version
python3 --version

# Check pip packages
pip list | grep -E "(fastapi|uvicorn|sqlalchemy)"

# Test imports
python3 -c "import app.main; print('Backend imports successfully')"

# Check database connection
python3 -c "from app.core.database import engine; print('Database connected')"

# Start with debug logging
uvicorn app.main:app --reload --log-level debug
```

### System Debugging
```bash
# Check running processes
ps aux | grep -E "(uvicorn|npm|node|redis|postgres)"

# Check port usage
lsof -i :8000
lsof -i :3000
lsof -i :6379
lsof -i :5432

# Check system resources
top -l 1 | head -20
```

This plan provides a comprehensive roadmap to get the platform fully functional by addressing all current issues systematically. 