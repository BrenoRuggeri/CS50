#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SIZE 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    char *file = argv[1];
    FILE *raw_file = fopen(argv[1], "r");

    if (raw_file == NULL)

    {
        return 1;
    }
    bool found_jpg = false;
    int count = 0;
    uint8_t buffer[SIZE];
    char file_name[8];
    FILE *img = NULL;

    while (fread(buffer, SIZE, 1, raw_file) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (found_jpg)
            {
                fclose(img);
            }
            else
            {
                found_jpg = true;
            }

            sprintf(file_name, "%03i.jpg", count);
            img = fopen(file_name, "w");
            if (img == NULL)
            {
                fclose(raw_file);
                return 3;
            }
            count++;
        }
        if (found_jpg)
        {
            fwrite(buffer, SIZE, 1, img);
        }
    }
    fclose(raw_file);
    if (found_jpg)
    {
        fclose(img);
    }
    return 0;
}
