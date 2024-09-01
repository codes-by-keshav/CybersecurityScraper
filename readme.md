# Twitter Scraping with Selenium

This repository contains Python scripts for scraping posts from Twitter (now X) using Selenium WebDriver. These scripts allow automated login and post extraction based on specific search terms and Twitter accounts.

## Features

- **Automated Login**: Logs into Twitter using credentials stored in environment variables.
- **Post Scraping**: Extracts post links and their timestamps from specific Twitter accounts.
- **Two Modes**:
  - `twitter_scrap.py`: Prompts the user to input search terms and the target Twitter account.
  - `scraper.py`: Scrapes Twitter for pre-defined search terms and a preset account (Cybercell India).

## Requirements

- Python 3.x
- Selenium
- Edge WebDriver
- Edge Browser
- `.env` file for storing Twitter credentials (username and password)

### Required Python Libraries
These are listed in `requirements.txt` and can be installed with the following command:

```bash
pip install -r requirements.txt
```
## Setup & Installation
1. Clone the repository:
```bash
git clone https://github.com/codes-by-keshav/CybersecurityScraper.git
```
2. Install the required Python libraries:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file in the project directory and add your Twitter credentials (username and password) in the following format specified in `.sample.env` file.

## Usage
### 2 Approaches:
#### 1. Using `twitter_scrap.py`:
1. This script allows the user to input search terms and a target Twitter account manually.
2. Run using 
```bash
python twitter_scrap.py
```
3. Go back to terminal and add the search terms and the target Twitter account.
4. Matching posts' links and timestamps will be printed in the terminal.
#### 2. Using `scraper.py`:
1. This script scrapes Twitter for pre-defined search terms and a preset account (Cybercell India).
2. Run using
```bash
python scraper.py
```
3. Matching posts' links and timestamps will be printed in the terminal.

## Disclaimer
This project is for educational purposes only. Use it responsibly and in compliance with Twitter's terms of service.



