# THU Grade Scraper

This Python script scrapes overall grades from the THU (East Sea) student information system.

## Introduction

THU Grade Scraper is a Python script designed to automate the retrieval of overall grades from the THU (East Sea) student information system. It uses Selenium for web automation and BeautifulSoup for HTML parsing.

## Requirements

- Python 3
- Selenium
- BeautifulSoup

## Installation

1. **Clone the repository:**
git clone https://github.com/Caspar15/THU-grade-scraper.git
cd THU-grade-scraper


2. **Install dependencies:**
pip install selenium beautifulsoup4


## Usage

1. **Configuration:**
- Open `scraper.py` and modify the following variables with your THU-NID credentials:
  ```python
  username = "your_THU_NID_here"
  password = "your_password_here"
  ```

2. **Run the Scraper:**
- Execute the scraper:
  ```
  python scraper.py
  ```
- The script will open a browser window and prompt you to complete the manual verification and login process.

3. **Output:**
- After successful login, the script will parse your grades and calculate the semester GPA.
- It will print individual course details and the overall semester GPA.

## Example Output
大一英文: GPA=4.0 * 學分=2.0 = 8.0
中文：文學欣賞與實用: GPA=3.7 * 學分=2.0 = 7.4
...
總成績點數: 60.6
總學分數: 18.0
學期總平均 GPA: 3.3666666667


## Contributing

Contributions are welcome! Fork the repository, make improvements, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- Caspar15
