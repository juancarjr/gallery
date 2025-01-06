from bs4 import BeautifulSoup
import string
import requests
import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from textblob import Word

# Uncomment these lines to download necessary NLTK data files
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')


def get_projects(url, output_file=False) -> BeautifulSoup:
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
    print("DONE GETTING PROJECTS")
    return soup

def parse_projects(data) -> list:
    """
    Parse the projects from the given BeautifulSoup object or file and extract the relevant information.
    """
    projects = []

    # Check if data is a BeautifulSoup object
    if isinstance(data, BeautifulSoup):
        soup = data
    else:
        # Assume data is a file path
        with open(data, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

    for project in soup.find_all(class_='project'):
        title_tag = project.find('a', class_='font-weight-bold')
        title = title_tag.text.strip()
        author = title_tag.parent.text.split("by")[1].strip()
        description = project.find_all('p')[1].text.strip()
        video = project.find('a')['href'] 
        thumbnail = project.find('img')['data-src']
        projects.append({'title': title,
                        'author': author,
                        'description': description, 
                        'video': video,
                        'thumbnail': thumbnail
                        })
    return projects

def generate_tags(projects: list) -> list:
    """
    Generate tags for each project based on the description
    """
    # Set of stop words to filter out common words
    stop_words = set(stopwords.words('english'))
    # Common unwanted words found in project descriptions
    unwanted_words = ['project', 'projects', 'cs50', 'harvard', 'cs50x', 'final']
    stop_words.update(unwanted_words)
    stop_words.update(string.punctuation)
    # Unwanted tags to filter out
    unwanted_tags = {'NNP': True, 
                     'VBZ': True, 
                     'VBP': True, 
                     'VBG': True, 
                     'VBD': True, 
                     'VBN': True, 
                     'RB': True, 
                     'RBR': True, 
                     'RBS': True, 
                     'JJ': True, 
                     'JJR': True, 
                     'JJS': True, 
                     'POS': True, 
                     'PRP': True, 
                     'PRP$': True, 
                     'WP': True, 
                     'WP$': True, 
                     'WRB': True, 
                     'WDT': True, 
                     'TO': True, 
                     'DT': True, 
                     'CC': True, 
                     'IN': True, 
                     'EX': True, 
                     'MD': True, 
                     'RP': True, 
                     'UH': True, 
                     'LS': True, 
                     'PDT': True, 
                     'SYM': True, 
                     'NFP': True,
                     'CD': True}
    
    for project in projects:
        description = project['description']
        # Tokenize the description into words
        word_tokens = word_tokenize(description)
        # Tag each word with its part of speech
        tags = nltk.pos_tag(word_tokens)
        # Filter out unwanted words and punctuation
        filtered_text = []
        for w, t in tags:
            if w.lower() in stop_words or t in unwanted_tags:
                continue
            # Singularize the word if it is a plural noun
            if t.endswith('S'):
                w = Word(w).singularize()
        # Append the word to the filtered text
            filtered_text.append(w.lower())
        # Assign the filtered words as tags to the project
        project['tags'] = set(filtered_text)
    
    return projects
