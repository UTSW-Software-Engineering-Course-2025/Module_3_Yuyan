# GeneGPT NCBI API Cheatsheet

This cheatsheet provides a summary of NCBI E-utils and BLAST URL APIs as described in the GeneGPT paper

## NCBI API Keys & Rate Limiting

The first step is to get an API key from NCBI. Without an API key, you will be limited to 3 requests per second. With an API key, you can make up to 10 requests per second.

### How to get an API key

1. Sign in to your NCBI account: https://www.ncbi.nlm.nih.gov/account/
2. If you do not yet have an account, you can still acquire an account through your UTSW credentials. 
3. Click on "more login options"
4. Search for "UT Southwestern Medical Center" in the login-provider page.
5. Once signed in, access your account's settings by clicking on your user name which is displayed in the top right corner of any NCBI page.
6. Scroll down the page to the section entitled API Key Management.
7. Click the Create an API Key button, which will generate a key (unique sequence of characters) displayed in the API Key Management box.

### How to use your API key in Python requests
*   Include your API key as a URL parameter named `api_key` in your E-utils requests.
*   **Example:**
    You can append API key to the end of the URL like this:

    `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=LMP10&api_key=YOUR_API_KEY`
    
    or if using Python `requests` library, you can include it in the `params` dictionary
*   **Python `requests` example:**
    ```python
    import requests

    api_key = "YOUR_ACTUAL_API_KEY" # Store your key securely
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=LMP10"
    params = {
        "api_key": api_key
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Process your data
        print(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")
    ```
### How to deal with rate limits
Exceeding your rate limits (3 requests/sec without a key, 10 requests/sec with a key) will result in error messages (often HTTP status code 429), and potentially temporary blocking of your IP address. To avoid this when calling the NCBI API:

1. Always include your API key in your requests.
2. Use robust request handling with retries and exponential backoff.
3. The following code is an example of how to do this

    ```python
    def call_api(url: str, params: dict | None = None, timeout: int = 60, max_retries: int = 3) -> bytes:
        """
        Perform an HTTP GET request to the given URL (with optional params) and return raw bytes.
        Retries with exponential back-off (up to 3 times) on rate limit or server errors.
        """
        base_delay = 1  # seconds
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.5)
                    logging.warning(f"API request failed (attempt {attempt+1}/{max_retries}): Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                response = requests.get(url, params=params, timeout=timeout)
                response.raise_for_status()
                return response.content
            except requests.exceptions.RequestException as e:
                status = getattr(e.response, "status_code", None)
                if status in [429, 500, 502, 503, 504] or isinstance(e, requests.exceptions.Timeout):
                    continue  # retry
                else:
                    logging.error(f"API request failed: {e}")
                    raise
        logging.error(f"API request failed after {max_retries} retries: {url} params={params}")
        raise RuntimeError(f"API request failed after {max_retries} retries: {url} params={params}")
    ```


## NCBI E-utils API

E-utils provide access to the Entrez portal, which encompasses 38 NCBI databases containing biomedical data like genes and proteins. They use a fixed URL syntax for retrieving this information

**Base URL:**
* `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/{function_name}.fcgi` 
    * Where `{function_name}` can be `esearch`, `efetch`, or `esummary`.

**Workflow:**
1.  Use `esearch` to get unique database identifiers (UIDs) for a given query term
2.  Use `esummary` with UIDs to get text summaries.
3.  Use `efetch` with UIDs to get full records.

**Key Parameters (for E-utils URL requests):**
* `db`: The database to use (e.g., `gene`, `snp`, `omim`).
* `term`: The search term (used with `esearch`).
* `id`: The unique database identifier(s) (UIDs) (used with `efetch` or `esummary`). For multiple UIDs, this is a comma-separated list.
* `retmax`: The maximum number of items to return.
* `retmode`: The format for returned data (e.g., `json`, `text`, `xml`).

**Syntax:**
* `"[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/[esearch|efetch|esummary].fcgi?db={gene|snp|omim}&retmax=[]&{term|id}=]"` 

**E-utils Examples:**

1.  **Alias Lookup (Gene Symbol for LMP10)** 
    * **Goal:** Find the official gene symbol for an alias.
    * **Step 1: `esearch` (to find UID for LMP10 in `gene` database)**
        ```
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&retmax=3&retmode=json&term=LMP10"
        ```
    * **Step 2: `esummary` (to get gene record using UID from esearch)**
        ```
         "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&retmode=json&id=19171,5699,8138"
        ```
    * **Example Answer:** PSMB10


## NCBI BLAST URL API

The BLAST (Basic Local Alignment Search Tool) API is used to find regions of similarity between nucleotide or protein sequences and sequences in a database. This can help infer relationships between sequences or identify members of gene families. Users can submit queries and retrieve results from NCBI servers via this API.

**Base URL:**
* `https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi` 

**Key `CMD` (Command) Parameter:** 
* `CMD=Put`: Submits a BLAST search query.
* `CMD=Get`: Retrieves the results of a submitted query using its Request ID (RID).

**Parameters for `CMD=Put`:**
* `DATABASE`: The database to search against (e.g., `nt` for nucleotide collection).
* `PROGRAM`: The BLAST program to use (e.g., `blastn` for nucleotide query vs. nucleotide database).
* `QUERY`: The sequence to be searched.
* `HITLIST_SIZE`: Maximum number of hits to return (optional, example from paper).
* `FORMAT_TYPE`: Desired format for the eventual results, can be specified at Put or Get (e.g., `XML`, `Text`).
* *(A Request ID (`RID`) is returned after a successful `CMD=Put` call, which is used to retrieve results)*.

**Parameters for `CMD=Get`:**
* `RID`: The Request ID obtained from a `CMD=Put` call.
* `FORMAT_TYPE`: The desired output format (e.g., `XML`, `Text`)

**Syntax:**
* `"[https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD={Put|Get}&PROGRAM=blastn&MEGABLAST=on&DATABASE=nt&FORMAT_TYPE={XML|Text}&QUERY={sequence}&HITLIST_SIZE={max_hit_size}]"` 
    *(Note: `MEGABLAST=on` is an option for blastn shown in the documentation example)*.

**BLAST Example:**
* **Goal:** Align a DNA sequence.
* **Step 1: `CMD=Put` (Submit sequence for BLAST search)**
    ```
    https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Put&PROGRAM=blastn&MEGABLAST=on&DATABASE=nt&FORMAT_TYPE=XML&QUERY=[YOUR_DNA_SEQUENCE]&HITLIST_SIZE=5
    ```
    *(DNA sequences are very long to input the full sequence from paper but you get the idea)*
* **Extract the RID from the response** (see sample code below)
    ```python
    def extract_rid_simple(response_bytes):
        """Extracts an NCBI BLAST Request ID (RID) from a byte string.

        This function decodes the input byte string (typically the output from an
        HTTP request to NCBI BLAST) to UTF-8 and uses a regular expression
        to find a line like "RID = <VALUE>\n".

        Args:
            response_bytes (bytes): The byte string response from an HTTP request,
                                    expected to contain an NCBI RID.

        Returns:
            str | None: The extracted RID as a string, stripped of any leading or
                        trailing whitespace, if the pattern is found. Returns None otherwise.
        """
        if not response_bytes:
            return None
        match = re.search(r'RID\s*=\s*([A-Z0-9]+)', response_bytes.decode('utf-8', errors='ignore'))
        return match.group(1).strip() if match else None
    ```
* **(Wait for RID to be processed)**
* **Step 2: `CMD=Get` (Retrieve BLAST results using RID)**
    ```
    https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&FORMAT_TYPE=Text&RID=[RID_FROM_CMD_PUT]
    ```