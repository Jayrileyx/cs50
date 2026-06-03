#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // One command-line argument to start program
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // Make argv[1] using digits
    for (int i = 0; argv[1][i] != '\0'; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Must contain only positive digits.\n");
            return 1;
        }
    }
    // Convert argv[1] from string to int
    int num = atoi(argv[1]);

    // Prompt user for plaintext
    string text = get_string("Plaintext: ");
    printf("Ciphertext: ");

    // For each character in plaintext
    for (int c = 0, length = strlen(text); c < length; c++)
    {
        // Rotate character if its a letter
        if (isupper(text[c]))
        {
            printf("%c", (text[c] - 65 + num) % 26 + 65);
        }
        else if (islower(text[c]))
        {
            printf("%c", (text[c] - 97 + num) % 26 + 97);
        }
        else
        {
            printf("%c", text[c]);
        }
    }
    printf("\n");
}
