# WoodStocks_Counter
This repository contains the files for the application "StockCounter" for Wood Stocks company.
The application reads the file "stocklist.csv" and displays each item one at a time on the screen. The user is then asked to input the new stock count of each item and will only stop after all the items were displayed. Then the user is asked whether to send the file to a receiving computer or edit the file again. If the user chooses to edit the file again, then the same procedure mentioned above is made. Else, the updated file is sent to another computer. If sending is successful, the Green LED will turn ON for 5 seconds. If sending fails, the Red LED instead will turn ON for 5 seconds. Then the application ends.

To run the application:
1. Get the stocklist.csv provided by Wood Stocks. 
2. Save the csv file to where StockCounter.py and the rest of the file is located in the Raspberry Pi.
3. From the Raspberry Pi terminal, type "sudo python StockCounter.py"
4. On another computer, copy TCPSocket.py and uncomment some lines to receive the csv file. (Lines 16, 85, 87-89.)
5. From the terminal, type "python.exe TCPSocket.py". The program will keep on running unless a file is received from the Raspberry Pi.
6. Back to the Raspberry Pi, the user can start to input new stock count and the application will end after the updated stocklist.csv is sent to the receiving computer.
