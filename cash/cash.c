#include <cs50.h>
#include <stdio.h>

int change(void);
int calculate_quarters(int change);
int calculate_dimes(int change);
int calculate_nickels(int change);
int calculate_pennies(int change);
int num_coins(int change);

int main(void)
{
    // Prompt user for input
    int change;
    do
    {
        change = get_int("What is the change needed?");
    }
    while (change < 0);

    // Calulation of quarters
    int quarters = calculate_quarters(change);
    change = change - quarters * 25;

    // Calulation of dimes
    int dimes = calculate_dimes(change);
    change = change - dimes * 10;

    // Calulation of nickels
    int nickels = calculate_nickels(change);
    change = change - nickels * 5;

    // Calulation of pennies
    int pennies = calculate_pennies(change);
    change = change - pennies * 1;

    // Sum of coins
    int num_coins = quarters + dimes + nickels + pennies;
    num_coins = quarters + dimes + nickels + pennies;

    // Print total number of coins given to customer
    printf("%i\n", num_coins);
}

int calculate_quarters(int change)
{
    int quarters = 0;
    while (change >= 25)
    {
        change = change - 25;
        quarters++;
    }
    return quarters;
}

int calculate_dimes(int change)
{
    int dimes = 0;
    while (change >= 10)
    {
        change = change - 10;
        dimes++;
    }
    return dimes;
}

int calculate_nickels(int change)
{
    int nickels = 0;
    while (change >= 5)
    {
        change = change - 5;
        nickels++;
    }
    return nickels;
}

int calculate_pennies(int change)
{
    int pennies = 0;
    while (change >= 1)
    {
        change = change - 1;
        pennies++;
    }
    return pennies;
}
