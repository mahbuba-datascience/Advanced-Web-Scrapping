# Advanced-Web-Scrapping

## Project Goal

This project aims to execute a complete ETL process. I will clean, transform, and store search results from multiple search engines into a database. Additionally, I will analyze and rank the search results to demonstrate the practical value of the project.

## My Approaches

To implement this project, I have outlined several steps:

**Extraction**

- Prompt the user to input search terms.
- Process the search terms by removing special characters, tokenization, removing stop words, and lemmatization.
- Utilize Search Engine 1: Use the Python Requests library to fetch search pages, parse the pages using Beautiful Soup, and extract URLs and titles.

**Transformation**

- Filter out ads using keywords and temporarily store results in a dataframe.
- Utilize Search Engine 2: Repeat the same steps until all search engines have been called, appending the results to the same dataframe.
- Remove duplicate URLs from the dataframe.

**Loading**

- Store the results in MySQL.

**Analysis**

- For each of the search results obtained, visit each URL page, retrieve the page text, count the occurrences of each token, and aggregate the results to obtain the frequency of each search term.
- Add the frequency results to each URL record.

**Web GUI**
The above steps are implemented in a notebook. To showcase the value of the custom bot, we need to create a web-based GUI.

- Utilize the Flask web framework to package the notebook code.
- Use the SQLAlchemy API to connect from the web server to the MySQL server, enabling data reading and writing.

## Key Considerations

**Build Database Schema**

Evaluate the datasets involved in the entire process and design an efficient and scalable schema.

**Assess the feasibility of methods**

- After evaluation, we found that storing web snapshots and then converting images to text was inefficient. Therefore, we decided to abandon this approach.
- Using the Python Requests library and parsing HTML with Beautiful Soup proved to be more efficient and accurate.

**Calculation method for URL frequency**

The guidelines did not clearly define the calculation of frequency, which added some difficulty.

- Initially, I only counted the frequency of URLs. However, this result was not ideal and lacked reference value. For example, if I have data from five search engines, a URL could appear up to five times, which only indicates that the URL has been indexed by different search engines, but does not reflect the relevance between the URL and the search term.

- Later, I changed my approach to counting the occurrences of each search term on each URL page. I removed special characters from the search term, split it into tokens, removed stopwords, and performed stemming. Then, I counted the number of occurrences of each token on the URL page and summed them to obtain the frequency of the search term on that page. This approach reflects the relevance between the search term and the URL. Although it differs significantly from ranking algorithms used by companies like Google, it allows us to gain insights into the association between search terms and URLs.

## Conclusion

This project provides valuable hands-on experience in ETL (Extract, Transform, Load) operations. In terms of technical difficulty, the requirements for this project are not too high. The main challenges of the project lie in the unclear requirements and definitions, which add difficulty to the project execution.
