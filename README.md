# Investopedia-Bot
![Investopedia-2017](https://user-images.githubusercontent.com/40627412/136075564-c1179715-164c-4e87-b81c-154adf20fb41.png)

Investopedia-Bot is a beginner-friendly GUI Python program that automates stock trading. The program calculates stock expectancies (measures which stocks are less risky and are expected to make more money), displays stock data and graphs, and recommends the number of shares to buy based on various user-defined variables. Once the user chooses stocks, the program can execute trades automatically.

## Technologies/Libraries Used
Selenium: used to scrape Finviz for stock charts and automate trades in the Investopedia stock simulator.
Pillow: used for Fiviz image manipulation.
yahoo_fin: get up-to-date stock price.

## Setup
To get started with Investopedia-Bot, follow these steps:
  1. Clone the repository: git clone git@github.com:bassel27/Investopedia-Bot.git
  2. Change the working directory to the cloned repository: cd Investopedia-Bot
  3. Install the required libraries: pip install -r requirements.txt
  4. Update your Investopedia login credentials in the config.py file
  5. Start the program by running python main.py

## How to Use Investopedia Trading?
### First Stage
When the program is launched, it prompts the user to enter the **risk percentage**, which is the maximum amount of cash they are willing to lose on a single trade. The default risk percentage is 2%, but users can enter their own value. The program also asks about the chance of winning for each stock. By default, it is set to 0.9 for all stocks, but users can enter their own value. Below these inputs, the program displays the account value and cash, which are scraped from the user's Investopedia profile.

![image](https://user-images.githubusercontent.com/40627412/136844357-76fa68f2-5ea8-4626-b633-ba1c21baef12.png)
### Seocnd Stage
Once the user enters the risk and chance of winning, they are prompted to enter details for each stock they are interested in trading. This includes the ticker symbol, the target price, and the stop-loss price. Users can add as many stocks as they like by clicking "Onto the next stock" or click "finish" if they are done.

![image](https://user-images.githubusercontent.com/40627412/136844395-f4694ab3-1a72-474d-9629-348207852646.png)
### Third Stage
After the user enters the stocks they are interested in, the program displays the results and ranks the stocks based on expectancy. The user can choose to place a market order or a limit order and specify the limit price (which is `current price ± 0.02` by default). The program calculates the number of shares to buy or short based on the following rule: `position size (number of shares) = Max loss per trade / amount you can lose per share, or position size (number of shares) = quantity = account value * (risk percentage / 100) / (|current price - stop loss price|)`.

![image](https://user-images.githubusercontent.com/40627412/136072260-660f6a72-d608-48ef-b480-ac4e3728974b.png)

## Limitations and Future Work
One limitation of the Investopedia-Bot is that it was designed to work with a specific version of the Investopedia stock simulator UI. Since the program's development, Investopedia has updated its UI, which has caused some of the scraping code to break. However, this presents an opportunity for contributors to update the program to work with the latest version of the UI. If you're interested in contributing to the project, updating the scraping code to match the new UI would be a valuable contribution that would help ensure the program continues to function as intended.
