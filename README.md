# data_task
Description:

This project extracts product information from a ZIP file containing multiple HTML files. 
The script parses the HTML content and retrieves product details like name, price, currency, short description, rating, and page size. 
It also calculates the median price of the products.
 
 
Prerequisites
Ensure you have the following installed on your system
Python 3.7+
BeautifulSoup4 for HTML parsing
 
 
Functions
1) extract_products_from_html_zip(zip_file_path)
	Accepts the path to a ZIP file.Extracts all HTML files and processes them in parallel using ThreadPoolExecutor.
	
2) process_file(file_path)
	Accepts a single HTML file path.Parses the HTML and fetches the mentioned details.
	
3) calculate_median(products)
	Accepts the list of extracted products.Extracts numeric prices and computes the median price.
 