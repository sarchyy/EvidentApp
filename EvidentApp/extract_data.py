from bs4 import BeautifulSoup

def extract_data_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table') 
    
    if table is None:
        raise ValueError("No table found in HTML content.")
    
    rows = table.find_all('tr')
    data = []
    
  
    headers = [header.get_text(strip=True) for header in rows[0].find_all('th')] if rows[0].find_all('th') else []
    data.append(headers) 
    
 
    for row in rows[1:]:
        cells = row.find_all('td')
        data.append([cell.get_text(strip=True) for cell in cells])
    
    return data
