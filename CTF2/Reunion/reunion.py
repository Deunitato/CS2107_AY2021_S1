#!/usr/bin/env python2
import random, sqlite3, sys

# Just a wrapper function to print line to standard output
def printline(data = "", end = "\n"):
    sys.stdout.write(data + end)
    sys.stdout.flush()

# Just a wrapper function to keep reading line input until there's valid input
def readline():
    while True:
        line = sys.stdin.readline().strip()
        if len(line) > 0:
            return line

# Populate database with nice videos suitable to play during a reunion dinner
def init_db():
    try:
        with open("flag.txt", "r") as f:
            flag = f.read().strip()
    except:
        flag = "you_need_to_connect_to_the_remote_service_to_get_the_flag"
        printline("Unable to open flag.txt. Using dummy flag value: {flag}".format(flag=flag))

    # Use non-persistent database, so changes are not saved across connections
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    global sql
    sql = connection.cursor()

    sample_videos = [
        {"url": "https://www.youtube.com/watch?v=LcL_lsWqEfs", "rating": 5, "topic": "Akira"},
        {"url": "https://www.youtube.com/watch?v=r-5KzHDPCTM", "rating": 5, "topic": "Cow"},
        {"url": "https://www.youtube.com/watch?v=3DkqMjfqqPc", "rating": 5, "topic": "Salamander"},
        {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "rating": 4, "topic": "Rick"},
        {"url": "https://www.youtube.com/watch?v=wZZ7oFKsKzY", "rating": 2, "topic": "Cat"},
        {"url": "https://www.youtube.com/watch?v=5w8QEWA8wGM", "rating": 1, "topic": "Shark"},
        {"url": "https://www.youtube.com/watch?v=-50NdPawLVY", "rating": 0, "topic": "Crab"}
    ]

    sql.execute("CREATE TABLE flags (flag text)")
    sql.execute("CREATE TABLE videos (topic text, rating int, url text)")
    sql.execute("INSERT INTO flags VALUES ('{flag}')".format(flag=flag))

    for video in sample_videos:
        sql.execute("INSERT INTO videos VALUES ('{topic}', '{rating}', '{url}')".format(topic=video["topic"], rating=video["rating"], url=video["url"]))

# Pretty-print all the videos fetched from query
def print_videos(videos):
    for id, video in enumerate(videos):
        printline("#{id}: Topic: {topic}, Rating: {rating}, URL: {url}".format(id=id+1, topic=video["topic"], rating=video["rating"], url=video["url"]))
    printline()

# Timer restriction is imposed on remote service, but removed here for local testing purposes
def loop_forever():
    options_msg = "\n".join([
        "What do you want to do next?",
        "1) Save a video",
        "2) List all videos",
        "3) Search video by topic",
        "4) Search video by rating",
        "5) Play random videos",
        "6) Stop watching now",
        "Enter option: "
    ])

    options = {
        "1": option_one,
        "2": option_two,
        "3": option_three,
        "4": option_four,
        "5": option_five,
        "6": option_six,
    }

    while True:
        printline(options_msg, end="")
        option = readline();
        if option not in options.keys():
            printline("Invalid option selected!")
            continue

        # execute function corresponding to option chosen
        try:
            options[option]()
        except sqlite3.OperationalError:
            printline("An unexpected error occured while querying the database")

# Save a video
def option_one():
    printline("Enter topic: ", end="")
    topic = readline().replace('"', "")
    while True:
        try:
            printline("Enter rating: ", end="")
            rating = int(readline())
            break
        except ValueError:
            printline("Invalid rating! Rating must be an integer value!")
    printline("Enter URL: ", end="")
    url = readline().replace('"', "")
    sql.execute('INSERT INTO videos VALUES ("{topic}", "{rating}", "{url}")'.format(topic=topic, url=url, rating=rating))
    printline("Adding video - Topic: {topic}, Rating: {rating}, URL: {url}".format(topic=topic, rating=rating, url=url))

# List all videos
def option_two():
    videos = sql.execute("SELECT topic, rating, url FROM videos").fetchall()
    printline()
    printline("Listing all videos:")
    print_videos(videos)

# Search video by topic
def option_three():
    printline("Enter topic: ", end="")
    topic = readline().replace("'", "")
    videos = sql.execute("SELECT topic, rating, url FROM videos WHERE topic = '{topic}' COLLATE NOCASE".format(topic=topic)).fetchall()
    print_videos(videos)

# Search video by rating
def option_four():
    while True:
        try:
            printline("Enter rating: ", end="")
            rating = int(readline())
            break
        except ValueError:
            printline("Invalid rating! Rating must be an integer value!")
    videos = sql.execute("SELECT topic, rating, url FROM videos WHERE rating = '{rating}' COLLATE NOCASE".format(rating=rating)).fetchall()
    print_videos(videos)

# Play random videos
def option_five():
    topic = random.choice(list(sql.execute("SELECT DISTINCT topic FROM videos")))["topic"]
    printline("Chosen to play random topic: {topic}".format(topic=topic))
    videos = sql.execute("SELECT topic, rating, url FROM videos WHERE topic = '{topic}' COLLATE NOCASE".format(topic=topic)).fetchall()
    print_videos(videos)

# Stop playing now
def option_six():
    printline("Hope you liked the videos and enjoy your reunion dinner!")
    sys.exit(0)

def main():
    init_db()
    printline("It's time for reunion dinner, but you are hooked onto YouTube videos...")
    loop_forever()

if __name__ == "__main__":
    main()
