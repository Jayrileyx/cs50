#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_num_letters(string text);
int count_num_words(string text);
int count_num_sentences(string text);

int main(void)
{
    // Prompt the user for text
    string text = get_string("Please enter text to be graded: ");

    // Count the number of letters, words, sentences in the text
    int num_letters = count_num_letters(text);
    int num_words = count_num_words(text);
    int num_sentences = count_num_sentences(text);

    // Compute the Coleman-Liau index
    float L = (float) num_letters / (float) num_words * 100;
    float S = (float) num_sentences / (float) num_words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Print the grade level
    if (index <= 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
int count_num_letters(string text)
{
    // Adding number of letters in text
    int num_letters = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isalpha(text[i]))
        {
            num_letters++;
        }
    }
    return num_letters;
}
int count_num_words(string text)
{
    // Adding number of words in text
    int num_words = 1;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isspace(text[i]))
        {
            num_words++;
        }
    }
    return num_words;
}
int count_num_sentences(string text)
{
    // Adding number of sentences in text
    int num_sentences = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            num_sentences++;
        }
    }
    return num_sentences;
}
