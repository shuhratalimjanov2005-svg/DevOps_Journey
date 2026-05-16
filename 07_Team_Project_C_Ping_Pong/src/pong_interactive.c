#include <ncurses.h>
#include <unistd.h>

int main() {

  int width = 80, height = 25;

  int pad_l_y = 12, pad_r_y = 12;

  int ball_x = 40, ball_y = 12;
  int ball_dx = 1, ball_dy = 1;

  int score_l = 0, score_r = 0;

  initscr();
  noecho();
  curs_set(0);
  timeout(50);
  keypad(stdscr, TRUE);

  int game_running = 1;
  while (game_running && score_l < 21 && score_r < 21) {
    clear();

    mvprintw(0, 33, "Score: %d | %d", score_l, score_r);
    for (int i = 0; i < width; i++) {
      mvaddch(1, i, '-');
      mvaddch(height - 1, i, '-');
    }

    mvaddch(pad_l_y - 1, 2, '|');
    mvaddch(pad_l_y, 2, '|');
    mvaddch(pad_l_y + 1, 2, '|');

    mvaddch(pad_r_y - 1, width - 3, '|');
    mvaddch(pad_r_y, width - 3, '|');
    mvaddch(pad_r_y + 1, width - 3, '|');

    mvaddch(ball_y, ball_x, 'O');

    int ch = getch();
    if (ch == 'a' || ch == 'A') {
      if (pad_l_y > 3)
        pad_l_y--;
    }
    if (ch == 'z' || ch == 'Z') {
      if (pad_l_y < height - 3)
        pad_l_y++;
    }
    if (ch == 'k' || ch == 'K') {
      if (pad_r_y > 3)
        pad_r_y--;
    }
    if (ch == 'm' || ch == 'M') {
      if (pad_r_y < height - 3)
        pad_r_y++;
    }
    if (ch == 'q' || ch == 'Q') {
      game_running = 0;
    }

    ball_x += ball_dx;
    ball_y += ball_dy;

    if (ball_y <= 2 || ball_y >= height - 2)
      ball_dy *= -1;

    if (ball_x == 3 && (ball_y >= pad_l_y - 1 && ball_y <= pad_l_y + 1)) {
      ball_dx *= -1;
    } else if (ball_x <= 0) {
      score_r++;
      ball_x = 40;
      ball_y = 12;
      ball_dx = 1;
    }

    if (ball_x == width - 4 &&
        (ball_y >= pad_r_y - 1 && ball_y <= pad_r_y + 1)) {
      ball_dx *= -1;
    } else if (ball_x >= width) {
      score_l++;
      ball_x = 40;
      ball_y = 12;
      ball_dx = -1;
    }

    refresh();
  }

  clear();
  if (score_l >= 21)
    mvprintw(12, 30, "LEFT PLAYER WINS!");
  else if (score_r >= 21)
    mvprintw(12, 30, "RIGHT PLAYER WINS!");
  refresh();
  sleep(2);
  endwin();

  return 0;
}
