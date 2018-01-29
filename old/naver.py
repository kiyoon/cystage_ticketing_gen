# http://developc.tistory.com/entry/Python-%EB%84%A4%EC%9D%B4%EB%B2%84-%EB%B8%94%EB%A1%9C%EA%B7%B8-%EA%B8%80%EC%93%B0%EA%B8%B0
# http://myinformation.tistory.com/entry/MetaWeblog-API-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0
import xmlrpc.client
 
API_URL = 'https://api.blog.naver.com/xmlrpc'
 
 
class NaverBlog(object):
    def __init__(self, user_id, api_key):
        self.__server = None
        self.__user_id = user_id
        self.__api_key = api_key
        self.__categories = []
 
        try:
            self.__set_categories()
        except Exception as e:
            raise e
 
    def __client(self):
        if self.__server is None:
            self.__server = xmlrpc.client.ServerProxy(API_URL)
 
        return self.__server
 
    def __set_categories(self):
        categories = self.__client().metaWeblog.getCategories(self.__user_id,
                                                              self.__user_id,
                                                              self.__api_key)
 
        for category in categories:
            self.__categories.append(category['title'])
 
    def new_post(self, title, description, category, publish=True):
        struct = {}
        struct['title'] = title
        struct['description'] = description
        if category in self.__categories:
            struct['categories'] = [category]
 
        try:
            return self.__client().metaWeblog.newPost(self.__user_id,
                                                      self.__user_id,
                                                      self.__api_key,
                                                      struct,
                                                      publish)
        except Exception as e:
            raise e

    def new_post_struct(self, struct, publish=True):
        try:
            return self.__client().metaWeblog.newPost(self.__user_id,
                                                      self.__user_id,
                                                      self.__api_key,
                                                      struct,
                                                      publish)
        except Exception as e:
            raise e

    def get_post(self, postid):
        #print(self.__client().metaWeblog.getPost.callable())
        #print(inspect.getsourcelines(self.__client().metaWeblog.getPost))
        try:
            return self.__client().metaWeblog.getPost(#self.__user_id,
				                                      postid,
                                                      self.__user_id,
                                                      self.__api_key
                                                      )
        except Exception as e:
            raise e
 
if __name__ == '__main__':
    naver = NaverBlog('cystage2017', token)
    #postid = naver.new_post('테스트 제목', '<h1>테스트 글쓰기</h1>', '공연알리미 ALARM')
    postid = '221195379424'
    struct = naver.get_post(postid)
    struct['description'] = 'asdf'
    naver.new_post_struct(struct)
