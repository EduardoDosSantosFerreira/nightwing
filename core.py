import os
import winreg
import shutil
import subprocess
import re
from typing import List, Tuple


def get_installed_programs() -> List[Tuple[str, str, float]]:
    """Retorna lista de programas instalados ordenados por tamanho (decrescente)

    Returns: Lista de tuplas (nome, comando desinstalação, tamanho em MB)
    """
    program_list = []
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]

    for reg_hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for path in registry_paths:
            try:
                with winreg.OpenKey(reg_hive, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    if not name:
                                        continue

                                    uninstall_cmd = winreg.QueryValueEx(
                                        subkey, "UninstallString"
                                    )[0]
                                    size = 0.0
                                    try:
                                        size = winreg.QueryValueEx(
                                            subkey, "EstimatedSize"
                                        )[0]
                                        size = round(size / 1024, 2)
                                    except FileNotFoundError:
                                        pass

                                    program_list.append((name, uninstall_cmd, size))
                                except FileNotFoundError:
                                    continue
                        except Exception as e:
                            continue
            except Exception as e:
                continue

    return sorted(program_list, key=lambda x: (-x[2], x[0]))


def limpar_residuos(nome_programa: str) -> List[str]:
    """Procura por pastas residuais do programa

    Args:
        nome_programa (str): Nome do programa para procurar resíduos

    Returns:
        List[str]: Lista de caminhos de pastas residuais
    """
    paths = [
        os.getenv("PROGRAMFILES", ""),
        os.getenv("PROGRAMFILES(X86)", ""),
        os.getenv("APPDATA", ""),
        os.getenv("LOCALAPPDATA", ""),
        os.getenv("PROGRAMDATA", ""),
        os.path.join(os.getenv("SYSTEMDRIVE", "C:"), "\\"),
    ]

    encontrados = []
    pattern = re.compile(re.escape(nome_programa), re.IGNORECASE)

    for base in paths:
        if not base or not os.path.exists(base):
            continue
        try:
            for item in os.listdir(base):
                try:
                    full_path = os.path.join(base, item)
                    if pattern.search(item) and os.path.isdir(full_path):
                        encontrados.append(full_path)
                except (PermissionError, FileNotFoundError):
                    continue
        except (PermissionError, FileNotFoundError):
            continue

    return encontrados


def remover_pastas(pastas: List[str]) -> bool:
    """Remove pastas residuais

    Args:
        pastas (List[str]): Lista de caminhos para remover

    Returns:
        bool: True se todas as pastas foram removidas com sucesso
    """
    success = True
    for path in pastas:
        try:
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
        except Exception as e:
            success = False
            continue
    return success


def desinstalar_programa(cmd: str) -> bool:
    """Executa o comando de desinstalação

    Args:
        cmd (str): Comando de desinstalação

    Returns:
        bool: True se a desinstalação foi iniciada com sucesso
    """
    try:
        if "msiexec" in cmd.lower():
            if "/qn" not in cmd.lower():
                cmd += " /qn /norestart"

        subprocess.Popen(cmd, shell=True)
        return True
    except Exception as e:
        return False


def scan_large_files(min_size_mb: int = 100) -> List[Tuple[str, str, float]]:
    """Procura por arquivos grandes no sistema

    Args:
        min_size_mb (int): Tamanho mínimo em MB para considerar

    Returns:
        List[Tuple[str, str, float]]: Lista de (nome_arquivo, caminho, tamanho_mb)
    """
    search_dirs = [
        os.path.expanduser("~"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Desktop"),
        os.getenv("TEMP", "C:\\Windows\\Temp"),
        os.getenv("ProgramData", "C:\\ProgramData"),
    ]

    large_files = []
    min_bytes = min_size_mb * 1024 * 1024

    for folder in search_dirs:
        if not os.path.exists(folder):
            continue

        try:
            for root, _, files in os.walk(folder):
                for file in files:
                    try:
                        path = os.path.join(root, file)
                        size = os.path.getsize(path)
                        if size >= min_bytes:
                            size_mb = round(size / (1024 * 1024), 2)
                            large_files.append((file, path, size_mb))
                    except (PermissionError, FileNotFoundError, OSError):
                        continue
        except (PermissionError, FileNotFoundError, OSError):
            continue

    return sorted(large_files, key=lambda x: (-x[2], x[0]))


def get_system_drives() -> List[str]:
    """Retorna lista de drives disponíveis no sistema"""
    drives = []
    for drive in range(ord("A"), ord("Z") + 1):
        drive = f"{chr(drive)}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives


if __name__ == "__main__":
    print("Programas instalados:")
    for i, (name, cmd, size) in enumerate(get_installed_programs()[:10]):
        print(f"{i+1}. {name} ({size} MB)")

    print("\nArquivos grandes:")
    for i, (name, path, size) in enumerate(scan_large_files()[:5]):
        print(f"{i+1}. {name} ({size} MB) - {path}")
