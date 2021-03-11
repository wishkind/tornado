from fontTools.ttLib import TTFont
import os


def modify_html(html, new_font=None):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '20ad699b.woff')
    new_font = TTFont(path)
    base_font = TTFont(path)
    uni_list = new_font['cmap'].tables[0].ttFont.getGlyphOrder()
    num_list = []
    base_num_list = ['3', '5', '8', '7', '0', '1', '9', '6', '2', '4']
    base_uni_code = ['uniF64E', 'uniF345', 'uniE8F8', 'uniEB4E', 'uniE261', 'uniECAE',
                   'uniE738', 'uniE492', 'uniE979', 'uniEB3D']
    for i in range(1, 12):
        new_glyph = new_font['glyf'][uni_list[i]]
        for j in range(10):
            base_glyph = base_font['glyf'][base_uni_code[j]]
            if new_glyph == base_glyph:
                num_list.append(base_num_list[j])
                break
    row_ist = []
    for i in uni_list[2:]:
        i = i.replace('uni', '&#x').lower()
        row_ist.append(i)
    dictory = dict(zip(row_ist, num_list))
    for key in dictory:
        if key in str(html):
            html = html.replace(key, str(dictory[key]))
    return html


if __name__ == '__main__':
    new_font = TTFont(r'E:\PythonProject\practice\meituan\FILES\20ad699b.woff')
    a = modify_html(''.join("&#xecae;&#xeb4e;:&#xe261;&#xe261;-&#xe979;&#xe979;:&#xf345;&#xf345;".split(';')), new_font)
    print(a)

