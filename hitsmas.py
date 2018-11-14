import random
import string
import getopt
import sys

def main():
    global MAP
    global SMUGGLED_ENABLED
    global UNIQUE_PULLS
    global WILDCARD_REQUIRE
    global NUM_PLAYERS

    SMUGGLED_ENABLED = False
    UNIQUE_PULLS = True
    WILDCARD_REQUIRE = True
    NUM_PLAYERS = 1
    MAP = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], "bchlm:n:v?", ["bombastic", "chicago", "help", "long_island", "map", "num_players", "verbose"])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt in ("-h", "help", "--help", "?", "-?"):
            usage()
        elif opt in ("-b", "--bombastic"):
            SMUGGLED_ENABLED = True
        elif opt in ("-c", "--chicago"):
            UNIQUE_PULLS = False
        elif opt in ("-l", "--long_island"):
            WILDCARD_REQUIRE = False    
        elif opt in ("-m", "--map"):
            MAP = arg    
        elif opt in ("-n", "--num_players"):
            NUM_PLAYERS = arg     
        elif opt in ("-v", "--verbose"):
            VERBOSE = True
    sanity()
    setup()

def sanity():
    FAIL = False
    if int(MAP) == 0:
        print("You must specify a map.\n")
        FAIL = True
    if int(MAP) > 6:
        print("You must specify a map between 1-6\n")
        FAIL = True
    if FAIL:
        usage()

def setup():
    define_areas()
    check_counts()

    print("REMEMBER!  These are Illusive Target rules.")
    print("If you fail to assassinate your target in the given way, die, or target escapes, you LOSE!\n")
    print("Map:\t\t" + str(SELECTED_MAP.get('Name')))
    for player in range(int(NUM_PLAYERS)):
        print("\nPlayer " + str(player+1))
        hitsmas()

def hitsmas():
    # TODO: Add Color
    # TODO: Make Weapon & Disguise pulls unique
    # TODO: Setup loop to take multiple players with unique wildcards
    #print(SELECTED_MAP.values())

    for target in SELECTED_MAP.get('Targets'):
        weapon = str(random.choice(SELECTED_MAP.get('Weapons')))
        disguise = str(random.choice(SELECTED_MAP.get('Disguises')))
        if UNIQUE_PULLS:    
            SELECTED_MAP.get('Weapons').remove(str(weapon))
            SELECTED_MAP.get('Disguises').remove(str(disguise))
        print("Target:\t\t" + target)
        print("DISGUISE:\t" + disguise)
        print("WEAPON:\t\t" + weapon + "\n")
    if WILDCARD_REQUIRE:
        wildcard = str(random.choice(SELECTED_MAP.get('Wildcards')))
        print("WILDCARD:\t" + wildcard + "\n")
        SELECTED_MAP.get('Wildcards').remove(str(wildcard))
    else:
        print("!! Long Island rules in play.  Wildcard disabled\n")
    if SMUGGLED_ENABLED:
        print("!! Bombastic rules in play.  You may choose a smuggled item\n")
    #print(SELECTED_MAP.values())

def check_counts():
    if UNIQUE_PULLS:
        NUM_WEAPONS = len(SELECTED_MAP.get('Weapons'))
        NUM_DISGUISES = len(SELECTED_MAP.get('Disguises'))
        NUM_TARGETS = len(SELECTED_MAP.get('Targets'))
        NUM_WILDCARDS = len(SELECTED_MAP.get('Wildcards'))
        REQUIRED_NUM_ITEMS = int(NUM_PLAYERS)*int(NUM_TARGETS)

        if int(NUM_WEAPONS) < int(REQUIRED_NUM_ITEMS): 
            print("Not enough Weapons on this Map for unique pulls")
            print("Please try again with Chicago rules in place.  Or yell at Tyler to add more shit.\n")
            print("# of weapons configured:\t" + str(NUM_WEAPONS))
            print("Required # of weapons:\t\t" + str(REQUIRED_NUM_ITEMS))
            sys.exit(3)
        if int(NUM_DISGUISES) < int(REQUIRED_NUM_ITEMS):
            print("Not enough Disguises on this Map for unique pulls")
            print("Please try again with Chicago rules in place.  Or yell at Tyler to add more shit.\n")
            print("# of disguises configured:\t" + str(NUM_DISGUISES))
            print("Required # of disguises:\t\t" + str(REQUIRED_NUM_ITEMS))
            sys.exit(3)
        if int(NUM_WILDCARDS) < int(NUM_PLAYERS):
            print("Not enough Wildcards on this Map for unique pulls")
            print("Please try again with Chicago rules in place.  Or yell at Tyler to add more shit.\n")
            print("Num of wildcards configured:\t" + str(NUM_WILDCARDS))
            print("Required # of wildcards:\t\t" + str(NUM_PLAYERS))
            sys.exit(3)

def define_areas():

    global PARIS
    global SAPIENZA
    global MARRAKESH
    global BANGKOK
    global COLORADO
    global HOKKAIDO
    global SELECTED_MAP

    PARIS = {
        'Name':'Paris, France',
        'Targets':['Viktor Novikov', 'Dalia Margolis'], 
        'Weapons':['Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive', 'Screwdriver'], 
        'Disguises':['Chef', 'Palace Staff', 'Auction Staff', 'Stylist', 'Crew Member', 'Guard', 'HELMUT FUCKING KRUGER', 'SHEIKH ZANZIBAR'],
        'Wildcards':['Set Off Explosion In Runway', 'Kill One Target During/After Fireworks', 'One Save Scum', 'Choose Starting Location', 'Put 5 Bodies In Any One Bathroom']
    }

    SAPIENZA = {
        'Name':'Sapienza, Italy',
        'Targets':('Silvio Caruso', 'Francesca De Santis'), 
        'Weapons':('Amputation Knife', 'Circumscision Knife', 'Katana', 'Hatchet', 'Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'), 
        'Disguises':('Delivery Man', 'Gardener', 'Plumber', 'Store Clerk', 'Any Guard', 'Church Staff', 'Priest', 'Plague Doctor', 'Waiter/Butler', 'Kitchen Staff', 'Mansion Staff', 'Hazmat Suit', 'Lab Tech', 'Private Dick', 'Dr Oscar', 'Roberto Vargas', 'Cyclist', 'Bohemian', 'Street Performer'), 
        'Wildcards':('Ring Church Bell', 'Must Escape via Airplane', 'Win After 2nd Target', 'Knock Out 5 People With Spaghetti Sauce', 'One Save Scum', 'Choose Starting Location', 'Put 3 Bodies In Wood Chipper')
    }

    MARRAKESH = {
        'Name':'Marrakesh, Morroco',
        'Targets':('Claus Hugo Strandberg', 'Reza Zaydan'), 
        'Weapons':('Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'), 
        'Disguises':('helmut fucking kruger','sheikeh zanzibar'),
        'Wildcards':('Set Off Explosion In Runway', 'One Save Scum', 'Choose Starting Location', 'Put 5 Bodies In Any One Bathroom')
    }

    BANGKOK = {
        'Name':'Bangkok, Thailand',
        'Targets':('Jordan Cross', 'Ken Morgan'), 
        'Weapons':('Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'), 
        'Disguises':('helmut fucking kruger','sheikeh zanzibar'),
        'Wildcards':('Set Off Explosion In Runway', 'You Must RAWK OUT',  'One Save Scum', 'Choose Starting Location', 'Put 5 Bodies In Any One Bathroom')
    }

    COLORADO = {
        'Name':'Colorado, USA',
        'Targets':('Sean Rose', 'Maya Parvati', 'Ezra Berg', 'Penelope Graves'), 
        'Weapons':('Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'), 
        'Disguises':('helmut fucking kruger','sheikeh zanzibar'),
        'Wildcards':('Set Off Explosion In Runway', 'Only Kill 2 Targets', 'One Save Scum', 'Choose Starting Location', 'Put 5 Bodies In Any One Bathroom')
    }

    HOKKAIDO = {
        'Name':'Hokkaido, Japan',
        'Targets':('Erich Soders', 'Yuki Yamazaki'), 
        'Weapons':('Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'), 
        'Disguises':('helmut fucking kruger','sheikeh zanzibar'),
        'Wildcards':('Set Off Explosion In Runway', 'Kill the AI', 'One Save Scum', 'Choose Starting Location', 'Put 5 Bodies In Any One Bathroom')
    }

    MAPS = {
        1: PARIS,
        2: SAPIENZA,
        3: MARRAKESH,
        4: BANGKOK,
        5: COLORADO,
        6: HOKKAIDO
    }

    SELECTED_MAP = MAPS.get(int(MAP))    

def usage():
    print ('MERRY HITSMAS!!!!!!')
    print ('This allows you to plop in a Himant 1 or 2 (NYI) map and we will spit out a contract for you')
    print ('')
    print ('Targets may be done in any order')
    print ('Each player only gets one chance at the game, unless a wildcard specifies otherwise')
    print ('')
    print ('-h, --help, -?. ?    - Get this usage information')
    print ('-b, --bombastic      - Enable Giant Bomb rules - Allow smuggled items to be set & configured.')
    print ('-c, --chicago        - All pulls will be NOT be unique.')
    print ('-l, --long_isalnd    - Remove the wildcard.')
    print ('-m, --map            - Tells the program which map to use')
    print ('Valid maps are paris(1), sapienza(2), marrakesh(3), bangkok(4), colorado(5), hokkaido(6)')
    print ('-n, --num_players    - Sets the # of players & cycles through scenarios for each.')
    print ('-v, --verbose        - Enable verbose output for this script.')
    sys.exit(0)

### Call Main
if __name__ == "__main__":
    main()
