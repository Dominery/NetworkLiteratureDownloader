import os
import re


class TextExporter:
    format = '.txt'
    illegal_char = {'\\':'、','/':'、','|':'l',':':'：','?':'？','<':'《','>':'》','*':'x'}

    def export(self,article,filepath):
        if article.title:
            title = self._legalize_filename(article.title)
            path = os.path.join(filepath,title+self.format)
            with open(path,'w',encoding='utf-8')as f:
                f.write(article.content)

    def _legalize_filename(self,title):
        for illegal,change in self.illegal_char.items():
            title = title.replace(illegal,change)
        return title