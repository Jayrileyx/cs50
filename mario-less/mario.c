#include <cs50.h>
#include <stdio.h>

void print_space(int spaces, int height);

void print_row(int bricks);

int main(void)
{
    // Prompt user for input
    int height;
    do
    {
        height = get_int("What is the height of the pyramid?");
    }
    while (height < 1 || height > 8);

    // Print a pyramid of that height
    for (int s = 0; s < height; s++)
    {
        print_space(height, s);
        print_row(s);
        printf("\n");
    }
}

void print_space(int height, int spaces)
{
    for (int s = 0; s < height - 1 - spaces; s++)
    {
        printf(" ");
    }
}

void print_row(int bricks)
{
    for (int b = 0; b < bricks + 1; b++)
    {
        printf("#");
    }
}
