#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int letter_values[] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                       1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int calculate_score(string answer);

int main(void)
{
    // Prompt Player 1 & Player 2 for input
    string p1_word = get_string("Player 1: ");
    string p2_word = get_string("Player 2: ");

    // Calculate score of each word
    int score1 = calculate_score(p1_word);
    int score2 = calculate_score(p2_word);

    // Print winner of the round including tie
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}
int calculate_score(string answer)
{
    // Start with score at zero
    int score = 0;

    // Needs to handle upper and lower case
    for (int i = 0, length = strlen(answer); i < length; i++)
    {
        if (isupper(answer[i]))
        {
            score += letter_values[answer[i] - 'A'];
        }
        else if (islower(answer[i]))
        {
            score += letter_values[answer[i] - 'a'];
        }
    }
    return score;
}
