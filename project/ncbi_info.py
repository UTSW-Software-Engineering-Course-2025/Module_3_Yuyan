import re
import time
from typing import List

import requests


def extract_rid_simple(response_bytes):
    """Extracts an NCBI BLAST Request ID (RID) from a byte string."""
    if not response_bytes:
        return None
    match = re.search(
        r"RID\s*=\s*([A-Z0-9]+)", response_bytes.decode("utf-8", errors="ignore")
    )
    return match.group(1).strip() if match else None


def blast_sequence(sequence, hitlist_size=5):
    """Submit a DNA sequence to NCBI BLAST and retrieve results."""
    # Step 1: Submit sequence
    params = {
        "CMD": "Put",
        "PROGRAM": "blastn",
        "MEGABLAST": "on",
        "DATABASE": "nt",
        "FORMAT_TYPE": "Text",
        "QUERY": sequence,
        "HITLIST_SIZE": str(hitlist_size),
    }
    put_response = requests.post(
        "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi", data=params
    )
    rid = extract_rid_simple(put_response.content)
    if not rid:
        return "Failed to retrieve RID."

    # Step 2: Poll for results
    for _ in range(10):
        time.sleep(10)
        get_response = requests.get(
            "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi",
            params={"CMD": "Get", "FORMAT_TYPE": "Text", "RID": rid},
        )
        if "Status=WAITING" not in get_response.text:
            return get_response.text
    return "Timed out waiting for BLAST results."


def get_official_symbol_from_alias(alias, email, api_key):
    """Find official gene symbol from alias using NCBI Entrez esearch + esummary."""
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esummary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    esearch_params = {
        "db": "gene",
        "retmax": 3,
        "retmode": "json",
        "term": alias,
        "email": email,
        "api_key": api_key,
    }
    search_resp = requests.get(esearch_url, params=esearch_params).json()
    id_list = search_resp.get("esearchresult", {}).get("idlist", [])
    if not id_list:
        return []

    esummary_params = {
        "db": "gene",
        "retmode": "json",
        "id": ",".join(id_list),
        "email": email,
        "api_key": api_key,
    }
    summary_resp = requests.get(esummary_url, params=esummary_params).json()
    summaries = summary_resp.get("result", {})
    summaries.pop("uids", None)
    return [summaries[uid]["name"] for uid in summaries if "name" in summaries[uid]]


import requests


def get_gene_uid(symbols: List[str]) -> List[str]:
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "gene", "retmode": "json", "term": " OR ".join(symbols)}
    r = requests.get(url, params=params)
    r.raise_for_status()
    uids = r.json()["esearchresult"]["idlist"]
    return uids  # might be multiple UIDs


def get_gene_aliases(uids: list[str]) -> list[str]:
    if not uids:
        return []

    uid_str = ",".join(uids)
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {"db": "gene", "retmode": "json", "id": uid_str}

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json().get("result", {})
    except Exception as e:
        print(f"[ERROR] Failed to fetch gene aliases: {e}")
        return []

    aliases = []

    for uid in uids:
        item = data.get(uid)
        if not item:
            continue
        # Safely get alias list and official name
        alias_str = item.get("otheraliases", "")
        alias_list = [a.strip() for a in alias_str.split(",") if a.strip()]
        official_name = item.get("name")
        if official_name:
            alias_list.append(official_name)
        aliases.extend(alias_list)

    return list(set(aliases))


def extract_gene_symbols_from_blast(blast_text: str):
    """
    Extracts gene symbols from BLAST alignment section using parentheses at the end of description lines.
    """
    gene_symbols = set()
    for line in blast_text.splitlines():
        match = re.search(r"\(([^)]+)\)", line)
        if match:
            symbol = match.group(1).strip()
            # Basic filter: uppercase, not numeric, not LOC*
            if (
                symbol.isupper()
                and not symbol.startswith("LOC")
                and not symbol.isdigit()
            ):
                gene_symbols.add(symbol)
    return list(gene_symbols)


def get_gene_from_snp(snp_id: str) -> str:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {"db": "snp", "id": snp_id.replace("rs", ""), "retmode": "json"}
    r = requests.get(url, params=params)
    r.raise_for_status()
    doc = r.json()
    try:
        gene_info = doc["result"][snp_id]["genename"]
        return gene_info
    except Exception:
        return None


def get_gene_locations_by_disease(disease_name: str) -> dict:
    # Step 1: Search gene linked to disease
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esearch_params = {"db": "gene", "term": disease_name, "retmode": "json"}
    search_resp = requests.get(esearch_url, params=esearch_params).json()
    gene_ids = search_resp["esearchresult"]["idlist"]

    # Step 2: Get gene summaries including chromosomal location
    if not gene_ids:
        return {}

    esummary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    esummary_params = {"db": "gene", "id": ",".join(gene_ids), "retmode": "json"}
    summary_resp = requests.get(esummary_url, params=esummary_params).json()

    locations = {}
    for gid in gene_ids:
        item = summary_resp["result"].get(gid)
        if item:
            locations[item["name"]] = item.get("maplocation", "unknown")

    return locations


def build_ncbi_info(dna_seq: str, disease: str = None, snp: str = None) -> dict:
    ncbi_info = {}

    # If you have a DNA sequence, run BLAST to find the gene
    if dna_seq:
        blast_result = blast_sequence(dna_seq)
        gene_symbols = extract_gene_symbols_from_blast(blast_result)
        if gene_symbols:
            ncbi_info["gene"] = gene_symbols[0]  # assume first is best hit
            uids = get_gene_uid([gene_symbols[0]])
            aliases = get_gene_aliases(uids)
            ncbi_info["aliases"] = aliases

    # If it's a disease -> gene location task
    if disease:
        gene_locs = get_gene_locations_from_disease(disease)
        ncbi_info["location"] = gene_locs

    # If it's an SNP query (like "What gene is associated with SNP rsXXXX?")
    if snp:
        snp_gene = get_gene_from_snp(snp)
        ncbi_info["gene"] = snp_gene
        uids = get_gene_uid([snp_gene])
        aliases = get_gene_aliases(uids)
        ncbi_info["aliases"] = aliases

    return ncbi_info


def dispatch_ncbi_data(task: str, question: str) -> dict:
    if task == "sequence gene alias":
        return build_ncbi_info(dna_seq=question)  # BLAST-based
    elif task == "Disease gene location":
        return {"location": get_gene_locations_by_disease(question)}
    elif task == "SNP gene function":
        return build_ncbi_info(dna_seq=None, snp=question)  # use SNP info
    else:
        return {}


def format_ncbi_data(ncbi_info: dict) -> str:
    lines = []

    if "gene" in ncbi_info:
        lines.append(f"The gene identified is {ncbi_info['gene']}.")

    if "aliases" in ncbi_info:
        alias_str = ", ".join(ncbi_info["aliases"])
        lines.append(f"Its known aliases include: {alias_str}.")

    if "location" in ncbi_info and isinstance(ncbi_info["location"], dict):
        locs = [
            f"{gene}: Chromosome {loc}" for gene, loc in ncbi_info["location"].items()
        ]
        loc_str = "; ".join(locs)
        lines.append(f"The following gene locations were found: {loc_str}.")

    return " ".join(lines)


# Example Usage
dna_seq = "GTAGATGGAACTGGTAGTCAGCTGGAGAGCAGCATGGAGGCGTCCTGGGGGAGCTTCAACGCTGAGCGGGGCTGGTATGTCTCTGTCCAGCAGCCTGAAGAAGCGGAGGCCGA"
blast_result = blast_sequence(dna_seq)
gene_symbols = extract_gene_symbols_from_blast(blast_result)
uids = get_gene_uid(gene_symbols)
aliases = get_gene_aliases(uids)
# print(gene_symbols)
# print(uids)
# print(aliases)
