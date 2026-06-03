# Bank CLI Application

#### Video Demo:  <https://youtu.be/_spu07Sata4>

#### Description:

This project is a command-line banking application written in Python that allows a user to perform basic financial operations such as depositing money, withdrawing funds, and checking their account balance. The purpose of this project is to demonstrate core programming concepts including function design, control flow, error handling, and testing using pytest.

The application is designed to simulate a simplified banking experience through a text-based interface. When the program is run, the user is presented with a menu of options including deposit, withdraw, check balance, and quit. Based on the user’s input, the program executes the corresponding action and updates the account balance accordingly. The program continues running in a loop until the user chooses to exit.

The main file of this project is project.py. This file contains the main() function, which serves as the entry point of the application and handles all user interaction. It continuously prompts the user for input and routes actions to the appropriate helper functions. In addition to main(), the file includes three core functions: deposit, withdraw, and check_balance. These functions are responsible for the core banking logic. The deposit function adds a specified amount to the balance, while ensuring that negative values are not accepted. The withdraw function subtracts an amount from the balance, with safeguards in place to prevent overdrafts and invalid inputs. The check_balance function simply returns the current balance.

A key design decision in this project was to separate user interaction (input and print statements) from the business logic. This means that functions like deposit and withdraw do not directly interact with the user, but instead take parameters and return values. This approach makes the code more modular, easier to understand, and significantly easier to test. It also follows best practices commonly used in larger software systems.

The testing file, test_project.py, contains unit tests written using pytest. These tests verify that the core functions behave as expected under various conditions, including normal operations and edge cases such as negative inputs and overdraft attempts. By separating the logic from user input, these functions can be tested automatically without requiring manual interaction.

Another important design consideration was error handling. The program uses exceptions to handle invalid inputs such as negative deposit or withdrawal amounts. This ensures that the program remains stable and provides meaningful feedback to the user rather than crashing.
