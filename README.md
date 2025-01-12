# text-converter
This short Python script will convert a raw `.txt` file to a structured `.csv`


---

## **<mark style="background: #BBFABBA6;">1. Prerequisites</mark>**

- **Python Installation**: 
	- Ensure Python is installed on your machine (preferably version 3.7 or later).
- **Required Libraries**:
    - `pandas`
    - `rapidfuzz`
- If not installed, the following commands can be used to install them:
    
    ```bash
    pip install pandas
    pip install rapidfuzz
    ```
    

---

## **<mark style="background: #BBFABBA6;">2. Input File</mark>**

- **Location**: Replace the `file_path` variable with the path to your `.txt` file:
    
    ```python
    file_path = r"C:\Users\edwar\Downloads\SVSWebTests.txt"
    ```
    
- **Content Format**:
    - Static headers like `"Department:"`, `"Test Code:"` should precede their values.
    - Nested or bullet-pointed subfields (e.g., `* Colour: Red Top`) will be processed correctly.

---

## **<mark style="background: #BBFABBA6;">3. Output Files</mark>**

- **Tabulated Data**: The script saves the extracted and formatted data to `output_file`. Update the file path:
    
    ```python
    output_file = r"C:\Users\edwar\Downloads\SVSWebTests_Tabulated.csv"
    ```
    
- **Incomplete Records Log**: If any records are incomplete, they are logged in `log_file` with the line number and a timestamp. You can use this to manually update your output file. Update the file path:
    
    ```python
    log_file = r"C:\Users\edwar\Downloads\Incomplete_Log.txt"
    ```
    

---

## **<mark style="background: #BBFABBA6;">4. Header Matching</mark>**

**Static Header Matching**

- Headers like `"Department:"` are matched exactly using `static_headers`. To add or change headers:
    
    ```python
    static_headers = {
        "New Header": "New Header Keyword:"
    }
    ```
    
**Fuzzy Header Matching**

- Handles variable headers (e.g., `"Clinical Information"`). To add new headers:
    
    ```python
    fuzzy_headers = ["New Fuzzy Header"]
    ```
    

---

## **<mark style="background: #BBFABBA6;">5. Running the Script</mark>**

1. Open a terminal or command prompt.
2. Navigate to the folder containing the script:
    
    ```bash
    cd C:\path\to\script
    ```
    
3. Run the script:
    
    ```bash
    python script_name.py
    ```
    
4. Check the output:
    - The CSV will contain the structured data.
    - The log file will detail any incomplete records.

---

## **<mark style="background: #BBFABBA6;">6. How to Amend the Script</mark>**

**Adjust Fuzzy Matching Sensitivity**

- By default, the fuzzy matching threshold is set at `80`. If your headers are prone to small variations, you can lower this threshold for example to `60`:
    
    ```python
    if fuzz.partial_ratio(header.lower(), line.lower()) > 80:
    ```
    

**Change Multiline Handling**

- Multiline values append to the last detected header. If you want to log unmatched multiline data, modify this block:
    
    ```python
    if not matched:
        previous_key = list(current_row.keys())[-1] if current_row else None
        if previous_key:
            current_row[previous_key] += " " + line
        else:
            print(f"Warning: Multiline data without a preceding header at line {line_number}.")
    ```
    

---

## **<mark style="background: #BBFABBA6;">7. Troubleshooting</mark>**

**File Not Found**
- Ensure the `file_path` points to the correct location of your `.txt` file.

**Empty Output**
- If no data is saved to the CSV, check:
    - The `.txt` file uses headers defined in `static_headers` or matches `fuzzy_headers`.
    - The file is not empty.

**Incomplete Records**
- Review the `Incomplete_Log.txt` for skipped or partially processed records.
