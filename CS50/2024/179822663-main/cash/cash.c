#include <cs50.h>
#include <stdio.h>

int calculate_coins(int cents, int coin_value);

int main(void)
{
    int cents = get_int("Change owed: ");
    while (cents < 0)
    {
        cents = get_int("Change owed: ");
    }

    int total_coins = 0;

    total_coins += calculate_coins(cents, 25);
    cents %= 25;

    total_coins += calculate_coins(cents, 10);
    cents %= 10;

    total_coins += calculate_coins(cents, 5);
    cents %= 5;

    total_coins += calculate_coins(cents, 1);

    printf("%d\n", total_coins);
}

int calculate_coins(int cents, int coin_value)
{
    int coins = 0;
    while (cents >= coin_value)
    {
        coins++;
        cents -= coin_value;
    }
    return coins;
}
