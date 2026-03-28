#!/usr/bin/env python3
import argparse
import csv
import html
import json
import re
import shutil
import socket
import ssl
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime, UTC
from typing import Dict, List, Optional, Tuple


TLS_VERSION_MAP = {
    "TLSv1": ssl.TLSVersion.TLSv1,
    "TLSv1.1": ssl.TLSVersion.TLSv1_1,
    "TLSv1.2": ssl.TLSVersion.TLSv1_2,
    "TLSv1.3": ssl.TLSVersion.TLSv1_3,
}

OBSOLETE_TLS = {"TLSv1", "TLSv1.1"}
MODERN_TLS = {"TLSv1.2", "TLSv1.3"}


@dataclass
class TLSProbeResult:
    supported: bool
    negotiated: Optional[str] = None
    cipher: Optional[str] = None
    cert_present: Optional[bool] = None
    status: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ScanResult:
    target: str
    host: str
    port: int
    scan_time: str
    tls_versions: Dict[str, dict]
    findings: List[str]
    risk_level: str
    score: int
    recommendations: List[str]
    summary: str
    nmap_summary: Optional[str] = None


def is_valid_ip(value: str) -> bool:
    try:
        socket.inet_aton(value)
        return True
    except OSError:
        return False


def is_valid_domain(value: str) -> bool:
    pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
    return re.match(pattern, value) is not None


def normalize_target(target: str) -> Tuple[str, int]:
    target = target.strip()
    if ":" in target and target.count(":") == 1:
        host, port_str = target.split(":")
        return host.strip(), int(port_str.strip())
    return target, 443


def validate_target(target: str) -> Tuple[str, int]:
    host, port = normalize_target(target)

    if not (is_valid_ip(host) or is_valid_domain(host)):
        raise ValueError(f"Objetivo inválido: {target}")

    if not (1 <= port <= 65535):
        raise ValueError(f"Puerto inválido: {port}")

    return host, port


def classify_ssl_error(exc: Exception) -> Tuple[str, str]:
    message = str(exc)

    if "NO_CIPHERS_AVAILABLE" in message:
        return "CLIENT_NOT_SUPPORTED", "El cliente local no dispone de cifrados para esta versión TLS."
    if "WRONG_VERSION_NUMBER" in message:
        return "WRONG_VERSION", "El servidor no aceptó esa versión TLS o el puerto no usa TLS."
    if "TLSV1_ALERT_PROTOCOL_VERSION" in message:
        return "SERVER_REJECTED", "El servidor rechazó explícitamente la versión TLS probada."
    if "CERTIFICATE_VERIFY_FAILED" in message:
        return "CERTIFICATE_ERROR", "Hubo un problema de validación de certificado."
    if "timed out" in message.lower():
        return "TIMEOUT", "El servidor tardó demasiado en responder."
    if "Name or service not known" in message or "nodename nor servname provided" in message:
        return "DNS_ERROR", "No fue posible resolver el dominio."

    return "CONNECTION_FAILED", message


def probe_tls_version(host: str, port: int, version_name: str, timeout: int = 4) -> TLSProbeResult:
    version = TLS_VERSION_MAP[version_name]

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        context.minimum_version = version
        context.maximum_version = version
    except ValueError as exc:
        status, message = classify_ssl_error(exc)
        return TLSProbeResult(False, status=status, error=message)

    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as tls_sock:
                cipher = tls_sock.cipher()
                cert = tls_sock.getpeercert()
                return TLSProbeResult(
                    supported=True,
                    negotiated=tls_sock.version(),
                    cipher=cipher[0] if cipher else None,
                    cert_present=cert is not None,
                    status="SUPPORTED"
                )
    except Exception as exc:
        status, message = classify_ssl_error(exc)
        return TLSProbeResult(False, status=status, error=message)


def run_nmap_tls_check(host: str, port: int) -> Optional[str]:
    if not shutil.which("nmap"):
        return None

    try:
        cmd = [
            "nmap",
            "--script", "ssl-enum-ciphers",
            "-p", str(port),
            host
        ]
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = completed.stdout + "\n" + completed.stderr
        output_lower = output.lower()

        detected = []
        if "tlsv1.0" in output_lower or "tlsv1.0:" in output_lower or "tlsv1:" in output_lower:
            detected.append("TLS 1.0")
        if "tlsv1.1" in output_lower:
            detected.append("TLS 1.1")
        if "tlsv1.2" in output_lower:
            detected.append("TLS 1.2")
        if "tlsv1.3" in output_lower:
            detected.append("TLS 1.3")

        if detected:
            return "nmap detectó: " + ", ".join(detected)
        return "nmap ejecutado sin versiones TLS claramente parseables."
    except Exception as exc:
        return f"nmap no pudo completarse: {exc}"


def risk_label(score: int) -> str:
    if score >= 70:
        return "CRITICAL"
    if score >= 40:
        return "HIGH"
    if score >= 15:
        return "MEDIUM"
    return "LOW"


def build_findings_and_recommendations(
    supported_versions: List[str],
    raw_results: Dict[str, TLSProbeResult]
) -> Tuple[List[str], List[str], int, str]:
    findings = []
    recommendations = []
    score = 0

    if not supported_versions:
        findings.append("No fue posible negociar ninguna versión TLS utilizable.")
        recommendations.append("Verificar si el puerto usa TLS, revisar conectividad y validar con herramientas externas.")
        score += 70

    obsolete_enabled = [v for v in supported_versions if v in OBSOLETE_TLS]
    if obsolete_enabled:
        findings.append(f"Protocolos obsoletos habilitados: {', '.join(obsolete_enabled)}.")
        recommendations.append("Deshabilitar TLS 1.0 y TLS 1.1.")
        recommendations.append("Restringir el servicio a TLS 1.2 y TLS 1.3.")
        score += 40

    if "TLSv1.2" not in supported_versions and "TLSv1.3" not in supported_versions:
        findings.append("No se detectaron versiones modernas de TLS (1.2 o 1.3).")
        recommendations.append("Reconfigurar urgentemente el servicio para soportar TLS moderno.")
        score += 50

    if "TLSv1.2" in supported_versions and "TLSv1.3" not in supported_versions:
        findings.append("TLS 1.3 no está habilitado.")
        recommendations.append("Evaluar habilitar TLS 1.3 para mejorar postura criptográfica.")
        score += 10

    legacy_client_limits = []
    for version_name in ("TLSv1", "TLSv1.1"):
        probe = raw_results.get(version_name)
        if probe and probe.status == "CLIENT_NOT_SUPPORTED":
            legacy_client_limits.append(version_name)

    if legacy_client_limits:
        findings.append(
            "La verificación de versiones heredadas depende del soporte criptográfico del cliente local: "
            + ", ".join(legacy_client_limits) + "."
        )
        recommendations.append("Validar TLS 1.0/1.1 adicionalmente con nmap, sslscan o testssl.sh.")
        score += 5

    if not findings:
        findings.append("Configuración segura: no se detectaron protocolos obsoletos ni exposición evidente.")
        recommendations.append("Mantener monitoreo periódico y validar consistencia entre ambientes.")

    summary = {
        "LOW": "Configuración TLS saludable.",
        "MEDIUM": "Configuración aceptable, con oportunidades de mejora.",
        "HIGH": "Existen debilidades importantes que deben corregirse.",
        "CRITICAL": "La exposición es alta y requiere remediación urgente."
    }[risk_label(score)]

    return findings, recommendations, score, summary


def analyze_target(target: str, use_nmap: bool = False) -> ScanResult:
    host, port = validate_target(target)

    raw_results: Dict[str, TLSProbeResult] = {}
    supported_versions: List[str] = []

    for version_name in TLS_VERSION_MAP:
        result = probe_tls_version(host, port, version_name)
        raw_results[version_name] = result
        if result.supported:
            supported_versions.append(version_name)

    findings, recommendations, score, summary = build_findings_and_recommendations(
        supported_versions,
        raw_results
    )

    nmap_summary = run_nmap_tls_check(host, port) if use_nmap else None

    return ScanResult(
        target=target,
        host=host,
        port=port,
        scan_time=datetime.now(UTC).isoformat(),
        tls_versions={k: asdict(v) for k, v in raw_results.items()},
        findings=findings,
        risk_level=risk_label(score),
        score=score,
        recommendations=recommendations,
        summary=summary,
        nmap_summary=nmap_summary
    )


def print_console_report(result: ScanResult) -> None:
    print("=" * 90)
    print(f"Servidor: {result.target}")
    print(f"Host: {result.host}:{result.port}")
    print(f"Fecha: {result.scan_time}")
    print("-" * 90)

    for version, data in result.tls_versions.items():
        status = "ENABLED" if data["supported"] else "DISABLED"
        print(f"{version}: {status}")
        if data["supported"]:
            print(f"  Negotiated: {data.get('negotiated')}")
            print(f"  Cipher: {data.get('cipher')}")
        else:
            print(f"  Status: {data.get('status')}")
            if data.get("error"):
                print(f"  Detail: {data.get('error')}")

    print("-" * 90)
    print(f"Riesgo: {result.risk_level} (score={result.score})")
    print(f"Resumen: {result.summary}")
    if result.nmap_summary:
        print(f"Validación nmap: {result.nmap_summary}")
    print("Hallazgos:")
    for finding in result.findings:
        print(f"  - {finding}")
    print("Recomendaciones:")
    for recommendation in result.recommendations:
        print(f"  - {recommendation}")
    print("=" * 90)


def summarize_results(results: List[ScanResult]) -> dict:
    summary = {"total": len(results), "LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for result in results:
        summary[result.risk_level] += 1
    return summary


def save_json(results: List[ScanResult], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump([asdict(r) for r in results], fh, indent=2, ensure_ascii=False)


def save_csv(results: List[ScanResult], filename: str) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            "target", "host", "port", "scan_time", "risk_level", "score",
            "summary", "findings", "recommendations", "nmap_summary"
        ])
        for result in results:
            writer.writerow([
                result.target,
                result.host,
                result.port,
                result.scan_time,
                result.risk_level,
                result.score,
                result.summary,
                " | ".join(result.findings),
                " | ".join(result.recommendations),
                result.nmap_summary or ""
            ])


def risk_css_class(risk: str) -> str:
    return {
        "LOW": "risk-low",
        "MEDIUM": "risk-medium",
        "HIGH": "risk-high",
        "CRITICAL": "risk-critical"
    }.get(risk, "")


def tls_version_badge(version: str, enabled: bool) -> str:
    version_clean = html.escape(version)
    if enabled and version in ("TLSv1.2", "TLSv1.3"):
        return f'<span class="badge badge-good">{version_clean}: ENABLED</span>'
    if enabled and version in ("TLSv1", "TLSv1.1"):
        return f'<span class="badge badge-bad">{version_clean}: ENABLED</span>'
    return f'<span class="badge badge-neutral">{version_clean}: DISABLED</span>'


def overall_status(summary: dict) -> Tuple[str, str]:
    if summary["CRITICAL"] > 0:
        return "Estado general: CRÍTICO", "overall-critical"
    if summary["HIGH"] > 0:
        return "Estado general: RIESGO ALTO", "overall-high"
    if summary["MEDIUM"] > 0:
        return "Estado general: MEJORABLE", "overall-medium"
    return "Estado general: SEGURO", "overall-safe"


def build_chart(summary: dict) -> str:
    total = max(summary["total"], 1)
    bars = []
    for label in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        value = summary[label]
        width = int((value / total) * 100)
        css = risk_css_class(label)
        bars.append(f"""
        <div class="chart-row">
            <div class="chart-label">{label}</div>
            <div class="chart-bar-wrap">
                <div class="chart-bar {css}" style="width:{max(width, 6 if value > 0 else 0)}%;">{value}</div>
            </div>
        </div>
        """)
    return "\n".join(bars)


def save_html(results: List[ScanResult], filename: str, dark_mode: bool = True) -> None:
    summary = summarize_results(results)
    overall_text, overall_class = overall_status(summary)

    rows = []
    for result in results:
        versions_html = "<br>".join(
            tls_version_badge(version, data["supported"])
            for version, data in result.tls_versions.items()
        )

        findings_html = "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in result.findings) + "</ul>"
        recommendations_html = "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in result.recommendations) + "</ul>"

        nmap_html = ""
        if result.nmap_summary:
            nmap_html = f"<div class='nmap-box'><strong>Validación nmap:</strong> {html.escape(result.nmap_summary)}</div>"

        rows.append(f"""
        <tr>
            <td>
                <strong>{html.escape(result.target)}</strong><br>
                <small>{html.escape(result.host)}:{result.port}</small><br>
                <small>{html.escape(result.scan_time)}</small>
            </td>
            <td>{versions_html}</td>
            <td>{findings_html}{nmap_html}</td>
            <td class="{risk_css_class(result.risk_level)}"><strong>{html.escape(result.risk_level)}</strong></td>
            <td>{html.escape(result.summary)}</td>
            <td>{recommendations_html}</td>
        </tr>
        """)

    if dark_mode:
        body_bg = "#0b1020"
        card_bg = "#121a2b"
        text_color = "#e8eefc"
        table_bg = "#111827"
        th_bg = "#1f2937"
        border_color = "#2b3548"
        muted = "#9fb0d1"
    else:
        body_bg = "#f7f9fc"
        card_bg = "#ffffff"
        text_color = "#222222"
        table_bg = "#ffffff"
        th_bg = "#e9eef5"
        border_color = "#dcdcdc"
        muted = "#555555"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Reporte de análisis TLS</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 24px;
                color: {text_color};
                background: {body_bg};
            }}
            h1, h2 {{
                margin-bottom: 10px;
            }}
            .intro, .card, .overall-banner {{
                background: {card_bg};
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 18px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.18);
            }}
            .summary-grid {{
                display: grid;
                grid-template-columns: repeat(5, minmax(120px, 1fr));
                gap: 12px;
                margin: 16px 0 24px 0;
            }}
            .card {{
                text-align: center;
            }}
            .value {{
                font-size: 1.8rem;
                font-weight: bold;
                margin-top: 6px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: {table_bg};
                box-shadow: 0 4px 16px rgba(0,0,0,0.18);
            }}
            th, td {{
                border: 1px solid {border_color};
                padding: 12px;
                vertical-align: top;
                text-align: left;
            }}
            th {{
                background: {th_bg};
            }}
            ul {{
                margin: 0;
                padding-left: 20px;
            }}
            .risk-low {{
                background: #1d4d2a55;
            }}
            .risk-medium {{
                background: #8a6d1f55;
            }}
            .risk-high {{
                background: #914f1b66;
            }}
            .risk-critical {{
                background: #7f1d1d88;
            }}
            .badge {{
                display: inline-block;
                padding: 6px 10px;
                border-radius: 999px;
                margin: 3px 4px 3px 0;
                font-size: 0.92rem;
                font-weight: bold;
            }}
            .badge-good {{
                background: #14532d;
                color: #dcfce7;
            }}
            .badge-bad {{
                background: #7f1d1d;
                color: #fee2e2;
            }}
            .badge-neutral {{
                background: #374151;
                color: #e5e7eb;
            }}
            .overall-safe {{
                border-left: 8px solid #22c55e;
            }}
            .overall-medium {{
                border-left: 8px solid #eab308;
            }}
            .overall-high {{
                border-left: 8px solid #f97316;
            }}
            .overall-critical {{
                border-left: 8px solid #ef4444;
            }}
            .chart-box {{
                background: {card_bg};
                border-radius: 12px;
                padding: 16px;
                margin: 0 0 22px 0;
                box-shadow: 0 4px 16px rgba(0,0,0,0.18);
            }}
            .chart-row {{
                display: flex;
                align-items: center;
                margin: 10px 0;
                gap: 12px;
            }}
            .chart-label {{
                width: 90px;
                font-weight: bold;
            }}
            .chart-bar-wrap {{
                flex: 1;
                background: #1f2937;
                border-radius: 999px;
                overflow: hidden;
                min-height: 28px;
            }}
            .chart-bar {{
                min-height: 28px;
                line-height: 28px;
                padding-left: 10px;
                font-weight: bold;
                color: white;
            }}
            .nmap-box {{
                margin-top: 10px;
                padding: 10px;
                border-radius: 8px;
                background: #1f2937;
                color: #d1d5db;
            }}
            .footer {{
                margin-top: 18px;
                font-size: 0.95rem;
                color: {muted};
            }}
        </style>
    </head>
    <body>
        <div class="intro">
            <h1>Reporte de análisis TLS</h1>
            <p>
                Este reporte evalúa la configuración TLS de uno o varios servicios web,
                identifica hallazgos de seguridad y traduce el análisis técnico en
                recomendaciones accionables.
            </p>
        </div>

        <div class="overall-banner {overall_class}">
            <strong>{overall_text}</strong><br>
            <span>Resumen visual de exposición para la muestra analizada.</span>
        </div>

        <h2>Resumen general</h2>
        <div class="summary-grid">
            <div class="card"><div>Total</div><div class="value">{summary['total']}</div></div>
            <div class="card"><div>LOW</div><div class="value">{summary['LOW']}</div></div>
            <div class="card"><div>MEDIUM</div><div class="value">{summary['MEDIUM']}</div></div>
            <div class="card"><div>HIGH</div><div class="value">{summary['HIGH']}</div></div>
            <div class="card"><div>CRITICAL</div><div class="value">{summary['CRITICAL']}</div></div>
        </div>

        <div class="chart-box">
            <h2>Distribución de riesgo</h2>
            {build_chart(summary)}
        </div>

        <table>
            <thead>
                <tr>
                    <th>Servidor</th>
                    <th>Versiones TLS</th>
                    <th>Hallazgos</th>
                    <th>Riesgo</th>
                    <th>Resumen ejecutivo</th>
                    <th>Recomendaciones</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>

        <div class="footer">
            Nota: la validación de versiones heredadas puede depender del soporte criptográfico del cliente local.
            Para mayor precisión, se recomienda contrastar con nmap, sslscan o testssl.sh.
        </div>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(html_content)


def parse_targets_from_file(file_path: str) -> List[str]:
    targets = []
    with open(file_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                targets.append(line)
    return targets


def main() -> None:
    parser = argparse.ArgumentParser(description="Analizador TLS final")
    parser.add_argument("targets", nargs="*", help="Dominios o IPs. Ej: google.com github.com:443")
    parser.add_argument("--file", help="Archivo con objetivos, uno por línea")
    parser.add_argument("--json", default="report_final.json", help="Salida JSON")
    parser.add_argument("--csv", default="report_final.csv", help="Salida CSV")
    parser.add_argument("--html", default="report_final.html", help="Salida HTML")
    parser.add_argument("--nmap", action="store_true", help="Activa validación cruzada con nmap")
    parser.add_argument("--light", action="store_true", help="Usa tema claro en HTML")
    args = parser.parse_args()

    input_targets = list(args.targets)
    if args.file:
        input_targets.extend(parse_targets_from_file(args.file))

    if not input_targets:
        print("Error: indique objetivos por línea de comandos o con --file")
        return

    results: List[ScanResult] = []

    for target in input_targets:
        try:
            result = analyze_target(target, use_nmap=args.nmap)
            print_console_report(result)
            results.append(result)
        except Exception as exc:
            print(f"[ERROR] {target}: {exc}")

    if results:
        save_json(results, args.json)
        save_csv(results, args.csv)
        save_html(results, args.html, dark_mode=not args.light)
        print(f"\nJSON generado: {args.json}")
        print(f"CSV generado: {args.csv}")
        print(f"HTML generado: {args.html}")


if __name__ == "__main__":
    main()