# Replace first keyword in post with its link, given a list of keywords and links in a file
import re
from BeautifulSoup import BeautifulSoup
import blogofile_bf as bf

config = {"name": "Linkify",
          "description": "Linkify blog post based on a file with a list of link",
          "author": "Paolo Corti",
}

def linkify(text, word_dic):
    """
    take a html text and replace words that match a key in a dictionary with
    the associated value, return the changed text.
    Filter should be run after markup filter and syntax hightlight filter
    """

    VALID_TAGS = ['p', 'li']

    def translate(match):
        key = match.group(0)
        value = word_dic[key.lower()]
        # only first keyword must be linkified
        if key in linkified_words:
            return key
        else:
            linkified_words.append(key)
            return value

    list_dict = map(re.escape, word_dic)
    list_dict2 = ['\\b%s\\b' % x for x in list_dict]
    re_str = '|'.join(list_dict2)
    rc = re.compile(re_str, re.IGNORECASE)
    soup = BeautifulSoup(text)
    textNodes = soup.findAll(text=True)

    linkified_words = []
    for textNode in textNodes:
        parent = textNode.findParent()
        if parent.name in VALID_TAGS:
            urlifiedtext = rc.sub(translate, textNode)
            textNode.replaceWith(urlifiedtext)
    return soup.renderContents()

def run(content):
    """
    Read links and create dictionary, then linkify post content
    """
    path_seo_links=bf.config.filters.linkify.seo_links
    seo_links = open(path_seo_links, 'r').read().split("\n")
    lst=[]
    for l in seo_links:
        if l.find(',')>0:
            sl=l.split(",")
            lst.append((sl[0].lower(), '<a href="%s">%s</a>' % (sl[1], sl[0])))
    seo_dict=dict(lst)

    return linkify(content, seo_dict)
