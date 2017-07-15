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
def rapi_comments(username, limit=25, after=""):
    return "https://www.reddit.com/user/" + username + "/comments.json?limit=" + str(limit)

def rapi_submitted(username, limit=25, after=""):
    return "https://www.reddit.com/user/" + username + "/submitted.json?limit=" + str(limit)

def rapi_about(username):
    return "https://www.reddit.com/user/" + username  + "/about.json"


### Convenience methods to use with Reddit API

def get_all_comments(username, limit=25, after=""):
    if(limit <= 100): 
        json = get_json_response(rapi_comments(username, limit, after))
        return json["data"]["children"]
    else:
        json = get_json_response(rapi_comments(username, 100, after))
        comments = json["data"]["children"]
        new_after = get_comment(comments, len(comments) - 1)["name"]
        return comments + get_all_comments(username, limit - 100, new_after)

def get_all_posts(username, limit=25, after=""):
    if(limit <= 100): 
        json = get_json_response(rapi_submitted(username, limit, after))
        return json["data"]["children"]
    else: 
        json = get_json_response(rapi_submitted(username, 100, after))
        submitted = json["data"]["children"]
        new_after = get_post(submitted, len(submitted) - 1)["name"]
        return submitted + get_all_posts(username, limit - 100, new_after)

#def get_all_posts(username, limit=25):
#    json = get_json_response(rapi_submitted(username, limit))
#    return json["data"]["children"]

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
## Item: Either a comment or a post

def vt_relevant_items(items, relevance_set):
    return list(filter(lambda x: x["data"]["subreddit"] in relevance_set, items))

def vt_extract_comments(items):
    return list(filter(lambda x: x["data"]["name"][:2] == "t1", items))

def vt_extract_posts(items):
    return list(filter(lambda x: x["data"]["name"][:2] == "t3", items))

def main():
    html = get_html("https://www.quora.com/What-subreddits-should-a-software-engineer-follow")
    sub_list = get_subreddits(html)

    sub_list.add("archlinux")
    print(sub_list)

    comments = get_all_comments("wadawalnut", 300)
    posts = get_all_posts("wadawalnut", 300)

    items = vt_relevant_items(comments + posts, sub_list)
    print("Retrieved " + str(len(items)) + " from wadawalnut")
    cmt = vt_extract_comments(items)
    pst = vt_extract_posts(items)
    print("\t Of which " + str(len(cmt)) + " are comments and " + str(len(pst)) + " are posts.")
    for i in range(0,2):
        print ("COMMENT\n==========")
        print(comments[i]["data"]["body"])
        print ()
    wada_about = get_json_response(rapi_about("wadawalnut"))
    print("wadawalnut's link karma: " + str(get_linkkarma(wada_about)))
    print("wadawalnut's comment karma: " + str(get_commentkarma(wada_about)))

if __name__ == '__main__':
    main()
