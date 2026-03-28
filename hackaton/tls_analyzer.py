#!/usr/bin/env python3
import argparse
import socket
import ssl
import json
import re
from datetime import datetime

TLS_VERSION_MAP = {
    "TLSv1": ssl.TLSVersion.TLSv1,
    "TLSv1.1": ssl.TLSVersion.TLSv1_1,
    "TLSv1.2": ssl.TLSVersion.TLSv1_2,
    "TLSv1.3": ssl.TLSVersion.TLSv1_3,
}

OBSOLETE = {"TLSv1", "TLSv1.1"}
MODERN = {"TLSv1.2", "TLSv1.3"}

def is_valid_ip(value: str) -> bool:
    try:
        socket.inet_aton(value)
        return True
    except OSError:
        return False

def is_valid_domain(value: str) -> bool:
    pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
    return re.match(pattern, value) is not None

def normalize_target(target: str):
    if ":" in target and target.count(":") == 1:
        host, port = target.split(":")
        return host.strip(), int(port)
    return target.strip(), 443

def validate_target(target: str):
    host, port = normalize_target(target)
    if not (is_valid_ip(host) or is_valid_domain(host)):
        raise ValueError(f"Objetivo inválido: {target}")
    if not (1 <= port <= 65535):
        raise ValueError(f"Puerto inválido en: {target}")
    return host, port

def test_tls_version(host: str, port: int, version_name: str, timeout: int = 4):
    version = TLS_VERSION_MAP[version_name]
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.minimum_version = version
    context.maximum_version = version

    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                negotiated = ssock.version()
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                return {
                    "supported": True,
                    "negotiated": negotiated,
                    "cipher": cipher[0] if cipher else None,
                    "cert_present": cert is not None
                }
    except Exception as e:
        return {
            "supported": False,
            "error": str(e)
        }

def analyze_target(target: str):
    host, port = validate_target(target)

    results = {
        "target": target,
        "host": host,
        "port": port,
        "scan_time": datetime.utcnow().isoformat() + "Z",
        "tls_versions": {},
        "findings": [],
        "risk_level": "LOW",
        "score": 0,
        "recommendations": []
    }

    supported_versions = []

    for version_name in TLS_VERSION_MAP.keys():
        res = test_tls_version(host, port, version_name)
        results["tls_versions"][version_name] = res
        if res["supported"]:
            supported_versions.append(version_name)

    # Hallazgos
    if not supported_versions:
        results["findings"].append("No fue posible negociar ninguna versión TLS")
        results["score"] += 60

    for version in supported_versions:
        if version in OBSOLETE:
            results["findings"].append(f"Protocolo obsoleto habilitado: {version}")
            results["score"] += 40

    if "TLSv1.3" not in supported_versions and "TLSv1.2" in supported_versions:
        results["findings"].append("TLS 1.3 no habilitado")
        results["score"] += 10

    if "TLSv1.2" not in supported_versions and "TLSv1.3" not in supported_versions:
        results["findings"].append("No hay protocolos modernos habilitados (TLS 1.2/1.3)")
        results["score"] += 50

    # Recomendaciones
    if any(v in supported_versions for v in OBSOLETE):
        results["recommendations"].append("Deshabilitar TLS 1.0 y TLS 1.1")
        results["recommendations"].append("Restringir el servicio a TLS 1.2 y TLS 1.3")

    if "TLSv1.3" not in supported_versions and "TLSv1.2" in supported_versions:
        results["recommendations"].append("Evaluar habilitación de TLS 1.3 para mejorar postura criptográfica")

    if "TLSv1.2" not in supported_versions and "TLSv1.3" not in supported_versions:
        results["recommendations"].append("Reconfigurar urgentemente el servicio para soportar versiones modernas")

    if not results["recommendations"]:
        results["recommendations"].append("Mantener monitoreo periódico y validar consistencia entre ambientes")

    # Severidad
    score = results["score"]
    if score >= 70:
        results["risk_level"] = "CRITICAL"
    elif score >= 40:
        results["risk_level"] = "HIGH"
    elif score >= 15:
        results["risk_level"] = "MEDIUM"
    else:
        results["risk_level"] = "LOW"

    return results

def print_report(result):
    print("=" * 70)
    print(f"Servidor: {result['target']}")
    print(f"Host: {result['host']}:{result['port']}")
    print(f"Fecha: {result['scan_time']}")
    print("-" * 70)

    for version, data in result["tls_versions"].items():
        status = "ENABLED" if data["supported"] else "DISABLED"
        print(f"{version}: {status}")
        if data["supported"]:
            print(f"  Cipher: {data.get('cipher')}")
        else:
            if "error" in data:
                print(f"  Error: {data['error']}")

    print("-" * 70)
    print(f"Nivel de riesgo: {result['risk_level']}")
    print("Hallazgos:")
    if result["findings"]:
        for f in result["findings"]:
            print(f"  - {f}")
    else:
        print("  - Sin hallazgos inseguros relevantes")

    print("Recomendaciones:")
    for r in result["recommendations"]:
        print(f"  - {r}")
    print("=" * 70)

def save_json(results, filename="report.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def save_html(results, filename="report.html"):
    rows = []
    for result in results:
        findings = "<br>".join(result["findings"]) if result["findings"] else "Sin hallazgos"
        recs = "<br>".join(result["recommendations"])
        versions = []
        for version, data in result["tls_versions"].items():
            status = "ENABLED" if data["supported"] else "DISABLED"
            versions.append(f"{version}: {status}")
        versions_html = "<br>".join(versions)

        rows.append(f"""
        <tr>
            <td>{result['target']}</td>
            <td>{versions_html}</td>
            <td>{findings}</td>
            <td>{result['risk_level']}</td>
            <td>{recs}</td>
        </tr>
        """)

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Reporte TLS</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ccc; padding: 10px; vertical-align: top; }}
            th {{ background: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Reporte de análisis TLS</h1>
        <table>
            <tr>
                <th>Servidor</th>
                <th>Versiones TLS</th>
                <th>Hallazgos</th>
                <th>Riesgo</th>
                <th>Recomendaciones</th>
            </tr>
            {''.join(rows)}
        </table>
    </body>
    </html>
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser(description="Analizador TLS para hackathon")
    parser.add_argument("targets", nargs="+", help="Dominios o IPs. Ej: google.com api.github.com:443")
    parser.add_argument("--json", dest="json_out", default="report.json", help="Archivo JSON de salida")
    parser.add_argument("--html", dest="html_out", default="report.html", help="Archivo HTML de salida")
    args = parser.parse_args()

    all_results = []

    for target in args.targets:
        try:
            result = analyze_target(target)
            print_report(result)
            all_results.append(result)
        except Exception as e:
            error_result = {
                "target": target,
                "error": str(e),
                "risk_level": "UNKNOWN"
            }
            print(f"[ERROR] {target}: {e}")
            all_results.append(error_result)

    save_json(all_results, args.json_out)

    valid_results = [r for r in all_results if "tls_versions" in r]
    if valid_results:
        save_html(valid_results, args.html_out)

    print(f"\nJSON generado: {args.json_out}")
    if valid_results:
        print(f"HTML generado: {args.html_out}")

if __name__ == "__main__":
    main()