import zipfile
import os
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import shutil
 
 
def process_file(file_path):
    try:
        # Open the file with encoding error handling
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            html_content = f.read()
 
        # Parse the HTML content with lxml parser
        soup = BeautifulSoup(html_content, 'lxml')
 
        # Extract product name
        product_name = soup.find('h1', itemprop='name')
        name = product_name.text.strip() if product_name else "N/A"
 
        # Extract price
        price_div = soup.find('div', id='PDP_productPrice')
        if price_div:
            raw_price = price_div.text.strip()
            currency =  raw_price[0]  # Extract currency symbol
            price = raw_price[1:].strip()  # Extract numeric value
        else:
            currency, price = "N/A", "N/A"
 
        # Extract short description
        description_p = soup.find('p', itemprop='description')
        short_description = (
            " ".join(description_p.stripped_strings) if description_p else "N/A"
        )
 
        # Extract rating
        rating_div = soup.find('div', itemprop='ratingValue')
        rating = rating_div.text.strip() if rating_div else "N/A"
 
        # Calculate page size
        page_size = len(html_content)/1024
 
        # Return product details
        if name != "N/A" and price != "N/A":
            return {
                "name": name,
                "Price": price,
                "currency": currency,
                "short_description": short_description,
                "rating": rating,
                "Page_Size": page_size,
            }
 
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None
 
 
def extract_products_from_html_zip(zip_file_path):
    products = []
 
    # Extract ZIP file
    extract_dir = "extracted_html_files"
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
 
    # Collect all HTML files
    html_files = []
    for root, _, files in os.walk(extract_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
 
    # Process files in parallel
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_file, html_files)
        for result in results:
            if result:
                products.append(result)
 
    # Clean up extracted files
    shutil.rmtree(extract_dir)
 
    return products

def calculate_median(products):
    # Extract prices for calculation
    prices = [float(product["Price"]) for product in products if float(product["Price"]) > 0]
    if not prices:
        return 0.0
    highest_price = max(prices)
    lowest_price = min(prices)
    return (highest_price + lowest_price) / 2

 
 
if __name__ == "__main__":
    # Path to your ZIP file
    # zip_file_path = r'C:\Users\kqvd665\OneDrive - AZCollaboration\Desktop\DE_Task\Sleep Aid Clone.zip'
    zip_file_path = './Sleep Aid Clone.zip'
    print("Processing ZIP file...")
 
    # Extract products
    products = extract_products_from_html_zip(zip_file_path)
 
    median_price = calculate_median(products)

    # Prepare the final output structure
    output = {
        "Products": products,
        "Median": round(median_price, 2)
    }
 
    # Convert to JSON format and print
    output_json = json.dumps(output, indent=4, ensure_ascii=False)
    print(output_json)

