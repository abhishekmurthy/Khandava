from collections import defaultdict
import re
import operator

import urllib
import urllib2
import json


class Summarize:

    MAX_SUMMARY_SIZE = 300

    filter = { 'a':1, 'an':1, 'the':1, 'aboard':1, 'about':1, 'above':1, 'across':1, 'after':1, 'along':1, 'amid':1, 'among':1, 'around':1, 'as':1, 'at':1, 'before':1, 'behind':1, 'below':1, 'beneath':1, 'because':1, 'beside':1, 'besides':1, 'between':1, 'beyond':1, 'but':1, 'by':1, 'so':1, 'during':1, 'don\'t':1, 'for':1, 'from':1, 'in':1, 'into':1, 'of':1, 'to':1, 'with':1,  'when':1, 'my':1, 'and':1, 'i':1, 'you':1, 'u':1, 'is':1, 'this':1, 'their':1, 'your':1, 'our':1, 'ur':1, 'too':1, 'but':1, 'then':1, 'her':1, 'him':1, 'ji':1, 'out':1, 'that':1, 'if':1, 'are':1, 'we':1, 'be':1, 'many':1, 'on':1, 'was':1, 'it':1, 'also':1, 'please':1, 'plz':1, 'yes':1, 'no':1, 'they':1, 'now':1, 'them':1, 'yeah':1, 'cute':1, 'i\'m':1, '&amp;':1, 'me':1, 'how':1, 'us':1 }

    tweets = [] #Place-holder for all tweets

    def tokenize(self, text):
        '''Very simple white space tokenizer, in real life we'll be much more
        fancy.
        '''
        return text.split()


    def split_to_sentences(self, text):
        '''Very simple spliting to sentences by [.!?] and paragraphs.
        In real life we'll be much more fancy.
        '''
        sentences = []
        start = 0

        # We use finditer and not split since we want to keep the end
        for match in re.finditer('(\s*[.!?]\s*)|(\n{2,})', text):
            sentences.append(text[start:match.end()].strip())
            start = match.end()

        if start < len(text):
            sentences.append(text[start:].strip())

        return sentences


    def get_full_url(self, short_url):
        '''Converts a t.co url to the full url
        '''
   
        data = {}
        data['url'] = short_url
        data_values = urllib.urlencode(data)
        base_url = "http://expandurl.appspot.com/expand"
        full_url = base_url + '?' + data_values
        resp = urllib2.urlopen(full_url).read()
        json_resp = json.loads(resp)
        return json_resp['end_url']

    def token_frequency(self, text):
        '''Return frequency (count) for each token in the text
        if not a hashtag and not a preposition
        '''
        text = unicode(text, 'ascii', 'ignore')
        frequencies = defaultdict(int)
        for token in self.tokenize(text):
            if token.isalnum() and not any (s in token for s in ('#', '@')):
                '''
                if token.startswith("http://t.co"):
                    token = get_full_url(token)
                '''
                if self.filter.get(token.lower()) is None:
                    frequencies[token.lower()] += 1

        return frequencies


    def sentence_score(self, sentence, frequencies):
        return sum((frequencies[token] for token in tokenize(sentence)))


    def create_summary(self, sentences, max_length):
        summary = []
        size = 0
        for sentence in sentences:
            summary.append(sentence)
            size += len(sentence)
            if size >= max_length:
                break

        summary = summary[:max_length]
        return '\n'.join(summary)


    def summarize(self, text, max_summary_size=MAX_SUMMARY_SIZE):
        frequencies = self.token_frequency(text)
        '''
        sentences = split_to_sentences(text)
        sentences.sort(key=lambda s: sentence_score(s, frequencies), reverse=1)
        summary = create_summary(sentences, max_summary_size)
        return summary
        '''
        sorted_frequencies = sorted(frequencies.iteritems(), key=operator.itemgetter(1), reverse=True)
        for item in sorted_frequencies:
            print item
        return sorted_frequencies

    def assign_weights_to_all_keywords(self,keywords):
        #search_string = ""
        weights_sum = 0
        keywords_weight = {}
        for keyword in keywords:
            #search_string = search_string + " " + keywords[i][0]
            weights_sum += keyword[1]
        for i in range(len(keywords)):
            keywords_weight[keywords[i][0]] = (float(keywords[i][1]) / weights_sum)
        return keywords_weight

    def assign_weight_to_tweets(self, keywords_weight):
        tweets_weight = []  # tweets_weight = Placeholder for weight of corresponding tweet
        '''
        lines = open('sample.txt').read().splitlines()
        for line in lines:
            if len(line) is not 0:
                text = unicode(line, 'ascii', 'ignore')
                self.tweets.append(text)
        '''
        file_dump = open('sample.txt').read()
        all_tweets = file_dump.split('%%')
        for t in all_tweets:
            text = unicode(t, 'ascii', 'ignore')
            self.tweets.append(text)
        for (i,tweet) in enumerate(self.tweets):
            tweets_weight.append(0)
            for word in self.tokenize(tweet):
                if keywords_weight.get(word.lower()) is not None:
                    tweets_weight[i] += keywords_weight[word.lower()]
               # tweets_weight[i] /= len(self.tokenize(tweet)) #Dividing total weight of tweet by no. of words
        return tweets_weight

    def pick_most_eligible_tweet(self, tweets_weight):
        ind =  tweets_weight.index(max(tweets_weight))
        print "\nMost Eligible Tweet :\n"
        print self.tweets[ind]

    def __init__(self):
        pass

if __name__ == '__main__':
    import sys
    from argparse import ArgumentParser

    argv =  sys.argv

    parser = ArgumentParser(description='Summarize text')
    parser.add_argument('file', nargs='?',
        help='file to summarize (stdin will be used otherwise)')
    parser.add_argument('-s', '--size', help='Size of summary',
                        default=300, type=int)
    parser.add_argument('--test', help='test', action='store_true',
                        default=False)
    args = parser.parse_args(argv[1:])

    if args.file:
        if args.file == '-':
            fo = sys.stdin
        else:
            try:
                fo = open(args.file)
            except IOError as err:
                raise SystemExit('error: cannot open {}: {}'.format(
                    args.file, err))
    else:
        fo = sys.stdin 
    text = fo.read()
    Summarize(text,args)
