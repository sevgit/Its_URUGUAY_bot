import datetime
import random
import string
import traceback

import praw

import botlogin


comment_log_path = "log.txt"

misspells = {
    "Uruguay": [
        "urugay",
        "uraguay",
        "uragay",
        "urogway",
        "uruguauy",
        "uruguary",
    ],
    "Uruguayan": [
        "urugayan",
        "uraguayan",
        "uragayan",
        "urogwayan",
        "uruguauyan",
        "uruguaryan",
    ]
}

replies = [
    "Did you mean **{}**?",
    "I'm pretty sure you meant **{}**",
]


def update_log(id, log_path):
    """ For comments that were already replied"""
    with open(log_path, 'a') as my_log:
        my_log.write(id + "\n")


def load_log(log_path):
    """ For comments that were already replied"""
    with open(log_path) as my_log:
        log = my_log.readlines()
        log = [x.strip('\n') for x in log]
        return log


def output_log(text):
    """ Used for debugging."""
    output_log_path = './logs/{}_output_log.txt'.format(
        datetime.date.today().strftime('%Y_%m')
    )
    with open(output_log_path, 'a') as myLog:
        s = "[{}]: {}\n".format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text
        )
        myLog.write(s)


def find_substring(needle, haystack):
    """ Only returns true if needle is found and it's a whole word."""
    index = haystack.find(needle)
    if index == -1:
        return False
    if index != 0 and haystack[index-1] in string.letters:
        return False
    L = index + len(needle)
    if L < len(haystack) and haystack[L] in string.letters:
        return False
    return True


def is_quote(text):
    return len(text) > 1 and text[0] == '>'


def check_misspells(text, misspells):
    for version in misspells:
        if find_substring(version, text.lower()):
            return True


def get_reply():
    return random.choice(replies)


def check_condition(comment):
    """ Has the bot been called?"""
    paragraphs = [
        paragraph for paragraph in comment.body.split('\n')
        if not is_quote(paragraph)
    ]
    for paragraph in paragraphs:
        # Separate by paragraphs to avoid triggering by quoted text.
        for word in misspells:
            if check_misspells(paragraph, misspells[word]):
                return get_reply().format(word)


signature = (
    "\n\n Script by \/u/Sevg, hosting by \/u/DirkGentle"
    "*^and ^yes, ^weed ^is ^legal ^here*"
)
source = "\n\n [Source.](https://github.com/sevgit/Its_URUGUAY_bot)"
epilogue = "\n\n*****\n\n{}\n\n{}".format(signature, source)


print("RUNNING")
if __name__ == "__main__":
    while True:
        try:
            output_log("Starting the script")
            log = load_log(comment_log_path)
            reddit = praw.Reddit(
                client_id=botlogin.client_id,
                client_secret=botlogin.client_secret,
                password=botlogin.password,
                user_agent=(
                    "Its_URUGUAY_bot script by "
                    "Sevg/Dirkgentle/ElectrWeakHyprCharge"
                ),
                username=botlogin.username
            )
            print("Logged to reddit as {}".format(reddit.user.me().name))
            output_log("Logged to reddit as: {}".format(reddit.user.me().name))

            for comment in reddit.subreddit('all').stream.comments():
                reply = check_condition(comment)
                if reply and comment.id not in log:
                    comment.reply("{} {}".format(reply, epilogue))

                    output_log("{{{}}}".format(reply))
                    log.append(comment.id)
                    update_log(comment.id, comment_log_path)
        except Exception as exception:
            output_log(str(exception))
            output_log(traceback.format_exc())
