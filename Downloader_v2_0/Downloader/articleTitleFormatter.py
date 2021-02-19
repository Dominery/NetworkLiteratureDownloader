import re


class ArticleTitleFormatter:
    def format(self,raw_title):
        return self._set_order(raw_title)

    def _set_order(self, raw_title):
        num_string = '零一二三四五六七八九十百千'
        result = re.search(r"第([%s]*?)章" % num_string, raw_title)
        if result:
            num_list = [*result.group(1)]
            set_list = ['0', '0', '0', '0']
            if re.search('["十百千"]', result.group(1)):
                dict = {'百': 1, '千': 0, '十': 2}
                for i in range(len(num_list)):
                    if num_list[i] in dict.keys():
                        if i == 0:  # format the num range form ten to twenty
                            set_list[dict[num_list[i]]] = '1'
                        else:
                            set_list[dict[num_list[i]]] = str(num_string.index(num_list[i - 1]))
                if num_list[-1] not in dict.keys():  # format the num like '六百零一'
                    set_list[3] = str(num_string.index(num_list[-1]))
            else:
                # to format the title which doesn't have characters like '十百千'
                num_list.reverse()  # process the situation that the num doesn't have thousand position
                for i in range(len(num_list)):
                    set_list[3 - i] = str(num_string.index(num_list[i]))
            return raw_title.replace(result[1], ''.join(set_list))
        else:
            return raw_title