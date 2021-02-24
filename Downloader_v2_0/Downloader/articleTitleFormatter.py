import re


class ArticleTitleFormatter:

    def __init__(self,padding_number):
        self.padding_number = padding_number

    def format(self,raw_title):
        return self._set_order(raw_title)

    def _set_order(self, raw_title):
        num_string = '零一二三四五六七八九十百千'
        result = re.search(r"第([%s]*?)章" % num_string, raw_title)
        if result:
            num_list = [*result.group(1)]
            numeral = '十百千'
            if re.search('[%s]'%numeral, result.group(1)):
                chapter = 0
                mark = 1
                for i in num_list:  # match the number before numeral
                    if i in numeral:
                        chapter += mark * pow(10,numeral.index(i)+1)
                        mark = 1
                    else:
                        mark = num_string.index(i)
                if num_list[-1] not in numeral:
                    chapter += num_string.index(num_list[-1])
                chapter = str(chapter)
            else:
                # to format the title which doesn't have characters like '十百千'
                chapter = ''
                for i in num_list:
                    chapter += str(num_string.index(i))
            chapter = chapter.rjust(self.padding_number,'0')
            return raw_title.replace(result[1],chapter)
        else:
            return raw_title