import os
import sys
import time
import signal
import subprocess
from pathlib import Path


def build_command(module: str, args: list[str]) -> list[str]:
    """Return a command that runs a module (prefers `uvicorn` if on PATH)."""
    # Prefer `python -m <module>` to avoid PATH issues on Windows
    return [sys.executable, "-m", module, *args]


def start_process(cmd: list[str], cwd: Path) -> subprocess.Popen:
    return subprocess.Popen(cmd, cwd=str(cwd))


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    service1_dir = repo_root / "service1_status"
    service2_dir = repo_root / "service2_telemetry"
    frontend_dir = repo_root / "frontend"

    processes: list[subprocess.Popen] = []

    try:
        # Serviço de Status (8001)
        svc1_cmd = build_command(
            "uvicorn",
            ["main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"],
        )
        processes.append(start_process(svc1_cmd, service1_dir))

        # Serviço de Telemetria (8002)
        svc2_cmd = build_command(
            "uvicorn",
            ["main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"],
        )
        processes.append(start_process(svc2_cmd, service2_dir))

        # Frontend (8080)
        fe_cmd = [sys.executable, "-m", "http.server", "8080"]
        processes.append(start_process(fe_cmd, frontend_dir))

        print("\nServiços iniciados:\n"
              " - Status:     http://localhost:8001/health\n"
              " - Telemetria: http://localhost:8002/health\n"
              " - Frontend:   http://localhost:8080\n")
        print("Pressione Ctrl+C para encerrar todos.")

        # Mantém o processo principal vivo
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nEncerrando processos...")
    finally:
        for p in processes:
            try:
                if p.poll() is None:
                    # Tenta encerrar graciosamente
                    p.terminate()
            except Exception:
                pass

        # Aguarda encerramento e força se necessário
        deadline = time.time() + 5
        for p in processes:
            try:
                while p.poll() is None and time.time() < deadline:
                    time.sleep(0.1)
                if p.poll() is None:
                    p.kill()
            except Exception:
                pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


