from selenium import webdriver
from selenium.webdriver.common.by import By

# Create driver to scrape character wiki webpage
driver = webdriver.Chrome()
driver.get("https://en.wikipedia.org/wiki/List_of_The_Wheel_of_Time_characters")
driver.implicitly_wait(1)

# Get text (names) from the character elements
elems = driver.find_elements(By.CLASS_NAME, "mw-headline")

# Cut off non-character headers
for i in range(len(elems)):
    if elems[i].text == "Other":
        elems = elems[1:i]
        break

# Convert elements from WebObject to strings
# Then, remove text without ": " or that don't start with a letter to get rid of references
elems = [e.text for e in elems]
elems += [e.text[:e.text.index(":")] for e in driver.find_elements(By.TAG_NAME, "li") if ": " in e.text and e.text[0].isalpha()]

# Write scraped names to file, separated by new line
with open("names.txt", "w", encoding = "utf-8") as f:
    f.writelines(e + "\n" for e in elems)
driver.quit()