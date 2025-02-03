البته! در اینجا توضیحات به زبان Markdown برای درج در GitHub آمده است:

```markdown
# توضیحات برنامه کامپایلر ساده با استفاده از PLY

## وارد کردن بسته‌های مورد نیاز
```python
import ply.lex as lex
import ply.yacc as yacc
```
این خطوط بسته‌های `ply.lex` و `ply.yacc` را وارد می‌کنند که برای تحلیل لغوی و نحوی استفاده می‌شوند.

## تعریف توکن‌ها
```python
tokens = (
    'INT', 'STR', 'PRINT',
    'NUMBER', 'IDENTIFIER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS'
)
```
این لیست شامل نام توکن‌هایی است که در زبان برنامه‌نویسی ساده شما استفاده می‌شوند.

## قوانین برای توکن‌های ساده
```python
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
```
این خطوط قوانین عبارات منظم برای توکن‌های ساده مانند `+`, `-`, `*`, `/` و `=` را تعریف می‌کنند.

## تعریف قانون برای شناسه‌ها
```python
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'
```
این قانون شناسه‌ها را تعریف می‌کند که با یک حرف یا زیرخط شروع می‌شوند و می‌توانند شامل حروف، اعداد و زیرخط باشند.

## تعریف قانون برای اعداد
```python
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
```
این تابع اعداد را شناسایی کرده و مقدار آن‌ها را به عدد صحیح تبدیل می‌کند.

## تعریف قانون برای رشته‌ها
```python
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove the quotes
    return t
```
این تابع رشته‌ها را شناسایی کرده و نقل‌قول‌های اطراف آن‌ها را حذف می‌کند.

## تعریف قانون برای خطوط جدید
```python
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
```
این تابع خطوط جدید را شناسایی کرده و شماره خط را به‌روزرسانی می‌کند.

## تعریف کاراکترهای نادیده گرفته شده
```python
t_ignore = ' \t'
```
این خط کاراکترهای فاصله و تب را نادیده می‌گیرد.

## تعریف کلمات کلیدی
```python
keywords = {
    'int': 'INT',
    'str': 'STR',
    'print': 'PRINT'
}
```
این دیکشنری کلمات کلیدی را تعریف می‌کند.

## تعریف قانون برای شناسایی کلمات کلیدی
```python
def t_KEYWORD(t):
    r'\b(?:int|str|print)\b'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t
```
این تابع کلمات کلیدی را شناسایی کرده و نوع آن‌ها را تعیین می‌کند.

## قانون مدیریت خطاها
```python
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
```
این تابع کاراکترهای غیرقانونی را شناسایی کرده و آن‌ها را نادیده می‌گیرد.

## ساخت تحلیل‌گر لغوی
```python
lexer = lex.lex()
```
این خط تحلیل‌گر لغوی را می‌سازد.

## قوانین تجزیه

### دیکشنری برای ذخیره متغیرها
```python
variables = {}
```
این دیکشنری برای ذخیره متغیرها استفاده می‌شود.

### تعریف قوانین تجزیه
```python
def p_statement_list(p):
    '''statement_list : statement
                      | statement statement_list'''
```
این قانون لیستی از دستورات را تعریف می‌کند.

### تعریف قوانین برای اعلان متغیرها
```python
def p_statement_decl(p):
    '''statement : INT IDENTIFIER EQUALS expression
                 | STR IDENTIFIER EQUALS STRING'''
    if p[1] == 'int':
        variables[p[2]] = p[4]
    elif p[1] == 'str':
        variables[p[2]] = p[4]
```
این قانون اعلان متغیرهای `int` و `str` را تعریف می‌کند.

### تعریف قوانین برای تخصیص متغیرها
```python
def p_statement_assign(p):
    '''statement : IDENTIFIER EQUALS expression'''
    if p[1] in variables:
        variables[p[1]] = p[3]
    else:
        print(f"Undefined variable '{p[1]}'")
```
این قانون تخصیص مقادیر به متغیرها را تعریف می‌کند.

### تعریف قوانین برای چاپ مقادیر
```python
def p_statement_print(p):
    '''statement : PRINT expression'''
    print(p[2])
```
این قانون چاپ مقادیر را تعریف می‌کند.

### تعریف قوانین برای عملیات‌های دودویی
```python
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
```
این قانون عملیات‌های دودویی مانند جمع، تفریق، ضرب و تقسیم را تعریف می‌کند.

### تعریف قوانین برای گروه‌بندی عبارات
```python
def p_expression_group(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]
```
این قانون گروه‌بندی عبارات را تعریف می‌کند.

### تعریف قوانین برای اعداد
```python
def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]
```
این قانون اعداد را تعریف می‌کند.

### تعریف قوانین برای شناسه‌ها
```python
def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    if p[1] in variables:
        p[0] = variables[p[1]]
    else:
        print(f"Undefined variable '{p[1]}'")
        p[0] = 0
```
این قانون شناسه‌ها را تعریف می‌کند.

## قانون مدیریت خطاها
```python
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")
```
این قانون خطاهای نحوی را مدیریت می‌کند.

## ساخت تحلیل‌گر نحوی
```python
parser = yacc.yacc()
```
این خط تحلیل‌گر نحوی را می‌سازد.

## استفاده از برنامه
```python
if __name__ == '__main__':
    with open(input("Enter the filename: "), 'r') as file:
        data = file.read()

    # Parse the data
    parser.parse(data)
```
این بخش از برنامه فایل ورودی را می‌خواند و داده‌ها را تجزیه می‌کند.

امیدوارم این توضیحات مفید بوده باشد! اگر سوال دیگری دارید، بپرسید.
```
