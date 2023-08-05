<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://www.linkedin.com/company/kungfuai/">
    <img src="https://www.kungfu.ai/wp-content/uploads/2020/06/kungfu-lockup-variant-1.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">KUNGFU.AI Env</h3>

  <p align="center">
    Environment handling to simplify development environments
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Dependencies](#dependencies)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

### Built With
* [Python-Dotenv](https://flask.palletsprojects.com/en/1.1.x/)
* [Python 3.8](https://www.python.org/)



<!-- GETTING STARTED -->
## Getting Started

This repo aims to be a cloud and local compatible approach to modern application environment handling.

Environment files committed with the repo bring us some clear advantages that we should consider
when building software.

At KUNGFU.AI, many of our usecases are single container microservice deployment into a cloud. By committing secrets to
cloud Secret Manager, and keeping Secret IDs + other environment data within our env files, we're able to:

1. Keep our deployed assets secure
2. Developers don't have to pass keys, know about keys, or share env files (YUCK)
3. Developers can pull and run their repos immediately.

The kungfuai/env repo aims to simplify these use-cases.

### Dependencies
Python 3.8

### Installation

`pip install kungfuai-env`

### How does it work?

The flow is 3 steps - Construction, Registration, and Loading.
e.g.
```python
# Construction
env = Environment('src/env')
# Registration
env.register_environment("test")
env.register_environment("prod")
# Loading
env.load_env()
```

In the above example, `Environment()` is constructed, and the path to environment files is set to be located at
`src/env`.

Next, we state that we have a `test` environment, and a `prod` environment that we intend to load. 
The names are important - seeing `test` indicates that `env.load_env()` will seek a `.test.env` file in the `src/env` directory.
The same would be true for `prod` / `.prod.env`

### Runtime Environment Selection

Now, we know how to handle the environments. How do we know which ones to load when the application starts?

There is a special environment variable that we always watch named `ENV`.

With the above example in mind, if you set `ENV=PROD` or `ENV=prod`, you will load the `.prod.env` file.

If you set `ENV=TEST` or `ENV=test`, you will load the `.test.env` file.

If you do not set anything for `ENV`, you will load, by default, the `.local.env` file.


### Usage

#### Simple Example

In the most simple of applications, imagine a `main.py` with a `.local.env` environment 

```python
# main.py
import os
from kfai_env.env import Environment

if __name__ == "__main__":
    print("Simple Python App Example")

    e = Environment()
    e.register_environment("prod")
    e.load_env()
    print(os.getenv("TEST_ENV"))
```

```dotenv
# .local.env
TEST_ENV=HELLOWORLDFROMLOCAL
```

```dotenv
# .prod.env
TEST_ENV=HELLOWORLDFROMPROD
```

If we were to run `python3 main.py` with this above example program, we would see `HELLOWORLDFROMLOCAL`.
If we were to run `ENV=PROD python3 main.py`, we would see `HELLOWORLDFROMPROD`.


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/kungfuai/env/issues) for a list of proposed features (and known issues).

1. Upgrade project to use poetry as the build and deploy system (instead of pip + versioneer)

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Endurance Idehen - endurance.idehen@kungfu.ai


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/kungfuai/env/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/kungfuai/
[product-screenshot]: images/screenshot.png
