import requests
import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
#from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from selenium import webdriver
	
	# Step 2.1: Data Collection
	# --------------------------
	
	# A. Manual Collection (Example dataset)
manual_data = [
	    {
	        "description": "write a BASIC program using execute statement",
	        "example": """
	    execute "who" capturing xx
            crt xx
	"""
    }
]

examples = []
async def getUrlContent(url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            max_retries = 3
            retry_delay = 3  # seconds
            page_content = []
            for attempt in range(max_retries):
                try:
                    #print(f"Attempt {attempt + 1} to load the page...")
                    await page.goto(url, timeout=60000) #60s
                    frame = page.frame(name='contentwin') 

                    await frame.wait_for_load_state('networkidle')
                    await frame.wait_for_selector("div.body.refbody")
                    #await frame.wait_for_selector("div.body.refbody h2.title.sectiontitle:has-text('Description')")
                    #await frame.wait_for_selector("div.body.refbody h2.title.sectiontitle:has-text('Example(s)')")
                    #description_selector = "div.body.refbody h2.title.sectiontitle:has-text('Description')"
                    #examples_selector = "div.body.refbody h2.title.sectiontitle:has-text('Example(s)')"

                    #async def extract_section_content(section_selector):
                    #    section_element = await page.query_selector(section_selector)
                    #    content = ""
                    #    if section_element:
                    #        siblings = await section_element.evaluate_handle('el => el.nextElementSibling')
                    #        while siblings:
                    #            sibling_tag = await siblings.evaluate('el => el.tagName')
                    #            if sibling_tag == 'H2':  # Stop if next sibling is an H2
                    #                break
                    #            sibling_text = await siblings.evaluate('el => el.outerHTML')
                    #            content += sibling_text.strip() + "\n"
                    #            siblings = await siblings.evaluate_handle('el => el.nextElementSibling')
                    #            if await siblings.evaluate('el => el === null'):
                    #                break
                    #    return content

                    #description_content = await extract_section_content(description_selector)
                    #examples_content = await extract_section_content(examples_selector)

                    #combined_content = f"<div class='description-section'>{description_content}</div>" \
                                       #f"<div class='examples-section'>{examples_content}</div>"

                    #print("combined_content is: ",combined_content)
                    #print("manually combined content is: ",description_content + examples_content)
                    page_content = await frame.content()
                    break
                except TimeoutError:
                    if attempt < max_retries - 1:
                        #print(f"Timeout occurred on attempt {attempt + 1}. Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                    else:
                        #print("Max retries reached. Exiting.")
                        #raise  # Re-raise the last exception if all retries fail
                        break
                except Exception as e:
                    #print(f"An error occurred: {e}")
                    if attempt < max_retries - 1:  # If not the last attempt, wait before retrying
                        await asyncio.sleep(retry_delay)
                    else:
                        #print("Max retries reached. Exiting.")
                        #raise  # Re-raise the last exception if all retries fail
                        break
            if page_content:
                soup = BeautifulSoup(page_content, "html.parser")

                h1_name = soup.find('h1')
                if h1_name:
                    name_content = h1_name.get_text()
                    print("Name content from <h1>:")
                    print(name_content)
                else:
                    name_content=""
                    print("\n")
                
                h2_syntax = soup.find('h2', string='Syntax')
                if h2_syntax:
                    parent_div = h2_syntax.find_parent('div')
                    syntax_content = [h2_syntax.get_text()]
                    for pre in parent_div.find_all('pre'):
                        syntax_content.append(pre.get_text())
                    print("Syntax content starting from <h2>:")
                    for content in syntax_content:
                        print(content)
                else:
                    syntax_content=""
                    print("\n")

                #verfity there is content between h1 name and h2 syntax or not, if yes, append to description part
                between_name_synatx = []
                if name_content and syntax_content:
                    main_body = soup.find('div', class_='body refbody')
                    shortdesc = main_body.find('p', class_='shortdesc')
                    if shortdesc:
                        between_name_synatx.append(shortdesc.get_text())
                    for div in main_body.find_all('div', recursive=False):
                        h2 = div.find('h2')
                        if h2 and h2.get_text(strip=True) == 'Syntax':
                            break
                        p_tags = div.find_all('p')
                        for p in p_tags:
                            between_name_synatx.append(p.get_text())
                    print("Between name and synatx:")
                    for content in between_name_synatx:
                        print(content)
                else:
                    between_name_synatx=""
                    print("\n")

                #h2_description = soup.select_one("h2.title.sectiontitle:-soup-contains('Description')")
                description_content=[]
                h2_description = soup.find('h2', string='Description')
                if h2_description:
                    parent_div = h2_description.find_parent('div')
                    description_content = [h2_description.get_text()]
                    description_content.extend(between_name_synatx)
                    for p in parent_div.find_all('p'):
                        description_content.append(p.get_text())

                    print("Description content starting from <h2>:")
                    for content in description_content:
                        print(content)
                else:
                    #print('<h2> tag with "Description" not found')
                    #description_content=""
                    description_content=between_name_synatx
                    print("\n")

                parameters_content=[]
                h2_parameter = soup.find('h2', string='Parameter(s)')
                if h2_parameter:
                    parent_div = h2_parameter.find_parent('div')
                    #parameters_content = [h2_parameter.get_text()]
                    # 遍历 parent_div 的所有直接子元素，按顺序提取内容
                    for element in parent_div.find_all(recursive=False):  # 只遍历直接子元素
                        text_content = element.get_text(strip=True)  # 去掉首尾空白
                        if text_content:  # 如果内容非空，直接追加
                            parameters_content.append(text_content)
                else:
                    parameters_content=""
                    print("\n")

                example_content = []
                h2_example = soup.find('h2', string='Example(s)')
                if h2_example:
                    parent_div = h2_example.find_parent('div')
                    #example_content = [h2_example.get_text()]
                    #for p in parent_div.find_all('pre'):
                    #    example_content.append(p.get_text())
                    # 遍历父级 <div> 中的直接子元素
                    for element in parent_div.find_all(recursive=False): 
                         text_content= element.get_text(strip=True)
                         if text_content:
                             example_content.append(text_content)

                    print("Example content starting from <h2>:")
                    for content in example_content:
                        print(content)
                    print("Both have description and example based on url: ",url)
                    #examples.append({"description": description_content, "example": example_content})
                else:
                    #print('<h2> tag with "Example(s)" not found')
                    example_content=""
                    print("\n")
                
                examples.append({"name":name_content, "Syntax":syntax_content, "description": description_content, "parameter":parameters_content, "example": example_content})
            else:
                print("Unsuccessfully to get the content from :",url)

            await browser.close()
        #return collected_content
        
	# B. Automated Collection (Example using web scraping)



async def scrape_BASIC_tutorials():
    #options = webdriver.ChromeOptions()
    #options.binary_location = '/usr/local/bin'
    #driver = webdriver.Chrome(options=options)
    URL = "https://www3.rocketsoftware.com/rocketd3/support/documentation/d3nt/103/refman/index.htm"
    prefix = "https://www3.rocketsoftware.com/rocketd3/support/documentation/d3nt/103/refman/"
    urls_path = "/home/dli/BASIC-code-generator/urls.txt"
    #driver.get(URL)
    #driver.implicitly_wait(10)
    #html = driver.page_source
    #page = requests.get(URL)
    #session = HTMLSession()
    #response = session.get(URL)
    #response.html.render(sleep=5, scrolldown=20)
    #html_content = response.html.html
    async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(URL)
            frame = page.frame(name='toc')
            await frame.wait_for_load_state('networkidle')

            main_page_content = await frame.content()
            soup = BeautifulSoup(main_page_content, "html.parser")
            subpage_urls = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                href = prefix + href
                subpage_urls.append(href)
            for url in subpage_urls:
                print("Found subpage URL:", url)
                #with open(urls_path, "a") as file:
                #    file.write(url+'\n')
                #    file.close()
                await getUrlContent(url)
            await browser.close()
    return examples

        	# Collect data from D3 reference maunal (or similar site)
scraped_data = asyncio.run(scrape_BASIC_tutorials())

        	# Combine manual and scraped data
#combined_data = manual_data + scraped_data
        	# Step 2.2: Data Labeling and Conversion to DataFrame
	# ---------------------------------------------------

	# Convert combined data to a Pandas DataFrame
df = pd.DataFrame(scraped_data)

	# Display the first few rows of the DataFrame
print("Initial DataFrame:")
print(df.head())

	# Step 2.3: Data Preprocessing
	# ----------------------------

	# Text normalization
def normalize_list(list):
    list_lower = [item.lower() for item in list]
    list_strip_split = [item.strip().split() for item in list_lower]
    #text = text.lower()
    #text = text.strip()
    #text = ' '.join(text.split())
    return list_strip_split

	# Code cleaning
def clean_code(code):
    replace_list = [s.replace("\n"," ") for s in code]
    #else:
        #raise ValueError(f"Expected a list, but got {type(code)}")

    #cleaned_lines = []
    #for line in lines:
    #    cleaned_line = line.split('//')[0].strip()  # Remove comments
    #    if cleaned_line:
    #        cleaned_lines.append(cleaned_line)
    #return '\n'.join(cleaned_lines)
    return replace_list

def clean_code_tail(code):
    remove_list = [s.rstrip("\n") for s in code]
    #else:
        #raise ValueError(f"Expected a list, but got {type(code)}")
    return remove_list

	# Tokenization (optional)
def tokenize_code(code):
    tokens = re.findall(r'\w+|[^\w\s]', code, re.UNICODE)
    return tokens

	# Apply preprocessing to the DataFrame
#df['description'] = df['description'].apply(normalize_list)
df['description'] = df['description'].apply(clean_code)
df['example'] = df['example'].apply(clean_code_tail)
#df['tokens'] = df['example'].apply(tokenize_code)  # Optional: Use if tokenization is needed

	# Display the DataFrame after preprocessing
print("\nDataFrame after Preprocessing:")
print(df.head())

	# Save the preprocessed data to a CSV file
df.to_csv('preprocessed_BASIC_data.csv', index=False)

	# Convert the DataFrame to a JSON format and save
df.to_json('preprocessed_BASIC_data_.json', orient='records', indent=4)

	# Output some example data to verify
print("\nExample data from preprocessed DataFrame:")
print(df.head(3).to_string(index=False))



