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
    return set(list(map(lambda x: x.lower()[3:], subreddit_retriever_alt.findall(html))))

def get_json_response(url):
    resp, content = httplib2.Http().request(url)
    return json.loads(content)

#Reddit API methods
def rapi_comments(username, limit=25):
    return "https://www.reddit.com/user/" + username + "/comments.json?limit=" + str(limit)

def rapi_submitted(username, limit=25):
    return "https://www.reddit.com/user/" + username + "/submitted.json?limit=" + str(limit)

def rapi_about(username):
    return "https://www.reddit.com/user/" + username  + "/about.json"


### Convenience methods to use with Reddit API

def get_all_comments(username, limit=25):
    json = get_json_response(rapi_comments(username, limit))
    return json["data"]["children"]

def get_all_posts(username, limit=25):
    json = get_json_response(rapi_submitted(username, limit))
    return json["data"]["children"]

# Get overall link karma from user
def get_linkkarma(user_about):
    return user_about["data"]["link_karma"]

# Get overall comment karma from user
def get_commentkarma(user_about):
    return user_about["data"]["comment_karma"]

# Get comment from comment list
def get_comment(comments, index):
    return comments[index]["data"]

# Get a tuple representing (upvotes, downvotes) of a particular comment
def get_comment_updown(comment):
    return (comment["ups"], comment["downs"])

# Get post from list of posts
def get_post(submitted, index):
    return submitted[index]["data"]

# Get a tuple representing (upvotes, downvotes) of a particular post
def get_post_updown(post):
    return (post["ups"], post["downs"])


### Vitae functions

def vt_relevant_items(items, relevance_set):
    return list(filter(lambda x: x["data"]["subreddit"] in relevance_set, items))

def main():
    html = get_html("https://www.quora.com/What-subreddits-should-a-software-engineer-follow")
    sub_list = get_subreddits(html)
#    for i in range(0,len(sub_list)):
#        print(sub_list[i])

    sub_list.add("archlinux")
    print(sub_list)

    comments = vt_relevant_items(get_all_comments("wadawalnut", 100),sub_list)
    for i in range(0,2):
        print(comments[i]["data"]["body"])
#    commentone = get_comment(comments, 1)
#    print(commentone["body"])
#    print("Above comment's updown: " + str(get_comment_updown(commentone)))
    wada_about = get_json_response(rapi_about("wadawalnut"))
    print("wadawalnut's link karma: " + str(get_linkkarma(wada_about)))
    print("wadawalnut's comment karma: " + str(get_commentkarma(wada_about)))

if __name__ == '__main__':
    main()
