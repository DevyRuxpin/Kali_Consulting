"""
Comprehensive Test Runner with Coverage Reporting
Target: 85-90% coverage across all modules
"""

import subprocess
import sys
import os
import time
from pathlib import Path
from typing import List, Dict, Any

class TestRunner:
    """Comprehensive test runner with coverage reporting"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_dir = self.project_root / "tests"
        self.coverage_dir = self.project_root / "test_results"
        self.coverage_dir.mkdir(exist_ok=True)
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests with comprehensive coverage"""
        print("🚀 Starting comprehensive test suite...")
        print("Target: 85-90% coverage across all modules")
        print("=" * 60)
        
        results = {
            "unit_tests": self._run_unit_tests(),
            "integration_tests": self._run_integration_tests(),
            "e2e_tests": self._run_e2e_tests(),
            "frontend_tests": self._run_frontend_tests(),
            "performance_tests": self._run_performance_tests(),
            "security_tests": self._run_security_tests(),
            "coverage_report": self._generate_coverage_report()
        }
        
        self._print_summary(results)
        return results
    
    def _run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests"""
        print("📋 Running Unit Tests...")
        start_time = time.time()
        
        cmd = [
            "python", "-m", "pytest",
            "tests/unit/",
            "-v",
            "--tb=short",
            "--cov=app",
            "--cov-report=term-missing",
            "--cov-report=html:test_results/unit_coverage",
            "--cov-report=xml:test_results/unit_coverage.xml",
            "-m", "unit"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        duration = time.time() - start_time
        
        return {
            "success": result.returncode == 0,
            "duration": duration,
            "output": result.stdout,
            "errors": result.stderr,
            "return_code": result.returncode
        }
    
    def _run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests"""
        print("🔗 Running Integration Tests...")
        start_time = time.time()
        
        cmd = [
            "python", "-m", "pytest",
            "tests/integration/",
            "-v",
            "--tb=short",
            "--cov=app",
            "--cov-report=term-missing",
            "--cov-report=html:test_results/integration_coverage",
            "--cov-report=xml:test_results/integration_coverage.xml",
            "-m", "integration"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        duration = time.time() - start_time
        
        return {
            "success": result.returncode == 0,
            "duration": duration,
            "output": result.stdout,
            "errors": result.stderr,
            "return_code": result.returncode
        }
    
    def _run_e2e_tests(self) -> Dict[str, Any]:
        """Run end-to-end tests"""
        print("🌐 Running End-to-End Tests...")
        start_time = time.time()
        
        cmd = [
            "python", "-m", "pytest",
            "tests/e2e/",
            "-v",
            "--tb=short",
            "--cov=app",
            "--cov-report=term-missing",
            "--cov-report=html:test_results/e2e_coverage",
            "--cov-report=xml:test_results/e2e_coverage.xml",
            "-m", "e2e"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        duration = time.time() - start_time
        
        return {
            "success": result.returncode == 0,
            "duration": duration,
            "output": result.stdout,
            "errors": result.stderr,
            "return_code": result.returncode
        }
    
    def _run_frontend_tests(self) -> Dict[str, Any]:
        """Run frontend tests"""
        print("🎨 Running Frontend Tests...")
        start_time = time.time()
        
        # Check if frontend directory exists
        frontend_dir = self.project_root / "frontend"
        if not frontend_dir.exists():
            return {
                "success": False,
                "duration": 0,
                "output": "Frontend directory not found",
                "errors": "Frontend tests skipped - no frontend directory",
                "return_code": 1
            }
        
        # Run frontend tests (if using Jest or similar)
        cmd = [
            "npm", "test",
            "--",
            "--coverage",
            "--coverageDirectory=../test_results/frontend_coverage",
            "--passWithNoTests"
        ]
        
        # Change to frontend directory
        original_cwd = os.getcwd()
        os.chdir(frontend_dir)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
        finally:
            os.chdir(original_cwd)
        
        duration = time.time() - start_time
        
        return {
            "success": result.returncode == 0,
            "duration": duration,
            "output": result.stdout,
            "errors": result.stderr,
            "return_code": result.returncode
        }
    
    def _run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests"""
        print("⚡ Running Performance Tests...")
        start_time = time.time()
        
        cmd = [
            "python", "-m", "pytest",
            "tests/e2e/",
            "-v",
            "--tb=short",
            "-m", "performance"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        duration = time.time() - start_time
        
        return {
            "success": result.returncode == 0,
            "duration": duration,
            "output": result.stdout,
            "errors": result.stderr,
            "return_code": result.returncode
        }
    
    def _run_security_tests(self) -> Dict[str, Any]:
        """Run security tests"""
        print("🔒 Running Security Tests...")
        start_time = time.time()
        
        cmd = [
            "python", "-m", "pytest",
            "tests/e2e/",
            "-v",
            "--tb=short",
            "-m", "security"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        duration = time.time() - start_time
        
        return {
            "success": result.returncode == 0,
            "duration": duration,
            "output": result.stdout,
            "errors": result.stderr,
            "return_code": result.returncode
        }
    
    def _generate_coverage_report(self) -> Dict[str, Any]:
        """Generate comprehensive coverage report"""
        print("📊 Generating Coverage Report...")
        
        cmd = [
            "python", "-m", "coverage",
            "combine",
            "test_results/*.coverage"
        ]
        
        subprocess.run(cmd, capture_output=True)
        
        # Generate HTML report
        cmd = [
            "python", "-m", "coverage",
            "html",
            "--directory=test_results/combined_coverage"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Generate XML report
        cmd = [
            "python", "-m", "coverage",
            "xml",
            "-o", "test_results/combined_coverage.xml"
        ]
        
        subprocess.run(cmd, capture_output=True)
        
        return {
            "success": result.returncode == 0,
            "html_report": "test_results/combined_coverage/index.html",
            "xml_report": "test_results/combined_coverage.xml"
        }
    
    def _print_summary(self, results: Dict[str, Any]):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = 0
        passed_tests = 0
        total_duration = 0
        
        for test_type, result in results.items():
            if test_type == "coverage_report":
                continue
                
            status = "✅ PASSED" if result["success"] else "❌ FAILED"
            duration = f"{result['duration']:.2f}s"
            
            print(f"{test_type.replace('_', ' ').title():<20} {status:<10} {duration}")
            
            if result["success"]:
                passed_tests += 1
            total_tests += 1
            total_duration += result["duration"]
        
        print("-" * 60)
        print(f"Overall Result: {'✅ ALL TESTS PASSED' if passed_tests == total_tests else '❌ SOME TESTS FAILED'}")
        print(f"Pass Rate: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"Total Duration: {total_duration:.2f}s")
        
        if "coverage_report" in results:
            print(f"Coverage Report: {results['coverage_report']['html_report']}")
        
        print("=" * 60)
    
    def run_specific_tests(self, test_paths: List[str]) -> Dict[str, Any]:
        """Run specific test files or directories"""
        print(f"🎯 Running specific tests: {', '.join(test_paths)}")
        
        cmd = [
            "python", "-m", "pytest",
            *test_paths,
            "-v",
            "--tb=short",
            "--cov=app",
            "--cov-report=term-missing"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr,
            "return_code": result.returncode
        }
    
    def run_tests_with_coverage(self, coverage_target: float = 85.0) -> Dict[str, Any]:
        """Run tests with specific coverage target"""
        print(f"🎯 Running tests with {coverage_target}% coverage target...")
        
        cmd = [
            "python", "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "--cov=app",
            f"--cov-fail-under={coverage_target}",
            "--cov-report=term-missing",
            "--cov-report=html:test_results/coverage",
            "--cov-report=xml:test_results/coverage.xml"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "coverage_target": coverage_target,
            "output": result.stdout,
            "errors": result.stderr,
            "return_code": result.returncode
        }

def main():
    """Main test runner entry point"""
    runner = TestRunner()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "specific":
            # Run specific tests
            test_paths = sys.argv[2:]
            results = runner.run_specific_tests(test_paths)
        elif sys.argv[1] == "coverage":
            # Run with coverage target
            coverage_target = float(sys.argv[2]) if len(sys.argv) > 2 else 85.0
            results = runner.run_tests_with_coverage(coverage_target)
        else:
            print("Usage:")
            print("  python run_tests.py                    # Run all tests")
            print("  python run_tests.py specific <paths>   # Run specific tests")
            print("  python run_tests.py coverage <target>  # Run with coverage target")
            return
    else:
        # Run all tests
        results = runner.run_all_tests()
    
    # Exit with appropriate code
    if isinstance(results, dict) and results.get("success", True):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 