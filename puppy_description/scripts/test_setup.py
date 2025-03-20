#!/usr/bin/env python3

import subprocess
import time
import sys
import signal
import os
import logging
import psutil
from datetime import datetime

class TestSetup:
    def __init__(self):
        self.container_name = f"puppy_ros_test_{os.getenv('USER', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.setup_successful = False
        self.processes = []
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = "/tmp/ros_logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"test_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def kill_process_tree(self, pid):
        """Kill a process and all its children"""
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                child.terminate()
            parent.terminate()
        except psutil.NoSuchProcess:
            pass
            
    def cleanup_processes(self):
        """Clean up all spawned processes"""
        for process in self.processes:
            try:
                self.kill_process_tree(process.pid)
            except Exception as e:
                self.logger.error(f"Error killing process {process.pid}: {e}")
                
    def run_command(self, command, timeout=30):
        """Run a command with timeout and return output"""
        self.logger.info(f"Running command: {command}")
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True
            )
            self.processes.append(process)
            stdout, stderr = process.communicate(timeout=timeout)
            if process.returncode != 0:
                self.logger.error(f"Command failed with return code {process.returncode}")
                self.logger.error(f"Stderr: {stderr}")
            return process.returncode, stdout, stderr
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out after {timeout} seconds")
            self.kill_process_tree(process.pid)
            return -1, "", "Command timed out"
            
    def cleanup(self):
        """Clean up any existing containers and processes"""
        self.cleanup_processes()
        if self.container_name:
            self.logger.info(f"Cleaning up container: {self.container_name}")
            self.run_command(f"docker stop {self.container_name}", timeout=5)
            self.run_command(f"docker rm {self.container_name}", timeout=5)
            
    def signal_handler(self, signum, frame):
        """Handle cleanup on exit signals"""
        self.logger.info("Received exit signal. Cleaning up...")
        self.cleanup()
        sys.exit(0)
        
    def test_simulation(self):
        """Test the simulation setup"""
        self.logger.info("Testing simulation setup...")
        
        # Start RViz with timeout
        self.logger.info("Starting RViz...")
        rviz_process = subprocess.Popen(
            f"docker exec {self.container_name} bash -c 'roslaunch puppy_description display.launch'",
            shell=True
        )
        self.processes.append(rviz_process)
        
        # Wait for RViz to start with timeout
        start_time = time.time()
        while time.time() - start_time < 10:  # 10 second timeout
            if rviz_process.poll() is not None:
                self.logger.error("RViz process terminated unexpectedly")
                return False
            time.sleep(0.5)
        
        # Test movement script with timeout
        self.logger.info("Testing movement script...")
        returncode, stdout, stderr = self.run_command(
            f"docker exec {self.container_name} bash -c 'python3 /ros_ws/src/puppy_description/scripts/movement_test.py'",
            timeout=10
        )
        
        # Cleanup RViz
        self.kill_process_tree(rviz_process.pid)
        
        return returncode == 0
        
    def test_setup(self):
        """Test the complete setup"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Step 1: Clean up any existing containers
            self.logger.info("Cleaning up existing containers...")
            self.run_command("docker-compose -f docker-compose.test.yml down", timeout=10)
            
            # Step 2: Start the container with custom name
            self.logger.info(f"Starting test container with name: {self.container_name}")
            returncode, stdout, stderr = self.run_command(
                f"CONTAINER_NAME={self.container_name} docker-compose -f docker-compose.test.yml up -d",
                timeout=10
            )
            if returncode != 0:
                self.logger.error("Failed to start container")
                return False
                
            # Step 3: Wait for container to be healthy with timeout
            self.logger.info("Waiting for container to be healthy...")
            start_time = time.time()
            while time.time() - start_time < 30:  # 30 second timeout
                returncode, stdout, stderr = self.run_command(
                    f"docker inspect --format='{{{{.State.Health.Status}}}}' {self.container_name}",
                    timeout=5
                )
                if returncode == 0 and stdout.strip() == "healthy":
                    self.logger.info("Container is healthy")
                    break
                self.logger.info(f"Waiting for container health... ({int(time.time() - start_time)}/30s)")
                time.sleep(1)
            else:
                self.logger.error("Container failed to become healthy")
                return False
                
            # Step 4: Test ROS setup
            self.logger.info("Testing ROS setup...")
            test_commands = [
                "source /opt/ros/noetic/setup.bash",
                "source /ros_ws/devel/setup.bash",
                "rosnode list"
            ]
            
            for cmd in test_commands:
                returncode, stdout, stderr = self.run_command(
                    f"docker exec {self.container_name} bash -c '{cmd}'",
                    timeout=5
                )
                if returncode != 0:
                    self.logger.error(f"Command failed: {cmd}")
                    return False
                    
            # Step 5: Test simulation and movement
            if not self.test_simulation():
                self.logger.error("Simulation test failed")
                return False
                
            self.logger.info("All tests passed successfully!")
            self.setup_successful = True
            return True
            
        except Exception as e:
            self.logger.error(f"Error during testing: {e}", exc_info=True)
            return False
        finally:
            if not self.setup_successful:
                self.cleanup()

if __name__ == '__main__':
    tester = TestSetup()
    success = tester.test_setup()
    if not success:
        print("Setup testing failed! Check logs in /tmp/ros_logs for details.")
        sys.exit(1) 