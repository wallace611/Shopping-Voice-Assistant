import re
from .voice_helper import *
from collections import defaultdict

def execute_command(cmd, input_line, cart):
    if cmd == '%close%':
        say("好挖再見")
        exit()
        
    elif cmd == '%call%':
        say("叫我幹啥勒")
        
    elif cmd == '%swear%':
        say("很兇喔老哥")
        
    elif cmd == '%add_to_cart%':
        say("加入物品")
        info = add_2_cart(input_line)
        try:
            item_name, quantity, price = info
            info = cart.add_item(item_name, price, quantity)
            if info is not None:
                say(info)
            else:
                say("加入{}個{}元的{}".format(quantity, price, item_name))
                say("目前總價為{}元".format(cart.sum_price()))
        except:
            say(info)
        
    elif cmd == '%remove_from_cart%':
        say("移除物品")
        product_name = get_product_name(input_line)
        if product_name == None:
            say("輸入格式不正確")
        else:
            try:
                cart.remove_item(product_name)
                say("移除" + product_name)
                say("目前總價為{}元".format(cart.sum_price()))
            except:
                say("購物車中無" + product_name)
        
    elif cmd == '%sum_price%':
        say("商品價錢總和")
        price = cart.sum_price()
        say("一共{}元".format(price))
        
    elif cmd == '%clear_cart%':
        say("清空購物車")
        cart.clear()
        say("購物車空了")
        
    elif cmd == '%discount%':
        say("設定折扣")
        number = find_number(input_line)
        if len(number) == 1:
            cart.set_discount(discount_to_float(int(number[0])))
            say("{}折".format(number[0]))
        else:
            say("格式錯誤，取消折扣")
            cart.set_discount(1)
            
    elif cmd == '%get_info%':
        name = get_product_name(input_line)
        if name == None:
            say("輸入字串中無商品名稱")
        elif name not in cart.get_all():
            say("購物車中無"+name)
        else:
            price = 0
            for item in cart.get_item(name):
                price += item[0]*item[1]
            say("{}花了{}元".format(name, price))
        
    elif cmd == '%final_price%':
        say("折扣後價格")
        price = cart.final_price()
        say("{}元".format(round(price, 0)))
        
    elif cmd == '%set_budget%':
        say("設定預算")
        number = find_number(input_line)
        if len(number) == 1:
            info = cart.set_budget(int(number[0]))
            if info is not None:
                say(info)
            else:
                say("預算設為{}".format(number[0]))
        else:
            say("格式不正確，輸入只能有一個數字")
        
    elif cmd == '%list_commodity%':
        say("列出購物車內商品")
        if len(cart.get_all()) == 0:
            say("購物車為空")
            return
        for items in cart.get_all().items():
            print(items[0])
            for price in items[1].items():
                print("{}元: {}個".format(price[0], price[1]))
        
    else:
        say("我聽不懂謝謝")

def chinese_to_number(sentence):
    
    digit = {'一': 1, '二': 2,'兩':2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    
    def _trans(s):
        num = 0
        if s:
            idx_q, idx_b, idx_s = s.find('千'), s.find('百'), s.find('十')
            if idx_q != -1:
                num += digit[s[idx_q - 1:idx_q]] * 1000
            if idx_b != -1:
                num += digit[s[idx_b - 1:idx_b]] * 100
            if idx_s != -1:
                num += digit.get(s[idx_s - 1:idx_s], 1) * 10
            if s[-1] in digit:
                num += digit[s[-1]]
        return num
    
    def trans(chn):
        chn = chn.replace('零', '')
        idx_y, idx_w = chn.rfind('億'), chn.rfind('萬')
        if idx_w < idx_y:
            idx_w = -1
        num_y, num_w = 100000000, 10000
        if idx_y != -1 and idx_w != -1:
            return trans(chn[:idx_y]) * num_y + _trans(chn[idx_y + 1:idx_w]) * num_w + _trans(chn[idx_w + 1:])
        elif idx_y != -1:
            return trans(chn[:idx_y]) * num_y + _trans(chn[idx_y + 1:])
        elif idx_w != -1:
            return _trans(chn[:idx_w]) * num_w + _trans(chn[idx_w + 1:])
        return _trans(chn)
    
    pattern = re.compile(r'[一二兩三四五六七八九十百千萬億]+')
    matches = pattern.findall(sentence)
    for match in matches:
        sentence = sentence.replace(match, str(trans(match)))
    return sentence

def get_product_name(sentence):
    match = re.search(r'(我不想要那個|我不要|購物車中移除那個|購物車中移除|刪除|移除)([\u4e00-\u4e85\u4e87-\u9fa5]+)', sentence)
    if match:
        return match.group(2)
    match = re.search(r'(知道|目前|需要知道)([\u4e00-\u9fa5]+)(的價格|占多少錢)', sentence)
    if match:
        return match.group(2)
    match = re.search(r'告訴我?([\u4e00-\u9fa5]+)(總共花了多少錢|花了多少錢|的價格|一共花了多少錢)', sentence)
    if match:
        return match.group(1)
    match = re.search(r'([\u4e00-\u9fa5]+)(總共花了多少錢|花了多少錢|的價格|一共花了多少錢)', sentence)
    if match:
        return match.group(1)
    match = re.search(r'(我買了多少錢)([\u4e00-\u9fa5]+)', sentence)
    if match:
        return match.group(2)
    match = re.search(r'(將一個新的|把這個|把)([\u4e00-\u9fa5]+)(加入|放入|移除|新增)(購物車)', sentence)
    if match:
        return match.group(2)
    return None

def add_2_cart(input_line):
    pattern = re.compile(r'(將|加入|放入|新增)(\d+)(\w)(\d+)元的(.+)')

    match = pattern.match(input_line)

    if match:
        try:
            quantity = int(match.group(2))
            price = int(match.group(4))  # 新增價格的捕獲組
            item_name = match.group(5).strip()  # 移除前後空格
            return item_name, quantity, price
        except ValueError:
            return "數量或價格格式不正確，請輸入正確的數量和價格。"
    else:
        return "輸入格式不正確，请使用 '加入[數量][量詞][價格]元的[商品名稱]' 的格式。"
    
def find_number(input_line):
    numbers = re.findall(r'\d+', input_line)
    return numbers
    
def discount_to_float(discount):
    try:
        if discount < 10 and discount > 0:
            return discount/10
        elif discount > 10 and discount < 100:
            return (discount//10)/10 + discount%10 / 100
        else:
            return 1.0
    except KeyError:
        return 1.0
    
class shopping_cart:
    def __init__(self) -> None:
        self.cart = defaultdict(lambda: defaultdict(int)) # cart[name] = {quantity: price}
        self.sumPrice = 0
        self.budget = 0
        self.discount = 1.0
        
    def add_item(self, name, price, quantity):
        if self.sumPrice + price*quantity > self.budget and self.budget != 0:
            return "超過預算:{}".format(self.budget)
        self.cart[name][price] += quantity
        self.sumPrice += price*quantity
        
    def remove_item(self, name):
        price = 0
        if name not in self.cart.keys():
            raise KeyError
        for items in self.cart[name].items():
            price += items[0] * items[1]
        del self.cart[name]
        self.sumPrice -= price
    
    def get_all(self):
        return self.cart
    
    def get_item(self, name):
        return self.cart[name].items()

    def clear(self):
        self.cart.clear()
        
    def sum_price(self):
        return self.sumPrice
    
    def set_discount(self, val):
        self.discount = val
        
    def final_price(self):
        return self.sumPrice * self.discount
    
    def set_budget(self, val):
        if self.sumPrice > val and val != 0:
            return "目前金額大於設定預算"
        self.budget = val