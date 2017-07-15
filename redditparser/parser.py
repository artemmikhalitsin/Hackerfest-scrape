import httplib2
import json
import re
import urllib
import urllib.request

# Regex filters
subreddit_retriever = re.compile('\/r\/\\S+')
subreddit_retriever_alt = re.compile('\/r\/[a-zA-Z0-9]+')

def get_html(url):
    f = urllib.request.urlopen(url)
    return f.read().decode('utf-8')

def get_subreddits(html):
    return list(map(lambda x: x.lower(), subreddit_retriever_alt.findall(html)))

def get_json_response(url):
    resp, content = httplib2.Http().request(url)
    return json.loads(content)

#Reddit API methods
def rapi_comments(username, limit=25):
    url = "https://www.reddit.com/user/" + username + "/comments.json?limit=" + str(limit)
#    print(url)
    return url

def rapi_about(username):
    return "https://www.reddit.com/user/" + username  + "/about.json"


### Convenience methods to use with Reddit API

# Get overall link karma from user
def get_link_karma(user_about):
    return user_about["data"]["link_karma"]

# Get overall comment karma from user
def get_comment_karma(user_about):
    return user_about["data"]["comment_karma"]

# Get comment from comment list
def get_comment(comments, index):
    return comments["data"]["children"][index]["data"]

# Get a tuple representing (upvotes, downvotes) of a particular comment
def get_comment_updown(comment):
    return (comment["ups"], comment["downs"])

def main():
    html = get_html("https://www.quora.com/What-subreddits-should-a-software-engineer-follow")
    sub_list = get_subreddits(html)
    for i in range(0,len(sub_list)):
        print(sub_list[i])

    comments = get_json_response(rapi_comments("wadawalnut", 100))
    commentone = get_comment(comments, 1)
    print(commentone["body"])
    print("Above comment's updown: " + str(get_comment_updown(commentone)))
    wada_about = get_json_response(rapi_about("wadawalnut"))
    print("wadawalnut's link karma: " + str(get_link_karma(wada_about)))
    print("wadawalnut's comment karma: " + str(get_comment_karma(wada_about)))

if __name__ == '__main__':
    main()
