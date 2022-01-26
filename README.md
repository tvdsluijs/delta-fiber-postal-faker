<p align="center">

  <h2 align="center">Delta fiber postal faker</h2>

  <p align="center">
    A script to see which addresses in my village can get Fiber Optic, and immediately try to get delta to install Fiber in my Village!
    <br />
    <br />
    <a href="https://github.com/tvdsluijs/delta-fiber-postal-faker/issues">Report Bug</a>
    ·
    <a href="https://github.com/tvdsluijs/delta-fiber-postal-faker/issues">Request Feature</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)




<!-- ABOUT THE PROJECT -->
## About The Project

In my village in the Province of Zeeland there is no Fiber optic internet yet.

Our ISP "Delta" only provides internet by coax.

For faster PING's (my kids love fast pings) we need fiber optic internet.

At the site deltafibernederland.nl you can check if you address can have a fiber optic.

At my address it is currently not possible.

With this project I want to achieve two things:

1. see if fiber internet is available somewhere in the village.
2. hoping that delta saves every postcode check via their site and that they get the impression that the whole village wants fiber optic.


### Built With

* [Python 3](https://www.python.org/downloads/)
* [tqdm](https://github.com/tqdm/tqdm)
* [Postcode.tech](https://postcode.tech)
* [Postcode bij adres](https://postcodebijadres.nl/)


<!-- GETTING STARTED -->
## Getting Started

```sh
git clone git@github.com:tvdsluijs/delta-fiber-postal-faker.git
cd delta-fiber-postal-faker
python -m venv .venv
```

Start your venv!

```
pip install -r requirements.txt
```


### Prerequisites

If you cannot use the requirements.txt you will need to install the following packages with pip

```sh
pip install requests
pip install tqdm
```

There's some manual stuff you need to do before you can use this script!

The most important thing is that you fill in the postcodes.csv
For my village I got the data from here
https://postcodebijadres.nl/4443

Just remove the street names and split everything with a ;
So that you get the following lines.

`4443AA;1;39`

**postal code;start house number;end house number**

You also need a token from  [Postcode.tech](https://postcode.tech)

You place the token in a config.ini (example: config_sample.ini)
it says something like:
```
[postcode_api]
# token: 49102cb3-07ce-4e42-a0b2-742663393a54 (this is a fake token)
```

Done!

<!-- USAGE EXAMPLES -->
## Usage

Run the script with

`python deltafiber.py`

Keep the terminal window open, it checks every postalcode with some time slack in it so you do not overrun the delta / postcode server.


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

See `LICENSE` file for more information.



<!-- CONTACT -->
## Contact

Theo van der Sluijs - [itheo.tech](https://itheo.tech) - theo@vandersluijs.nl - [@itheo_tech](https://twitter.com/itheo_tech)

Project Link: [https://github.com/tvdsluijs/delta-fiber-postal-faker](https://github.com/tvdsluijs/delta-fiber-postal-faker)
