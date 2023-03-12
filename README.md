# Glorious Blog
![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
Small project of a web blog.
Backend made with flask
Frontend made with vue.js
## Installation
Clone this repository in your personal directory with the command:

```bash
git clone https://github.com/RubenChet/Esaip-Groupe-Violet.git
```
>  **Important**
Requires [Node.js] and [Python]

### You can create a new virtual environment

On Linux or MacOS

```bash
python3 -m venv .venv --upgrade-deps
source .venv/bin/activate
```

On Windows

```shell
python -m venv .venv --upgrade-deps
.venv\Scripts\activate.bat
```

*For more information about virtual environments see the [official documentation](https://docs.python.org/3/library/venv.html).*

### Install needed packages

Install needed packages with:

```bash
pip install -r requirements.txt
```

```bash
cd vue
npm install
```

### Initialize project

Run this command once to initialize the project:

```bash
flask --app flask/app.py init-db
```

## Running the program

Execute one of the following command to start the program:

```bash
python flask/app.py
```

```bash
cd vue
npm run dev
```