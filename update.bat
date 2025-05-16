@echo off
setlocal enabledelayedexpansion

echo ===================================
echo BBMG-TOOL Updater
echo ===================================
echo.

:: Verifica se Python è installato
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python non trovato! Assicurati che Python sia installato e aggiunto al PATH.
    pause
    exit /b 1
)

:: Verifica se git è installato
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git non trovato! Installazione in corso...
    
    :: Scarica Git for Windows
    echo Scaricamento di Git for Windows...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.41.0.windows.1/Git-2.41.0-64-bit.exe' -OutFile '%TEMP%\git-installer.exe'}"
    
    :: Installa Git silenziosamente
    echo Installazione di Git...
    start /wait "" "%TEMP%\git-installer.exe" /VERYSILENT /NORESTART
    
    :: Pulisci
    del "%TEMP%\git-installer.exe"
    
    :: Verifica nuovamente
    git --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Impossibile installare Git. Per favore installalo manualmente.
        pause
        exit /b 1
    )
    
    echo Git installato con successo!
)

:: Crea uno script Python temporaneo per controllare gli aggiornamenti
echo import os, sys, json, requests, re, shutil, tempfile, zipfile > "%TEMP%\check_update.py"
echo from datetime import datetime >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo def get_current_time(): >> "%TEMP%\check_update.py"
echo     return datetime.now().strftime("%%Y-%%m-%%d %%H:%%M:%%S") >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo # Versione corrente >> "%TEMP%\check_update.py"
echo current_version = '1.0.0' >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo # Repository GitHub >> "%TEMP%\check_update.py"
echo repo_owner = "sonosimooo" >> "%TEMP%\check_update.py"
echo repo_name = "BBMG-TOOL" >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo # URL per l'API GitHub >> "%TEMP%\check_update.py"
echo api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest" >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo try: >> "%TEMP%\check_update.py"
echo     print(f"[{get_current_time()}] [*] Controllo aggiornamenti...") >> "%TEMP%\check_update.py"
echo     response = requests.get(api_url, timeout=10) >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo     if response.status_code == 200: >> "%TEMP%\check_update.py"
echo         release_info = json.loads(response.text) >> "%TEMP%\check_update.py"
echo         latest_version = release_info.get('tag_name', '').replace('v', '') >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo         # Assicurati che la versione sia nel formato corretto >> "%TEMP%\check_update.py"
echo         if not re.match(r'^(\d+\.)*\d+$', latest_version): >> "%TEMP%\check_update.py"
echo             numeric_parts = re.findall(r'\d+', latest_version) >> "%TEMP%\check_update.py"
echo             if numeric_parts: >> "%TEMP%\check_update.py"
echo                 latest_version = '.'.join(numeric_parts) >> "%TEMP%\check_update.py"
echo             else: >> "%TEMP%\check_update.py"
echo                 print(f"[{get_current_time()}] [!] Formato versione non valido") >> "%TEMP%\check_update.py"
echo                 sys.exit(1) >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo         if latest_version and latest_version != current_version: >> "%TEMP%\check_update.py"
echo             try: >> "%TEMP%\check_update.py"
echo                 current_version_parts = [int(x) for x in current_version.split('.')] >> "%TEMP%\check_update.py"
echo                 latest_version_parts = [int(x) for x in latest_version.split('.')] >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                 if latest_version_parts > current_version_parts: >> "%TEMP%\check_update.py"
echo                     print(f"[{get_current_time()}] [+] Nuova versione disponibile: {latest_version}") >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                     # Ottieni l'URL di download >> "%TEMP%\check_update.py"
echo                     download_url = None >> "%TEMP%\check_update.py"
echo                     for asset in release_info.get('assets', []): >> "%TEMP%\check_update.py"
echo                         if asset.get('name', '').endswith('.zip'): >> "%TEMP%\check_update.py"
echo                             download_url = asset.get('browser_download_url') >> "%TEMP%\check_update.py"
echo                             break >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                     if not download_url: >> "%TEMP%\check_update.py"
echo                         download_url = release_info.get('zipball_url') >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                     if download_url: >> "%TEMP%\check_update.py"
echo                         print(f"[{get_current_time()}] [*] Scaricamento in corso...") >> "%TEMP%\check_update.py"
echo                         # Crea una directory temporanea >> "%TEMP%\check_update.py"
echo                         temp_dir = tempfile.mkdtemp() >> "%TEMP%\check_update.py"
echo                         zip_path = os.path.join(temp_dir, "update.zip") >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                         # Scarica il file zip >> "%TEMP%\check_update.py"
echo                         with requests.get(download_url, stream=True) as r: >> "%TEMP%\check_update.py"
echo                             r.raise_for_status() >> "%TEMP%\check_update.py"
echo                             with open(zip_path, 'wb') as f: >> "%TEMP%\check_update.py"
echo                                 for chunk in r.iter_content(chunk_size=8192): >> "%TEMP%\check_update.py"
echo                                     f.write(chunk) >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                         print(f"[{get_current_time()}] [*] Estrazione in corso...") >> "%TEMP%\check_update.py"
echo                         # Estrai il file zip >> "%TEMP%\check_update.py"
echo                         extract_dir = os.path.join(temp_dir, "extracted") >> "%TEMP%\check_update.py"
echo                         with zipfile.ZipFile(zip_path, 'r') as zip_ref: >> "%TEMP%\check_update.py"
echo                             zip_ref.extractall(extract_dir) >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                         # Trova la directory principale nell'archivio >> "%TEMP%\check_update.py"
echo                         extracted_dirs = [d for d in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, d))] >> "%TEMP%\check_update.py"
echo                         if extracted_dirs: >> "%TEMP%\check_update.py"
echo                             source_dir = os.path.join(extract_dir, extracted_dirs[0]) >> "%TEMP%\check_update.py"
echo                         else: >> "%TEMP%\check_update.py"
echo                             source_dir = extract_dir >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                         # Ottieni la directory corrente del programma >> "%TEMP%\check_update.py"
echo                         current_dir = os.path.dirname(os.path.abspath(__file__)) >> "%TEMP%\check_update.py"
echo                         target_dir = os.path.abspath(os.path.join(current_dir, "..")) >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                         print(f"[{get_current_time()}] [*] Installazione in corso...") >> "%TEMP%\check_update.py"
echo                         # Copia i file nella directory corrente >> "%TEMP%\check_update.py"
echo                         for item in os.listdir(source_dir): >> "%TEMP%\check_update.py"
echo                             s = os.path.join(source_dir, item) >> "%TEMP%\check_update.py"
echo                             d = os.path.join(target_dir, item) >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                             if os.path.isdir(s): >> "%TEMP%\check_update.py"
echo                                 if os.path.exists(d): >> "%TEMP%\check_update.py"
echo                                     shutil.rmtree(d) >> "%TEMP%\check_update.py"
echo                                 shutil.copytree(s, d) >> "%TEMP%\check_update.py"
echo                             else: >> "%TEMP%\check_update.py"
echo                                 if os.path.exists(d): >> "%TEMP%\check_update.py"
echo                                     os.remove(d) >> "%TEMP%\check_update.py"
echo                                 shutil.copy2(s, d) >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                         # Pulisci i file temporanei >> "%TEMP%\check_update.py"
echo                         shutil.rmtree(temp_dir) >> "%TEMP%\check_update.py"
echo. >> "%TEMP%\check_update.py"
echo                         print(f"[{get_current_time()}] [+] Aggiornamento completato alla versione {latest_version}!") >> "%TEMP%\check_update.py"
echo                         print(f"[{get_current_time()}] [*] Riavvia l'applicazione per applicare gli aggiornamenti.") >> "%TEMP%\check_update.py"
echo                     else: >> "%TEMP%\check_update.py"
echo                         print(f"[{get_current_time()}] [!] URL di download non trovato") >> "%TEMP%\check_update.py"
echo                 else: >> "%TEMP%\check_update.py"
echo                     print(f"[{get_current_time()}] [*] Nessun aggiornamento disponibile") >> "%TEMP%\check_update.py"
echo             except ValueError as e: >> "%TEMP%\check_update.py"
echo                 print(f"[{get_current_time()}] [!] Errore nel confronto delle versioni: {str(e)}") >> "%TEMP%\check_update.py"
echo         else: >> "%TEMP%\check_update.py"
echo             print(f"[{get_current_time()}] [*] Nessun aggiornamento disponibile") >> "%TEMP%\check_update.py"
echo     else: >> "%TEMP%\check_update.py"
echo         print(f"[{get_current_time()}] [!] Errore nella richiesta API: {response.status_code}") >> "%TEMP%\check_update.py"
echo except Exception as e: >> "%TEMP%\check_update.py"
echo     print(f"[{get_current_time()}] [!] Errore nel controllo degli aggiornamenti: {str(e)}") >> "%TEMP%\check_update.py"

:: Esegui lo script Python
echo.
echo Controllo aggiornamenti in corso...
python "%TEMP%\check_update.py"

:: Pulisci
del "%TEMP%\check_update.py"

echo.
echo Premi un tasto per uscire...
pause >nul
endlocal