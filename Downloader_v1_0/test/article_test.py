import unittest

from Downloader_v1_0.articleurls import ArticleUrls


class ArticleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.article = ArticleUrls('1')

    def test_get_book_info(self):
        html_str = """
         <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml;charset=utf-8" />
    <title>搜索小说_笔趣阁</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no" />
    <meta name="format-detection" content="telephone=no" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <link rel="stylesheet" href="/css/reset.css" />
    <link rel="stylesheet" href="/css/index.css" />
    <style>.tips{border:1px solid #C0DEEA;margin:10px;padding:10px;color:red}</style>
    <script src="/js/wap.js"></script>
</head>
<body>
    <strong></strong>
    <header class="channelHeader">
<a class="iconback" href="/"><img src="images/header-back.gif" alt="返回"/></a>
搜索小说
<a class="iconhome" href="/"><img src="images/header-backhome.gif" alt="首页"/></a>
</header>
<!--<script>_17mb_top()</script>-->
    <div class="recommend mybook">
    <div class="tips"></div>
	    <div class="hot_sale "><span class="num num1">1</span><a href="/4_4074/"><p class="title">牧神记</p><p class="author">玄幻小说 | 作者：宅猪</p><p class="author">连载 | 更新：新书，《临渊行》已经上传</p></a></div>
	</div>
    <script language="javascript" type="text/javascript" src="/js/zepto.min.js"></script>
    <script language="javascript" type="text/javascript" src="/js/common.js"></script>
    <!--<script>_17mb_bottom();_17mb_xuanfu();</script>-->
<form name="articlesearch" class="searchForm" method="post" action="/s.php">  
    <input type="text" name="keyword" class="searchForm_input searchForm_input2" placeholder="输入书名或作者,请您少字也别错字。" />
    <input type="hidden" name="t" value="1" />
    <input type="submit" class="searchForm_btn" value="搜索" />
</form>

<p class="note">
</p>
<footer>
    <a href="#top"><img src="/images/icon-backtop.gif" title="↑" alt="↑"/></a>
    <p class="version channel">
    <a href="/">首页</a>
    <a href="/mybook.php" >书架</a>
    <a href="/newcase.html" >阅读记录</a>
    <script type="text/javascript" src="https://s4.cnzz.com/z_stat.php?id=1278827600&web_id=1278827600"></script>
    </p>


</footer>
</body>
</html>
        """
        self.article.get_book_info(html_str)
        print(self.article.book_url)
        self.assertEqual(bool(self.article.book_url),True)



if __name__ == '__main__':
    unittest.main()
