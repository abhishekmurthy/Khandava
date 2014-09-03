#!/usr/bin/python
from class_summary import Summarize
from class_get_tweets import TweetRepo
import os

def main(fo,args):

    repo = TweetRepo()
    if args.search:
        text = fo.read()
        summary = Summarize()
        frequency_dictionary = summary.summarize(text)
        all_keywords_weight = summary.assign_weights_to_all_keywords(frequency_dictionary)
        tweets_weight = summary.assign_weight_to_tweets(all_keywords_weight)
        summary.pick_most_eligible_tweet(tweets_weight)
        #repo.search_relevant_tweets(keywords,limit=15)
    elif args.gather:
        repo.set_region('india')
        repo.write_tweets_to_file(fo)

if __name__ == '__main__':
    import sys
    from argparse import ArgumentParser

    argv =  sys.argv
    parser = ArgumentParser(description='The Khandava Project')
    parser.add_argument('-g','--gather', action='store_true',default=False,
        help='gather tweets to a file')
    parser.add_argument('-s','--search', action='store_true',default=False,
        help='search for relevant tweets from a file')
    parser.add_argument('file', nargs='?',
        help='file to summarize (stdin will be used otherwise)')
    args = parser.parse_args(argv[1:])

    if args.file:
        if args.file == '-':
            fo = sys.stdin
        else:
            if args.search:
                try:
                    fo = open(args.file)
                except IOError as err:
                    raise SystemExit('error: cannot open {}: {}'.format(
                        args.file, err))
            elif args.gather:
                if os.path.isfile(args.file):
                    print "%s exists...  Removing file" %args.file
                    os.remove(args.file)
                try:
                    fo = open(args.file,'w')
                except IOError as err:
                    raise SystemExit('error: cannot open {}: {}'.format(
                        args.file, err))
    else:
        fo = sys.stdin
    main(fo,args)

