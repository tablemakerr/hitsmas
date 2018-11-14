# hitsmas
A Python version of Giant Bomb's popular Hitsmas game mode for the recent Hitman games.

Ideally this simple python script should work for any newer version of python3 out of the box.  Further testing of that claim required

The idea is to just launch the script with the flags that appeal to you and the script will return how your Hitman contract should go!

Usage prompt below:

MERRY HITSMAS!!!!!!
This allows you to plop in a Himant 1 or 2 (NYI) map and we will spit out a contract for you

Targets may be done in any order
Each player only gets one chance at the game, unless a wildcard specifies otherwise

-h, --help, -?. ?    - Get this usage information
-b, --bombastic      - Enable Giant Bomb rules - Allow smuggled items to be set & configured.
-c, --chicago        - All pulls will be NOT be unique.
-l, --long_isalnd    - Remove the wildcard.
-m, --map            - Tells the program which map to use
Valid maps are paris(1), sapienza(2), marrakesh(3), bangkok(4), colorado(5), hokkaido(6)
-n, --num_players    - Sets the # of players & cycles through scenarios for each.
-v, --verbose        - Enable verbose output for this script.
