# Gallery Project
#### Video Demo:  <URL HERE>

This is a Django-based web application for managing and displaying CS50's gallery of final projects. Each project can have multiple tags associated with it, and the tags are used to categorize and filter the projects.
## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)


## Features

- Display a list of projects with thumbnails and titles.
- Filter projects by tags.
- View detailed information about each project, including a description, author, and video.
- Increment the count of tags each time they are used.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/gallery.git
    cd gallery
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On Unix or MacOS
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser to access the admin interface:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Open your browser and go to `http://127.0.0.1:8000` to see the application.

## Usage

- To add new projects, you can use the Django admin interface at `http://127.0.0.1:8000/admin`.
- Projects can be filtered by tags using the search functionality on the main page.
- Each project detail page displays the project's description, author, video, and associated tags.

## Project Structure

- `gallery/`: The main Django project directory.
- [webpage/](http://_vscodecontentref_/0): The Django app containing the models, views, templates, and management commands.
- `templates/`: The directory containing HTML templates for the project.
- `static/`: The directory containing static files (CSS, JavaScript, images).

## Models

- [Tag](http://_vscodecontentref_/1): Represents a tag that can be associated with projects.
- [Project](http://_vscodecontentref_/2): Represents a project with a title, author, description, video, and thumbnail.
- [ProjectTag](http://_vscodecontentref_/3): Represents the many-to-many relationship between projects and tags.
- [Favorite](http://_vscodecontentref_/4): Represents a user's favorite projects.

## Project Parser
- Extracts the project data based on the models fields.
- Generates tags based on the project's description utilizing the nltk library. Could use some more work, some NNPs like Harry Potter are filtered out even though it would be a good tag to have.


## Management Commands

- `load_projects`: A custom management command to load projects from a file and populate the database.
I've though about using the import_export module, but because of the way the data
is presented, I decided to try and write a command myself.

## TODO
- Improve user authentication and authorization templates.
- Improve tagging.
- Implement throttling in some other way.
- Add and remove projects.
- Add and remove tags.
- Light/dark mode? This particular theme doesn't change much.
- Refactor remove_from_favorites so that it reloads the content div
instead of removing the card html element, however, at that point I should also refactor the index.html, and the view, and the whole  project.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.
