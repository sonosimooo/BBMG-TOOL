--- install_requirements.bat
+++ install_requirements.bat
@@ -0,0 +1,31 @@
+@echo off
+echo ===================================
+echo BBMG TOOL INSTALLER
+echo ===================================
+
+:: Check if Python is installed
+python --version > nul 2>&1
+if %errorlevel% neq 0 (
+    echo Python not found! Please make sure Python is installed and added to PATH.
+    pause
+    exit /b 1
+)
+
+echo Python found. Proceeding with package installation...
+echo.
+
+:: Install packages from requirements.txt
+python -m pip install -r requirements.txt
+
+if %errorlevel% neq 0 (
+    echo.
+    echo An error occurred during package installation.
+    echo Please check the requirements.txt file and ensure all packages are valid.
+) else (
+    echo.
+    echo Installation completed successfully!
+)
+
+echo.
+echo Press any key to exit...
+pause > nul