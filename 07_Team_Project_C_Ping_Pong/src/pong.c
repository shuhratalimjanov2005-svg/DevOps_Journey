#include <stdio.h>

int main() {
    int width = 80, height = 25;
    int pad_l_y = 12, pad_r_y = 12;
    int ball_x = 40, ball_y = 12;
    int ball_dx = 1, ball_dy = 1;
    int score_l = 0, score_r = 0;

    while (score_l < 21 && score_r < 21) {
        
        printf("\033[H\033[J");

        printf("             Score: %d | %d\n", score_l, score_r);

       
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if (y == 0 || y == height - 1) {
                    printf("-");
                } else if (x == 0 || x == width - 1) {
                    printf("|");
                } else if (x == ball_x && y == ball_y) {
                    printf("O");
                } else if (x == 2 && (y == pad_l_y - 1 || y == pad_l_y || y == pad_l_y + 1)) {
                    printf("|");
                } else if (x == width - 3 && (y == pad_r_y - 1 || y == pad_r_y || y == pad_r_y + 1)) {
                    printf("|");
                } else {
                    printf(" ");
                }
            }
            printf("\n");
        }

        
        char action;
        if (scanf(" %c", &action) != 1) continue;

        if (action == 'q' || action == 'Q') break;
        if ((action == 'a' || action == 'A') && pad_l_y > 2) pad_l_y--;
        if ((action == 'z' || action == 'Z') && pad_l_y < height - 3) pad_l_y++;
        if ((action == 'k' || action == 'K') && pad_r_y > 2) pad_r_y--;
        if ((action == 'm' || action == 'M') && pad_r_y < height - 3) pad_r_y++;
       

      
        ball_x += ball_dx;
        ball_y += ball_dy;

        
        if (ball_y <= 1 || ball_y >= height - 2) ball_dy *= -1;

        
        if (ball_x == 3 && (ball_y >= pad_l_y - 1 && ball_y <= pad_l_y + 1)) {
            ball_dx *= -1;
        } else if (ball_x <= 0) {
            score_r++;
            ball_x = 40; ball_y = 12; ball_dx = 1;
        }

        
        if (ball_x == width - 4 && (ball_y >= pad_r_y - 1 && ball_y <= pad_r_y + 1)) {
            ball_dx *= -1;
        } else if (ball_x >= width - 1) {
            score_l++;
            ball_x = 40; ball_y = 12; ball_dx = -1;
        }
    }

    if (score_l >= 21) printf("Congratulations! LEFT PLAYER WINS!\n");
    if (score_r >= 21) printf("Congratulations! RIGHT PLAYER WINS!\n");

    return 0;
}


