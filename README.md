📜 PubMed Paper Fetcher
📌 Description
PubMed Paper Fetcher is a Python-based CLI tool that allows users to search and retrieve research papers from PubMed based on specific queries. It leverages the Entrez API to fetch metadata such as title, author, publication year, and abstract, making it easier for researchers and students to find relevant papers.

🛠 Installation Steps
Follow these steps to set up the project on your local machine:

1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/Tejashwini2903/PubMed-Paper-Fetcher.git
cd PubMed-Paper-Fetcher
2️⃣ Install Dependencies using Poetry
Make sure you have Poetry installed. If not, install it first:

sh
Copy
Edit
pip install poetry
Now, install the required dependencies:

sh
Copy
Edit
poetry install
3️⃣ Set Up Environment Variables (Optional)
Create a .env file and add your NCBI API Key for better rate limits:

ini
Copy
Edit
NCBI_API_KEY=your_api_key_here
4️⃣ Run the Script
To search for papers related to cancer treatment, run:

sh
Copy
Edit
poetry run get-papers-list "cancer treatment"
📌 Usage Instructions
Open the terminal and navigate to the project folder.

Run the command:

sh
Copy
Edit
poetry run get-papers-list "your search query"
The tool will fetch relevant research papers and display them.

Example output:
yaml
Copy
Edit
🔍 Searching for papers related to 'cancer treatment'...
1️⃣ Title: Advances in Cancer Immunotherapy
   Author: John Doe et al.
   Year: 2023
   Abstract: This paper explores...
📋 Requirements
Python 3.8+
Poetry (for dependency management)
Requests & xmltodict libraries

