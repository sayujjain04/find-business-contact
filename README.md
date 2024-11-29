# Company Data Enrichment Toolkit

This script is a powerful data enrichment tool designed to collect and organize publicly available information about companies. It uses web scraping, search engine queries, and data extraction techniques to gather details like company websites, emails, phone numbers, addresses, and social media links.

---

## Features

### 1. **Domain Finder**
   - **Input**: Company name.
   - **Output**: Official company website URL.
   - Uses Google search results to identify the most relevant company domain.

### 2. **Email Extraction**
   - **Input**: Company name and/or website.
   - **Output**: Publicly available email addresses and the webpages where they were found.
   - Filters results to ensure emails originate from the identified company domain.

### 3. **Phone Number Extraction**
   - **Input**: Company webpages.
   - **Output**: Phone numbers found in the webpage text.
   - Utilizes regex to locate various phone number formats.

### 4. **Address Extraction**
   - **Input**: Company webpages.
   - **Output**: Physical addresses found using both schema.org tags and regex patterns.
   - Cross-references structured data and unstructured HTML text.

### 5. **Social Media Links**
   - **Input**: Company webpages.
   - **Output**: Links to official company profiles on platforms like Facebook, Twitter, LinkedIn, Instagram, etc.
   - Ensures social media links are specific to the company's domain.

### 6. **Webpage Scraping**
   - Retrieves and processes raw HTML from key company webpages, such as `Contact`, `About`, or `FAQ` pages, to extract relevant data.

### 7. **TOR Integration for Anonymity**
   - Uses TOR for web scraping to anonymize traffic.
   - Includes functions to renew TOR IP and configure Selenium WebDriver to route through TOR.

### 8. **Selenium-Based Scraping**
   - Utilizes Selenium to interact with dynamic content on webpages.
   - Ensures robust scraping capabilities for modern, JavaScript-heavy sites.

---

## Setup and Requirements

### Prerequisites
- **Python 3.7+**
- **Dependencies**: Install the required Python libraries:
  ```bash
  pip install requests beautifulsoup4 selenium stem
  ```
- **TOR**: Install and configure TOR on your system:
  1. Install TOR:
     ```bash
     sudo apt-get install tor
     ```
  2. Configure `torrc` file:
     ```
     ControlPort 9051
     HashedControlPassword 16:YOUR_HASHED_PASSWORD_HERE
     CookieAuthentication 1
     ```
  3. Start the TOR service:
     ```bash
     sudo service tor start
     ```
  4. Generate a hashed password for TOR:
     ```bash
     tor --hash-password your_password
     ```

---

## How It Works

### Main Workflow
1. **Domain Identification**:
   - Searches Google for the company name and extracts the domain with the fewest subdirectories.

2. **Relevant Link Collection**:
   - Collects links from the company domain and Google search results for key terms like "Contact" or "About."

3. **Data Extraction**:
   - Scrapes relevant company links to extract:
     - **Emails**: Validated against the company domain.
     - **Phone Numbers**: Extracted using regex patterns.
     - **Addresses**: Found via schema.org tags and regex.
     - **Social Media Links**: Identified for major platforms.

4. **TOR-Supported Anonymity**:
   - Routes all traffic through TOR for anonymity and refreshes the IP every 5 requests.

---

## Running the Script

### Basic Execution
```python
python script_name.py
```

### Customization
Modify the `main()` function to set the company name and domain:
```python
main(name="Example Company", domain="example.com")
```
If the domain is not provided, the script will attempt to find it automatically.

---

## Outputs
- **Domain**: Official website URL.
- **Emails**: List of public company emails with corresponding webpages.
- **Phone Numbers**: Company phone numbers extracted from text.
- **Addresses**: Physical addresses associated with the company.
- **Social Media Links**: Official links to the company's social media profiles.

---

## Limitations and Future Work
1. **Verification**: Add email and address verification against databases.
2. **Social Media**: Enhance functionality to include more platforms.
3. **Databases**: Integrate checks against public databases for additional accuracy.

---

## License
This project is open-source and available under the MIT License.