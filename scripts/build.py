#!/usr/bin/env python3
"""Deterministic rule builder: merge MetaCubeX upstreams with local patches and compile .mrs/.list/DOMAIN-SET/catalog."""

from __future__ import annotations

import argparse
import ipaddress
import json
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def fetch_text(url: str, retries: int = 3) -> str:
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "w0ven-routing-rules-builder/1.2"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            if attempt < retries:
                time.sleep(attempt * 2)
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")


def strip_comment(line: str) -> str:
    line = line.strip()
    if not line or line.startswith("#") or line.startswith(";"):
        return ""
    if " #" in line:
        line = line.split(" #", 1)[0].strip()
    return line


def normalize_domain_entry(raw: str) -> str | None:
    line = strip_comment(raw)
    if not line:
        return None
    if line.startswith("- "):
        line = line[2:].strip()

    upper = line.upper()
    if upper.startswith("DOMAIN-SUFFIX,"):
        dom = line.split(",", 2)[1].strip().lower().lstrip(".")
        return f"+.{dom}" if dom else None
    if upper.startswith("DOMAIN,"):
        dom = line.split(",", 2)[1].strip().lower().lstrip(".")
        return dom if dom else None
    if "," in line:
        return None

    dom = line.lower()
    if dom.startswith("+."):
        dom = dom[2:].lstrip(".")
        return f"+.{dom}" if dom else None
    if dom.startswith("."):
        dom = dom.lstrip(".")
        return f"+.{dom}" if dom else None
    if dom.startswith("*."):
        dom = dom[2:].lstrip(".")
        return f"+.{dom}" if dom else None
    return dom


def normalize_ipcidr_entry(raw: str) -> str | None:
    line = strip_comment(raw)
    if not line:
        return None
    if line.startswith("- "):
        line = line[2:].strip()
    upper = line.upper()
    if upper.startswith("IP-CIDR,") or upper.startswith("IP-CIDR6,"):
        line = line.split(",", 2)[1].strip()
    net = ipaddress.ip_network(line, strict=False)
    return str(net)


def domain_to_classical(entry: str) -> str:
    if entry.startswith("+."):
        return f"DOMAIN-SUFFIX,{entry[2:]}"
    return f"DOMAIN,{entry}"


def domain_to_surge_domain_set(entry: str) -> str:
    if entry.startswith("+."):
        return f".{entry[2:]}"
    return entry


def ipcidr_to_classical(entry: str) -> str:
    net = ipaddress.ip_network(entry, strict=False)
    kind = "IP-CIDR6" if net.version == 6 else "IP-CIDR"
    return f"{kind},{entry},no-resolve"


def sort_domains(entries: set[str]) -> list[str]:
    def key(item: str) -> tuple[list[str], int, str]:
        is_suffix = item.startswith("+.")
        host = item[2:] if is_suffix else item
        labels = list(reversed(host.split(".")))
        return (labels, 0 if is_suffix else 1, item)

    return sorted(entries, key=key)


def sort_cidrs(entries: set[str]) -> list[str]:
    def key(item: str) -> tuple[int, int, int]:
        net = ipaddress.ip_network(item, strict=False)
        return (net.version, int(net.network_address), net.prefixlen)

    return sorted(entries, key=key)


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def compile_mrs(mihomo_bin: str, behavior: str, src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [mihomo_bin, "convert-ruleset", behavior, "text", str(src), str(dst)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"mihomo convert-ruleset failed for {src}: {proc.stderr or proc.stdout}"
        )


def parse_sgmodule_meta(text: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#!") and "=" in s:
            k, v = s[2:].split("=", 1)
            meta[k.strip()] = v.strip()
        elif s and not s.startswith("#"):
            break
    return meta


def build_all(out_dir: Path, mihomo_bin: str | None) -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    upstream_base: str = manifest["upstream_base"]
    upstream_cache: dict[str, list[str]] = {}

    def get_upstream(rel_path: str) -> list[str]:
        if rel_path not in upstream_cache:
            url = upstream_base + rel_path
            print(f"[fetch] {url}")
            upstream_cache[rel_path] = fetch_text(url).splitlines()
        return upstream_cache[rel_path]

    if out_dir.exists():
        shutil.rmtree(out_dir)

    dom_dir = out_dir / "mihomo" / "domain"
    ip_dir = out_dir / "mihomo" / "ip"
    cls_dir = out_dir / "mihomo" / "classical"
    surge_dir = out_dir / "surge"
    surge_dset_dir = surge_dir / "domain-set"
    surge_mod_dir = surge_dir / "modules"
    for d in (dom_dir, ip_dir, cls_dir, surge_dir, surge_dset_dir, surge_mod_dir):
        d.mkdir(parents=True, exist_ok=True)

    built_entries: dict[str, set[str]] = {}
    summary_rows: list[tuple[str, str, int, int, str]] = []
    catalog_rulesets: list[dict[str, object]] = []

    for spec in manifest["rulesets"]:
        name: str = spec["name"]
        rtype: str = spec["type"]
        category: str = spec.get("category", "core")
        default_policy: str = spec.get("default_policy", "Proxy")
        desc: str = spec.get("description", "")
        skip_classical: bool = bool(spec.get("skip_classical", False))

        items: set[str] = set()
        extra_ips: set[str] = set()

        for inc in spec.get("include_sets", []):
            if inc not in built_entries:
                raise RuntimeError(
                    f"Ruleset '{name}' references '{inc}' before it was built"
                )
            items.update(built_entries[inc])

        normalizer = (
            normalize_domain_entry if rtype == "domain" else normalize_ipcidr_entry
        )

        for up in spec.get("upstreams", []):
            for line in get_upstream(up):
                norm = normalizer(line)
                if norm:
                    items.add(norm)

        for patch_rel in spec.get("patches", []):
            for line in read_lines(ROOT / patch_rel):
                norm = normalizer(line)
                if norm:
                    items.add(norm)

        for excl_rel in spec.get("excludes", []):
            for line in read_lines(ROOT / excl_rel):
                norm = normalizer(line)
                if norm:
                    items.discard(norm)

        for ip_up in spec.get("ip_upstreams", []):
            for line in get_upstream(ip_up):
                norm_ip = normalize_ipcidr_entry(line)
                if norm_ip:
                    extra_ips.add(norm_ip)

        built_entries[name] = set(items)

        classical_extra: list[str] = []
        for extra_rel in spec.get("classical_extra", []):
            for line in read_lines(ROOT / extra_rel):
                cleaned = strip_comment(line)
                if cleaned:
                    classical_extra.append(cleaned)

        paths: dict[str, str] = {}
        has_extra_rules = bool(extra_ips or classical_extra)

        if rtype == "domain":
            ordered = sort_domains(items)
            txt_path = dom_dir / f"{name}.txt"
            txt_path.write_text("\n".join(ordered) + "\n", encoding="utf-8")
            paths["mihomo_txt"] = f"mihomo/domain/{name}.txt"

            dset_lines = [domain_to_surge_domain_set(x) for x in ordered]
            (surge_dset_dir / f"{name}.txt").write_text(
                "\n".join(dset_lines) + "\n", encoding="utf-8"
            )
            paths["surge_domain_set"] = f"surge/domain-set/{name}.txt"

            if mihomo_bin:
                compile_mrs(mihomo_bin, "domain", txt_path, dom_dir / f"{name}.mrs")
            paths["mihomo_mrs"] = f"mihomo/domain/{name}.mrs"

            ordered_ips = sort_cidrs(extra_ips)
            if not skip_classical:
                classical_lines = [domain_to_classical(x) for x in ordered]
                for cidr in ordered_ips:
                    classical_lines.append(ipcidr_to_classical(cidr))
                for extra in classical_extra:
                    if extra not in classical_lines:
                        classical_lines.append(extra)
                classical_body = "\n".join(classical_lines) + "\n"
                (cls_dir / f"{name}.list").write_text(classical_body, encoding="utf-8")
                (surge_dir / f"{name}.list").write_text(classical_body, encoding="utf-8")
                paths["classical_list"] = f"mihomo/classical/{name}.list"
                paths["surge_list"] = f"surge/{name}.list"

            summary_rows.append((name, "domain", len(ordered), len(ordered_ips) + len(classical_extra), desc))
            surge_recommended = "rule-set" if (has_extra_rules and not skip_classical) else "domain-set"
            catalog_rulesets.append({
                "name": name,
                "type": "domain",
                "category": category,
                "defaultPolicy": default_policy,
                "description": desc,
                "entries": len(ordered),
                "extraEntries": len(ordered_ips) + len(classical_extra),
                "noResolve": bool(ordered_ips or any("IP-" in x.upper() for x in classical_extra)),
                "surgeRecommended": surge_recommended,
                "paths": paths,
            })
        elif rtype == "ipcidr":
            ordered = sort_cidrs(items)
            txt_path = ip_dir / f"{name}.txt"
            txt_path.write_text("\n".join(ordered) + "\n", encoding="utf-8")
            paths["mihomo_txt"] = f"mihomo/ip/{name}.txt"

            if mihomo_bin:
                compile_mrs(mihomo_bin, "ipcidr", txt_path, ip_dir / f"{name}.mrs")
            paths["mihomo_mrs"] = f"mihomo/ip/{name}.mrs"

            if not skip_classical:
                classical_lines = [ipcidr_to_classical(x) for x in ordered]
                for extra in classical_extra:
                    if extra not in classical_lines:
                        classical_lines.append(extra)
                classical_body = "\n".join(classical_lines) + "\n"
                (cls_dir / f"{name}.list").write_text(classical_body, encoding="utf-8")
                (surge_dir / f"{name}.list").write_text(classical_body, encoding="utf-8")
                paths["classical_list"] = f"mihomo/classical/{name}.list"
                paths["surge_list"] = f"surge/{name}.list"

            summary_rows.append((name, "ipcidr", len(ordered), len(classical_extra), desc))
            catalog_rulesets.append({
                "name": name,
                "type": "ipcidr",
                "category": category,
                "defaultPolicy": default_policy,
                "description": desc,
                "entries": len(ordered),
                "extraEntries": len(classical_extra),
                "noResolve": True,
                "surgeRecommended": "rule-set",
                "paths": paths,
            })
        else:
            raise ValueError(f"Unsupported ruleset type: {rtype}")

        extra_cnt = len(extra_ips) + len(classical_extra)
        note = f" (+{extra_cnt} extra)" if extra_cnt else ""
        print(f"[built] {name:<20} ({rtype:<6}) -> {len(ordered)} entries{note}")

    # Copy & index Surge modules
    catalog_modules: list[dict[str, object]] = []
    for mod in manifest.get("modules", []):
        src = ROOT / mod["source"]
        text = src.read_text(encoding="utf-8")
        dst = surge_mod_dir / mod["filename"]
        dst.write_text(text, encoding="utf-8")
        meta = parse_sgmodule_meta(text)
        lines_list = text.splitlines()
        catalog_modules.append({
            "id": mod["id"],
            "name": meta.get("name", mod["id"]),
            "description": meta.get("desc", ""),
            "category": meta.get("category", "模块"),
            "version": meta.get("version", ""),
            "notes": mod.get("notes", ""),
            "path": f"surge/modules/{mod['filename']}",
            "lineCount": len(lines_list),
            "sizeBytes": len(text.encode("utf-8")),
            "preview": "\n".join(lines_list[:24]),
        })
        print(f"[module] {mod['id']:<19} -> surge/modules/{mod['filename']} ({len(lines_list)} lines)")

    # Write deterministic SUMMARY.md
    lines = [
        "# Built Rulesets Summary",
        "",
        "| Ruleset | Type | Entries | Extra Rules (List) | Description |",
        "|---|---:|---:|---:|---|",
    ]
    for name, rtype, count, extra_cnt, desc in summary_rows:
        lines.append(f"| `{name}` | `{rtype}` | {count} | {extra_cnt} | {desc} |")
    lines.append("")
    (out_dir / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")

    # Write deterministic catalog.json for static navigation site
    catalog = {
        "repo": manifest.get("repo", {"owner": "w0ven", "name": "routing-rules", "release_branch": "release"}),
        "categories": manifest.get("categories", []),
        "stats": {
            "rulesetCount": len(catalog_rulesets),
            "moduleCount": len(catalog_modules),
            "totalEntries": sum(int(r["entries"]) for r in catalog_rulesets),
        },
        "modules": catalog_modules,
        "rulesets": catalog_rulesets,
    }
    (out_dir / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Copy static site & .nojekyll for GitHub Pages on release branch
    site_index = ROOT / "site" / "index.html"
    if site_index.exists():
        shutil.copyfile(site_index, out_dir / "index.html")
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build routing rulesets")
    parser.add_argument("--out", default="dist", help="Output directory")
    parser.add_argument(
        "--mihomo",
        default=None,
        help="Path to mihomo binary for compiling .mrs rulesets",
    )
    args = parser.parse_args()
    build_all(Path(args.out), args.mihomo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
