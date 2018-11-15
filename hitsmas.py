#!/usr/bin/env python

"""
Merry Hitsmas

Based on the Contract feature within 2016's Hitman in combination with the Video Game website Giant Bomb.  I present a scripted version of Hitsmas.

The purpose of this script is to save everyone money on those hats the Fortnite crowd tells you that you need.  Gotta save those vbucks somehow!
This script doesn't have any major design goals to it other than to present a fun programming project for myself.  
That said, all facets of this script are on a best effort basis and I guarantee nothing...well maybe something.

@Version 1.0
@Author TB
"""

# Import statements
import random
import string
import getopt
import sys

# Main
def main():
    
    # Define global variables that we care about
    global MAP
    global SMUGGLED_ENABLED
    global UNIQUE_PULLS
    global WILDCARD_REQUIRE
    global NUM_PLAYERS
    global VERBOSE

    # OK here is where we actually define them.
    SMUGGLED_ENABLED = False
    UNIQUE_PULLS = True
    WILDCARD_REQUIRE = True
    NUM_PLAYERS = 1
    MAP = 0
    VERBOSE = False

    # GetOpts
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
    
    # Check for any bad input that we can check for at the moment.
    sanity()

    # Start setting up what we need.
    setup()

"""
sanity()

Just does a few checks to make sure the script has enough information to run.
This could probably handle a few more things in the future.
"""
def sanity():
    FAIL = False
    
    if int(MAP) == 0:
        print("You must specify a map.\n")
        FAIL = True
    
    if int(MAP) > 6:
        print("You must specify a map between 1-6\n")
        FAIL = True
    
    # If any of these checks have failed, print the usage message which bails the whole script.    
    if FAIL:
        usage()

"""
setup()

Sets up the Dictionaries that contain all the static map information.
Then will check the count of players VS the amount of things on a map to ensure we can do enough if unique flags are set.
Finally, reminds players of the rules and launches the actual part of the script we care about.
"""
def setup():
    define_areas()

    if int(NUM_PLAYERS) > 1:
        check_counts()

    print("REMEMBER!  These are Illusive Target rules.")
    print("If you fail to assassinate your target in the given way, die, or target escapes, you LOSE!\n")
    print("Map:\t\t" + str(SELECTED_MAP.get('Name')))
    
    for player in range(int(NUM_PLAYERS)):
        print("\nPlayer " + str(player+1))
        hitsmas()

"""
hitsmas()

This is the bulk of the script.
Ideally this is called when all items have been verified as sane.
Takes in all your options and then actually spews out the rules of your contract as well as enough for the amount of players you specified.
"""
def hitsmas():
    # TODO: Add Color

    # Loop through each target
    for target in SELECTED_MAP.get('Targets'):
        # Grab a weapon from the valid pool.
        weapon = str(random.choice(SELECTED_MAP.get('Weapons')))
        
        # Grab a disguise from the valid pool.
        disguise = str(random.choice(SELECTED_MAP.get('Disguises')))
    
        # If we have uniqueness set, we will remove the items we just grabbed from the map's pool.
        # TODO - Can this be more efficient? 
        if UNIQUE_PULLS:    
            SELECTED_MAP.get('Weapons').remove(str(weapon))
            SELECTED_MAP.get('Disguises').remove(str(disguise))

        # Tell the player what to do for each target.    
        print("Target:\t\t" + target)
        print("DISGUISE:\t" + disguise)
        print("WEAPON:\t\t" + weapon + "\n")
    
    # Once the loop is over, we grab a wildcard for the map - if they're on.
    if WILDCARD_REQUIRE:
        # Grab a wildcard from the valid pool.
        wildcard = str(random.choice(SELECTED_MAP.get('Wildcards')))
        print("WILDCARD:\t" + wildcard + "\n")
        # If we have uniqueness set & there's more than one player, remove the wildcard from the map's pool.
        if UNIQUE_PULLS and int(NUM_PLAYERS) > 1:
            SELECTED_MAP.get('Wildcards').remove(str(wildcard))
    # Else, we will just alert that there is no wildcard
    else:
        print("!! Long Island rules in play.  Wildcard disabled\n")
    # If we have smuggled items enabled, - alert the player of such.
    if SMUGGLED_ENABLED:
        print("!! Bombastic rules in play.  You may choose a smuggled item\n")

"""
check_counts()

If we have more than one player, uses that number and figures if we have enough items equipped on the map for that amount.
Formula is basically if #Items < (#Players*#Targets) then the script will fail out because we don't have enough stuff to be unique every time.
Prompts you to turn off unique flag if you have too many people playing.

# TODO Set flags for unique weapons, unique disguises, or unique both.
# TODO I'm sure there's a better way to not have so many print statements for each IF block
"""
def check_counts():
    # Verify if we want to do that.
    if UNIQUE_PULLS:
        # Get the counts for each item now that we know the map
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

"""
define_areas()

Actualy sets up the Dictionaries that contain each map's information. 
Probably the easiest way I've found so far to deal with all this static information rather than shipping a bunch of CSV or XML files.
Probably not that well off for usability if people don't want to go into the code to add to each map.
But then again you probably pulled this from my Github so I'll assume you know enough of what you're doing if you're also reading this.
"""
def define_areas():

    # Setup the maps as globals as they need to be accessed elsewhere
    global PARIS
    global SAPIENZA
    global MARRAKESH
    global BANGKOK
    global COLORADO
    global HOKKAIDO
    global SELECTED_MAP

    # Need more/better Wildcards
    PARIS = {
        'Name':'Paris, France',
        'Targets':['Viktor Novikov', 'Dalia Margolis'], 
        'Weapons':['Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive', 'Screwdriver'], 
        'Disguises':['Chef', 'Palace Staff', 'Auction Staff', 'Stylist', 'Crew Member', 'Guard', 'HELMUT FUCKING KRUGER', 'SHEIKH ZANZIBAR'],
        'Wildcards':['Kill Bystander in Front of a Target', 'Invert Your Default Axis', 'Set Off Explosion In Runway', 'Kill One Target During/After Fireworks', 'One Save Scum', 'Choose Starting Location', 'Put 5 Bodies In Any One Bathroom']
    }

    # Need more/better Wildcards
    SAPIENZA = {
        'Name':'Sapienza, Italy',
        'Targets':['Silvio Caruso', 'Francesca De Santis'], 
        'Weapons':['Amputation Knife', 'Circumscision Knife', 'Katana', 'Hatchet', 'Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Delivery Man', 'Gardener', 'Plumber', 'Store Clerk', 'Any Guard', 'Church Staff', 'Priest', 'Plague Doctor', 'Waiter/Butler', 'Kitchen Staff', 'Mansion Staff', 'Hazmat Suit', 'Lab Tech', 'Private Dick', 'Dr Oscar', 'Roberto Vargas', 'Cyclist', 'Bohemian', 'Street Performer'], 
        'Wildcards':['Kill Bystander in Front of a Target', 'Invert Your Default Axis', 'Ring Church Bell', 'Must Escape via Airplane', 'Win After 2nd Target', 'Knock Out 5 People With Spaghetti Sauce', 'One Save Scum', 'Choose Starting Location', 'Put 3 Bodies In Wood Chipper']
    }

    # Need more/better Wildcards
    MARRAKESH = {
        'Name':'Marrakesh, Morroco',
        'Targets':['Claus Hugo Strandberg', 'Reza Zaydan'], 
        'Weapons':['Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Shop Keep', 'Food Vendor', 'Waiter', 'Handyman', 'Printing Crew', 'Any Guard (Non Military)', 'Any Non-Military Officer', 'Janitor', 'Cameraman', 'Intern', 'Masseur', 'Prisoner', 'Fortune Teller'],
        'Wildcards':['Kill Bystander in Front of a Target', 'Invert Your Default Axis', 'One Save Scum', 'Choose Starting Location', 'Put 5 Bodies In Any One Bathroom', 'Coin a Soldier Through a Hallway Length', 'Shootout All Cameras', 'Break-Up The Protest']
    }

    # Need more/better Wildcards
    BANGKOK = {
        'Name':'Bangkok, Thailand',
        'Targets':['Jordan Cross', 'Ken Morgan'], 
        'Weapons':['Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Hotel Staff', 'Any Non-Unique Guard', 'Waiter', 'Kitchen Staff', 'Groundskeeper', 'Exterminator', 'Recording Crew', 'Jordan Cross Bodyguard', 'Morgans Bodyguard', 'Abel De Silva', 'Stalker'],
        'Wildcards':['Kill Bystander in Front of a Target', 'Invert Your Default Axis', 'You Must RAWK OUT',  'One Save Scum', 'Choose Starting Location', 'Put 5 Bodies In Any One Bathroom', 'Hit 3 People With a Golf Club', 'Put 2 People in the Ocean']
    }

    # Need more/better Wildcards
    # Try not to use unique pulls with this level....
    COLORADO = {
        'Name':'Colorado, USA',
        'Targets':['Sean Rose', 'Maya Parvati', 'Ezra Berg', 'Penelope Graves'], 
        'Weapons':['Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Cook', 'Technician', 'Soldier', 'Elite Solider', 'Spec Ops', 'Explosives Specialist', 'Hacker', 'Point Man', 'Scarecrow'],
        'Wildcards':['Kill Bystander in Front of a Target', 'Invert Your Default Axis', 'Snipe 2 of your Targets', 'Only Kill 2 Targets', 'One Save Scum', 'Brand 2 People', 'Beat 3 People With a Mannequin Arm', 'Choose Starting Location', 'Kill at Least One Non-Target via Sabotage']
    }

    # Need more/better Wildcards
    HOKKAIDO = {
        'Name':'Hokkaido, Japan',
        'Targets':['Erich Soders', 'Yuki Yamazaki'], 
        'Weapons':['Oversized Weapon', 'Chef Implement', 'Medical Implement', 'Thrown Item', 'Katana', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Patient', 'Resort Staff', 'Chef', 'Handyman', 'Resort Security', 'Doctor', 'Morgue Doctor', 'Surgeon', 'Body Guard', 'Hospital Director', 'Chief Surgeon', 'Any VIP Patient', 'Yoga Instructor', 'Helicopter Pilot', 'Ninja', 'Motorcyclist', 'Baseball Player'],
        'Wildcards':['Kill Bystander in Front of a Target', 'Invert Your Default Axis', 'Get Plastic Surgery', 'You Can Kill the Heart Instead', 'Kill the AI', 'One Save Scum', 'Choose Starting Location', 'Put 5 Bodies In Any One Bathroom']
    }

    """
    # PLACEHOLDERS for Hitman 2

    # TODO
    HAWKES_BAY = {
        'Name':"Hawke's Bay, New Zealand"
        'Targets':['Silvio Caruso', 'Francesca De Santis'], 
        'Weapons':['Amputation Knife', 'Circumscision Knife', 'Katana', 'Hatchet', 'Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Delivery Man', 'Gardener', 'Plumber', 'Store Clerk', 'Any Guard', 'Church Staff', 'Priest', 'Plague Doctor', 'Waiter/Butler', 'Kitchen Staff', 'Mansion Staff', 'Hazmat Suit', 'Lab Tech', 'Private Dick', 'Dr Oscar', 'Roberto Vargas', 'Cyclist', 'Bohemian', 'Street Performer'], 
        'Wildcards':['Ring Church Bell', 'Must Escape via Airplane', 'Win After 2nd Target', 'Knock Out 5 People With Spaghetti Sauce', 'One Save Scum', 'Choose Starting Location', 'Put 3 Bodies In Wood Chipper']
    }

    # TODO
    MIAMI = {
        'Name':'Miami, Florida',
        'Targets':['Silvio Caruso', 'Francesca De Santis'], 
        'Weapons':['Amputation Knife', 'Circumscision Knife', 'Katana', 'Hatchet', 'Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Delivery Man', 'Gardener', 'Plumber', 'Store Clerk', 'Any Guard', 'Church Staff', 'Priest', 'Plague Doctor', 'Waiter/Butler', 'Kitchen Staff', 'Mansion Staff', 'Hazmat Suit', 'Lab Tech', 'Private Dick', 'Dr Oscar', 'Roberto Vargas', 'Cyclist', 'Bohemian', 'Street Performer'], 
        'Wildcards':['Ring Church Bell', 'Must Escape via Airplane', 'Win After 2nd Target', 'Knock Out 5 People With Spaghetti Sauce', 'One Save Scum', 'Choose Starting Location', 'Put 3 Bodies In Wood Chipper']
    }

    # TODO
    SANTA_FORTUNA = {
        'Name':'Santa Fortuna, Colombia,
        'Targets':['Silvio Caruso', 'Francesca De Santis'], 
        'Weapons':['Amputation Knife', 'Circumscision Knife', 'Katana', 'Hatchet', 'Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Delivery Man', 'Gardener', 'Plumber', 'Store Clerk', 'Any Guard', 'Church Staff', 'Priest', 'Plague Doctor', 'Waiter/Butler', 'Kitchen Staff', 'Mansion Staff', 'Hazmat Suit', 'Lab Tech', 'Private Dick', 'Dr Oscar', 'Roberto Vargas', 'Cyclist', 'Bohemian', 'Street Performer'], 
        'Wildcards':['Ring Church Bell', 'Must Escape via Airplane', 'Win After 2nd Target', 'Knock Out 5 People With Spaghetti Sauce', 'One Save Scum', 'Choose Starting Location', 'Put 3 Bodies In Wood Chipper']
    }

    # TODO
    MUMBAI = {
        'Name':'Mumbai, India',
        'Targets':['Silvio Caruso', 'Francesca De Santis'], 
        'Weapons':['Amputation Knife', 'Circumscision Knife', 'Katana', 'Hatchet', 'Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Delivery Man', 'Gardener', 'Plumber', 'Store Clerk', 'Any Guard', 'Church Staff', 'Priest', 'Plague Doctor', 'Waiter/Butler', 'Kitchen Staff', 'Mansion Staff', 'Hazmat Suit', 'Lab Tech', 'Private Dick', 'Dr Oscar', 'Roberto Vargas', 'Cyclist', 'Bohemian', 'Street Performer'], 
        'Wildcards':['Ring Church Bell', 'Must Escape via Airplane', 'Win After 2nd Target', 'Knock Out 5 People With Spaghetti Sauce', 'One Save Scum', 'Choose Starting Location', 'Put 3 Bodies In Wood Chipper']
    }

    # TODO
    WHITTLETON_CREEK = {
        'Name':'Whittleton Creek, Vermont',
        'Targets':['Silvio Caruso', 'Francesca De Santis'], 
        'Weapons':['Amputation Knife', 'Circumscision Knife', 'Katana', 'Hatchet', 'Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Delivery Man', 'Gardener', 'Plumber', 'Store Clerk', 'Any Guard', 'Church Staff', 'Priest', 'Plague Doctor', 'Waiter/Butler', 'Kitchen Staff', 'Mansion Staff', 'Hazmat Suit', 'Lab Tech', 'Private Dick', 'Dr Oscar', 'Roberto Vargas', 'Cyclist', 'Bohemian', 'Street Performer'], 
        'Wildcards':['Ring Church Bell', 'Must Escape via Airplane', 'Win After 2nd Target', 'Knock Out 5 People With Spaghetti Sauce', 'One Save Scum', 'Choose Starting Location', 'Put 3 Bodies In Wood Chipper']
    }

        # TODO
    ISLE_OF_SGAIL = {
        'Name':'Isle of Sgàil, Atlantic Ocean',
        'Targets':['Silvio Caruso', 'Francesca De Santis'], 
        'Weapons':['Amputation Knife', 'Circumscision Knife', 'Katana', 'Hatchet', 'Oversized Weapon', 'Chef Implement', 'Thrown Item', 'Sword', 'Any Firearm',  'Sabotage', 'Any Explosive'], 
        'Disguises':['Delivery Man', 'Gardener', 'Plumber', 'Store Clerk', 'Any Guard', 'Church Staff', 'Priest', 'Plague Doctor', 'Waiter/Butler', 'Kitchen Staff', 'Mansion Staff', 'Hazmat Suit', 'Lab Tech', 'Private Dick', 'Dr Oscar', 'Roberto Vargas', 'Cyclist', 'Bohemian', 'Street Performer'], 
        'Wildcards':['Ring Church Bell', 'Must Escape via Airplane', 'Win After 2nd Target', 'Knock Out 5 People With Spaghetti Sauce', 'One Save Scum', 'Choose Starting Location', 'Put 3 Bodies In Wood Chipper']
    }
    """

    # This dictionary is used in conjunction with the command flag of -m to determine which map to use.
    # This will also allow us to expand on the amount of maps once we incorporate Hitman 2 (2018)
    MAPS = {
        1: PARIS,
        2: SAPIENZA,
        3: MARRAKESH,
        4: BANGKOK,
        5: COLORADO,
        6: HOKKAIDO
    }
    SELECTED_MAP = MAPS.get(int(MAP)) 
"""
        # PLACEHOLDERS for Hitman 2
        7: HAWKES_BAY,
        8: MIAMI,
        9: SANTA_FORTUNA,
        10: MUMBAI,
        11: WHITTLETON_CREEK,
        12: ISLE_OF_SGAIL
    }
""" 

"""
usage()

This just spits out the help message for confused peeps and hopefully gives some good information on how to use this script.
"""
def usage():
    print ('MERRY HITSMAS!!!!!!')
    print ('This allows you to plop in a Himant 1 or 2 (NYI) map and we will spit out a contract for you')
    print ('')
    print ('Targets may be done in any order')
    print ('Each player only gets one chance at the game, unless a wildcard specifies otherwise')
    print ('')
    print ('-h, --help, -?. ?    - Get this usage information')
    print ('-b, --bombastic      - Enable Bomber rules - Allow smuggled items to be set & configured.')
    print ('-c, --chicago        - All pulls will NOT be unique.')
    print ('-l, --long_isalnd    - Removes the wildcard.')
    print ('-n, --num_players #  - Sets the # of players & cycles through scenarios for each.')
    print ('-m, --map            - Tells the program which map to use')
    print ('Valid maps are paris(1), sapienza(2), marrakesh(3), bangkok(4), colorado(5), hokkaido(6)')
    #print ('NYI -v, --verbose        - Enable verbose output for this script.')
    sys.exit(0)

"""
!!!NYI!!!
verbose(text)

@param text - The text that you want printed out.

Used for verbose output of the script.  Ideally this is just for debugging what may be going wrong if there's an issue.
"""
def verbosity(text):
    if VERBOSE:
        print(str(text))

### Call Main
if __name__ == "__main__":
    main()
