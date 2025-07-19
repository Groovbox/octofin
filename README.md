<h1 align="center">Octofin</h1>

---

![Octofin Banner](docs/img/Banner.png)

Octofin provides a set of tools, scripts, and an extensive plugin ecosystem to build on top of Jellyfin, essentially giving it more features and making it *smarter*, with more capabilities and flexibility.  
It uses a Django backend and provides a beautiful front-end interface for users to manage their Jellyfin installations and content with ease.

Octofin is the culmination of many small tools and scripts I've created over years of using Jellyfin, now polished and unified into a cohesive ecosystem. It may also support third-party extensions in the future.

---

## Octofin Server

This repository contains the code for Octofin’s backend server. The backend is built with Django because I'm more familiar with it as well as the fact that it comes with many built-in features that reduce the need for custom implementations.

For the database, it uses SQLite, the default database for Django since it's perfectly suited for handling configurations and lightweight data without the overhead of a full-fledged DBMS.

---

### Development

Octofin requires a few prerequisites to enable full content-management functionality. While you can skip them for basic usage, some tools depend on them:

- [FFmpeg]() – required for any media-processing features.

For managing Python dependencies, the project uses [Poetry](https://python-poetry.org/) as the dependency manager.  
To get started:

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone https://github.com/yourusername/octofin.git
cd octofin

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

Then, to run the Django development server on port `3936`:

```shell
python manage.py runserver 0.0.0.0:3936
```

> [!NOTE]\
> If port 3936 is already in use, feel free to change it.\
> However, be sure to reflect the same port change in the front-end webserver configuration.


### Octofin Web Client

The Octofin web client is a React-based front-end that interacts with this Django backend.  
It provides a smooth and modern user experience for managing content, running tools, and visualizing data.

You can find the web client repository here:  
 [https://github.com/groovbox/octofin-web](https://github.com/groovbox/octofin-web)

