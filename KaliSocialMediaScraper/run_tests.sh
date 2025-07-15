#!/bin/bash

# Comprehensive Test Runner Script
# Target: 85-90% coverage with industry-standard testing

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install test dependencies
install_dependencies() {
    print_status "Installing test dependencies..."
    
    if [ -f "requirements-test.txt" ]; then
        pip install -r requirements-test.txt
        print_success "Test dependencies installed successfully"
    else
        print_warning "requirements-test.txt not found, installing basic dependencies"
        pip install pytest pytest-asyncio pytest-cov httpx fastapi
    fi
}

# Function to run tests with coverage
run_tests_with_coverage() {
    local coverage_target=${1:-85}
    print_status "Running tests with ${coverage_target}% coverage target..."
    
    python tests/run_tests.py coverage $coverage_target
    
    if [ $? -eq 0 ]; then
        print_success "Tests passed with coverage target met!"
    else
        print_error "Tests failed or coverage target not met"
        exit 1
    fi
}

# Function to run specific test categories
run_test_category() {
    local category=$1
    print_status "Running $category tests..."
    
    case $category in
        "unit")
            python -m pytest tests/unit/ -v -m unit
            ;;
        "integration")
            python -m pytest tests/integration/ -v -m integration
            ;;
        "e2e")
            python -m pytest tests/e2e/ -v -m e2e
            ;;
        "frontend")
            if [ -d "frontend" ]; then
                cd frontend && npm test && cd ..
            else
                print_warning "Frontend directory not found, skipping frontend tests"
            fi
            ;;
        "performance")
            python -m pytest tests/e2e/ -v -m performance
            ;;
        "security")
            python -m pytest tests/e2e/ -v -m security
            ;;
        *)
            print_error "Unknown test category: $category"
            print_status "Available categories: unit, integration, e2e, frontend, performance, security"
            exit 1
            ;;
    esac
}

# Function to run all tests
run_all_tests() {
    print_status "Running comprehensive test suite..."
    python tests/run_tests.py
}

# Function to show coverage report
show_coverage() {
    if [ -f "test_results/coverage/index.html" ]; then
        print_status "Opening coverage report..."
        if command_exists "open"; then
            open test_results/coverage/index.html
        elif command_exists "xdg-open"; then
            xdg-open test_results/coverage/index.html
        else
            print_status "Coverage report available at: test_results/coverage/index.html"
        fi
    else
        print_warning "Coverage report not found. Run tests first."
    fi
}

# Function to clean test artifacts
clean_tests() {
    print_status "Cleaning test artifacts..."
    rm -rf test_results/
    rm -rf .pytest_cache/
    rm -rf .coverage
    rm -rf htmlcov/
    print_success "Test artifacts cleaned"
}

# Function to show help
show_help() {
    echo "Comprehensive Test Runner"
    echo "========================"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  all                    Run all tests with comprehensive coverage"
    echo "  unit                   Run unit tests only"
    echo "  integration            Run integration tests only"
    echo "  e2e                    Run end-to-end tests only"
    echo "  frontend               Run frontend tests only"
    echo "  performance            Run performance tests only"
    echo "  security               Run security tests only"
    echo "  coverage [target]      Run tests with specific coverage target (default: 85)"
    echo "  install                Install test dependencies"
    echo "  clean                  Clean test artifacts"
    echo "  report                 Show coverage report"
    echo "  help                   Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 all                 # Run all tests"
    echo "  $0 unit                # Run unit tests only"
    echo "  $0 coverage 90         # Run tests with 90% coverage target"
    echo "  $0 install             # Install dependencies"
    echo ""
}

# Main script logic
case "${1:-help}" in
    "all")
        install_dependencies
        run_all_tests
        ;;
    "unit"|"integration"|"e2e"|"frontend"|"performance"|"security")
        install_dependencies
        run_test_category $1
        ;;
    "coverage")
        install_dependencies
        run_tests_with_coverage $2
        ;;
    "install")
        install_dependencies
        ;;
    "clean")
        clean_tests
        ;;
    "report")
        show_coverage
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        print_error "Unknown option: $1"
        show_help
        exit 1
        ;;
esac

print_success "Test execution completed!" 