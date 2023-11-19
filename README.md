
<h1 align="center">UniMart by EvoQ<br>Your Personal Shopping Companion</h1>

<h4 align="center">E-Commerce API MVP</h4>

<p align="center">
  <a href="https://github.com/tigran-saatchyan/UniMart_by_EvoQ/blob/master/LICENSE"><img src="https://img.shields.io/github/license/tigran-saatchyan/UniMart_by_EvoQ" alt="License"></a>
  <a href="https://t.me/PythonistiC"><img src="https://img.shields.io/badge/telegram-@PythonistiC-blue.svg?logo=telegram" alt="Telegram"></a>
  <a href="https://www.paypal.me/TigranSaatchyan"><img src="https://img.shields.io/badge/support-paypal-blue.svg?logo=paypal" alt="Support me on Paypal"></a>
  <a href="https://github.com/tigran-saatchyan/UniMart_by_EvoQ"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit" alt="Support me on Paypal"></a>
</p>


## Table of Contents

* [Background / Overview](#background--overview)
* [Features](#features)
* [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Structure / Scaffolding](#structure--scaffolding)
* [Documentation](#documentation)
* [Browser Support](#browser-support)
* [Dependencies](#dependencies)
* [Release History](#release-history)
* [Changelog](#changelog)
* [Issues](#issues)
* [Bugs](#bugs)
* [Translations](#translations)
* [Authors](#authors)
* [Acknowledgments](#acknowledgments)
* [Support](#support)
* [License](#license)

## Background / Overview
**UniMart by EvoQ API** is a tool that allows
developers to integrate e-commerce features
like product management, inventory control,
order processing, and customer data management
into their applications or websites, making it
easier to run online stores.

## Features
#### **Effortless Registration, Exclusive Access**

- **Swift Onboarding:**
  - Join UniMart with a breeze using your Full Name, Email, and Phone – setting up your account in moments.

- **Exclusive Shopping Experience:**
  - Gain access to a world of curated products tailor-made for our authorized users.

#### **Smart Shopping with UniMart Basket**

- **Intelligent Cart Management:**
  - UniMart Basket, your intelligent shopping companion, adapts to your preferences seamlessly.

- **Quick Checkout:**
  - Add, remove, or clear items with a single click – making your shopping journey smooth and enjoyable.

#### **Real-Time Product Discovery**

- **Diverse Product Range:**
  - Explore a diverse range of products that cater to your unique tastes and needs.

- **Stay Informed:**
  - Receive real-time updates on product additions and updates, ensuring you never miss out.

#### **Secure and User-Friendly Authentication**

- **Effortless Login:**
  - Swiftly access UniMart using your Email or Phone, accompanied by a secure password.

- **Authenticated Perks:**
  - Unlock a world of benefits with exclusive access to our curated product list.

#### **Technical Brilliance for a Seamless Experience**

- **Blazing-Fast Speed:**
  - UniMart leverages asynchronous processes, ensuring a swift and responsive shopping experience.

- **Secure Identity Handling:**
  - Your identity is protected with robust Bearer Tokens or JWT authentication.

#### **UniMart by EvoQ - Elevating Your Shopping Experience to New Heights!**
## Prerequisites

You will need the following installed on your computer.

* [Git](https://git-scm.com/)
* [Python Poetry](https://python-poetry.org/)
* [PostgreSQL](https://www.postgresql.org/)

### Installation

Let's go through the steps to run the project "UniMart_by_EvoQ".

1. **Clone the Repository:**
   ```bash
   git clone git@github.com:tigran-saatchyan/UniMart_by_EvoQ.git
   ```

2. **Navigate to Project Directory:**
   ```bash
   cd UniMart_by_EvoQ
   ```

3. **Install Poetry:**
   - If you haven't installed Poetry yet, please follow the instructions on the official website: https://python-poetry.org/docs/#installation
   - If you have Poetry installed, you can use the following command to activate Python 3.12 for the project:
        ```bash
        poetry env use python3.12
        ```

4. **Install Project Dependencies:**
   ```bash
   poetry install
   ```

5. **Activate Virtual Environment:**
   ```bash
   poetry shell
   ```

6. **Create Database:**
   - If you haven't installed PostgreSQL yet, please follow the instructions on the official website: https://www.postgresql.org/download/
   ```bash
    createdb --host=POSTGRES_HOST --port=POSTGRES_PORT --username=POSTGRES_USER POSTGRES_DB
    ```
   - **Note:** Don't forget to rename .env.sample and replace the values with your own.
   - **Note:** If you are using the default PostgreSQL settings, you can use the following command:
       ```bash
       createdb --host=localhost --port=5432 --username=postgres unimart_db
       ```

7. **Run Migrations:**
   ```bash
   alembic upgrade head
   ```

8. **Run the Project:**
    ```bash
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
    ```

9. **Testing:**
   - Create a test database:
     ```bash
     createdb --host=TEST_POSTGRES_HOST --port=TEST_POSTGRES_PORT --username=TEST_POSTGRES_USER TEST_POSTGRES_DB
     ```
     - **Note:** Don't forget to replace the values with your own and put them in the .env.test file.

   - You can run tests by using the following command:
     ```bash
     poetry run pytest
     ```
    - If you want to run the tests with coverage, you can use:
      ```bash
      poetry run pytest --cov=app tests/
      ```
    - If you want to run the tests with coverage and generate a report, you can use:
      ```bash
      poetry run pytest --cov=app tests/ --cov-report=html && open htmlcov/index.html
      ```
Please note that the success of these steps depends on the project's structure and requirements. If there are additional steps or specific configurations needed, consult the project's documentation or README.


### Structure / Scaffolding
```text
               =========                  Tigran Saatchyan ~ git version 2.34.1
            ===============               -------------------------------------
           =================              Project: UniMart_by_EvoQ (2 branches)
          ===  ==============
          ===================             Created: 5 days ago
                   ==========             Language:
   ========================== =======               ● Python (100.0 %)
 ============================ ========    Authors: 100% Tigran Saatchyan
============================= =========   URL: git@github.com:tigran-saatchyan/UniMart_by_EvoQ.git
============================ ==========
========== ============================
========= =============================   Lines of code: 1369
 ======== ============================    Size: 244.97 KiB (60 files)
  ======= ==========================      License: MIT
          ==========
          ===================
          ==============  ===
           =================
            ===============
               =========


```
<details>
<summary>Project Structure</summary>

```text
UniMart_by_EvoQ
app
├── __init__.py
├── api
│  ├── __init__.py
│  └── v1
│     ├── __init__.py
│     ├── auth.py
│     ├── cart.py
│     ├── dependencies.py
│     ├── products.py
│     └── routers.py
├── db
│  ├── __init__.py
│  └── db.py
├── main.py
├── migrations
│  ├── env.py
│  ├── README
│  ├── script.py.mako
│  └── versions
├── models
│  ├── __init__.py
│  ├── base_model.py
│  ├── cart.py
│  ├── products.py
│  └── users.py
├── repositories
│  ├── __init__.py
│  ├── cart.py
│  ├── products.py
│  ├── repository.py
│  └── users.py
├── schemas
│  ├── __init__.py
│  ├── cart.py
│  ├── products.py
│  └── users.py
├── services
│  ├── __init__.py
│  ├── cart.py
│  ├── managers.py
│  ├── products.py
│  └── validators.py
├── settings
│  ├── __init__.py
│  ├── auth.py
│  └── config.py
└── utils
   ├── __init__.py
   ├── factories.py
   ├── unitofwork.py
   └── utils.py


```

</details>


<strong>Note:</strong> The scaffolding was generated with tree.

## Documentation
- http://example.com:8000/
- http://example.com:8000/docs

## Dependencies

List of dependencies used in the project


| **Main Libraries**                                                                                                                                                                                                                                             | **Other Libraries**                                                                                                                                                                                                                                           |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Python Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftigran-saatchyan%2FUniMart_by_EvoQ%2Fdevelop%2Fpyproject.toml&query=%24.tool.poetry.dependencies.python&style=flat&logo=python&label=Python)           | ![Alembic](https://img.shields.io/badge/FastAPI--users-%5E2.8.2-blue?logo=FastAPI)                                                                                                                                                                            |
| ![FastAPI](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftigran-saatchyan%2FUniMart_by_EvoQ%2Fdevelop%2Fpyproject.toml&query=%24.tool.poetry.dependencies.fastapi.version&style=flat&logo=fastapi&label=FastAPI)     | ![asyncpg](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftigran-saatchyan%2FUniMart_by_EvoQ%2Fdevelop%2Fpyproject.toml&query=%24.tool.poetry.dependencies.asyncpg&logo=PostgreSQL&style=flat&label=asyncpg)         |
| ![SQLAlchemy](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftigran-saatchyan%2FUniMart_by_EvoQ%2Fdevelop%2Fpyproject.toml&query=%24.tool.poetry.dependencies.sqlalchemy&style=flat&logo=sqlalchemy&label=SQLAlchemy) | ![pytest](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftigran-saatchyan%2FUniMart_by_EvoQ%2Fdevelop%2Fpyproject.toml&query=%24.tool.poetry.group.develop.dependencies.pytest&logo=pytest&style=flat&label=pytest)  |
| ![Alembic](https://img.shields.io/badge/Alembic-%5E1.12.1-blue?logo=Alembic)                                                                                                                                                                                   | ![pytest](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftigran-saatchyan%2FUniMart_by_EvoQ%2Fdevelop%2Fpyproject.toml&query=%24.tool.poetry.group.develop.dependencies.ruff&logo=ruff&style=flat&label=ruff)        |
|                                                                                                                                                                                                                                                                | ![pytest](https://img.shields.io/badge/pre--commit-%5E3.5.0-blue?logo=pre-commit)                                                                                                                                                                             |
|                                                                                                                                                                                                                                                                | ![pytest](https://img.shields.io/badge/pytest--postgresql-%5E5.0.0-blue?logo=pytest)                                                                                                                                                                          |
|                                                                                                                                                                                                                                                                | ![pytest](https://img.shields.io/badge/pytest--asyncio-%5E0.21.1-blue?logo=pytest)                                                                                                                                                                            |
|                                                                                                                                                                                                                                                                | ![pytest](https://img.shields.io/badge/pytest--cov-%5E4.1.0-blue?logo=pytest)                                                                                                                                                                                 |


[//]: # (## Todo)


## Release History
Actual version: ![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftigran-saatchyan%2FUniMart_by_Evoq%2Fdevelop%2Fpyproject.toml&query=%24.tool.poetry.version&style=flat&label=Version)



## Changelog

Detailed changes for each release will be documented in the
[release notes](https://github.com/users/tigran-saatchyan/projects/11).

## Issues
<a href="https://github.com/tigran-saatchyan/UniMart_by_EvoQ/issues?q=is%3Aopen+is%3Aissue"><img src="https://img.shields.io/github/issues/tigran-saatchyan/UniMart_by_Evoq" alt="open"></a>
<a href="https://github.com/tigran-saatchyan/UniMart_by_EvoQ/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/tigran-saatchyan/UniMart_by_Evoq" alt="close"></a>

Please make sure to read the [Issue Reporting Checklist](https://github.com/tigran-saatchyan/UniMart_by_Evoq/issues?q=is%3Aopen) before opening an issue. Issues not conforming to the guidelines may be closed immediately.

## Bugs

If you have questions, feature requests or a bug you want to report, please click [here](https://github.com/tigran-saatchyan/UniMart_by_Evoq/issues) to file an issue.

[//]: # (## Deployment)

## Translations

* :ru: Russian/Русский

## Authors

* [**Tigran Saatchyan**](https://github.com/tigran-saatchyan) - UniMart by EvoQ

See also the list of [contributors](#acknowledgments) who participated in this project.

## Acknowledgments

This project would not have been possible without the help and advice of many contributors and the tremendous support of each of you.

## Contact Us:

  * Discord: ![Discord](https://img.shields.io/discord/1152575327810363482)

## Support

Like what you see? Keep me awake at night by buying me a coffee or two.

<a href="https://www.buymeacoffee.com/saatchyan" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Book" style="height: 60px !important;width: 217px !important;" ></a>

## License
Copyright (c) 2023 Tigran Saatchyan.

Usage is provided under the MIT License. See [LICENSE](https://github.com/tigran-saatchyan/UniMart_by_EvoQ/blob/master/LICENSE) for the full details.
