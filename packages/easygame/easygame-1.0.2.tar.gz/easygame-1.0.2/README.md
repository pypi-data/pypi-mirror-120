# 环境
- `easygame`需要python3.6及以上的python版本，最好的使用版本为python3.8。
- `easygame`不需要联网。
- `easygame`需要pygame2.0.1及以上的pygame版本，最好的使用版本为pygame2.0.1。
- `easygame`适用于Windows、MacOS、Linux。不同的操作系统，窗口样式会不同。非Windows系统下剪贴板功能可能有误。
# 下载
使用pip下载:
```shell script
pip install easygame -i https://pypi.org/project
```
使用easy-install下载:
```shell script
easy-install easygame -i https://pypi.org/project
```
# 示例
`easygame`使用pygame为基础类。
对比:<br>
在`pygame`中显示**hello world**:
```python
import pygame as pg
import sys


def destroy():
    pg.quit()
    sys.exit(0)


pg.init()
pg.font.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption('hello world')
font = pg.font.Font(None, 50)
clock = pg.time.Clock()
fps = 60
while True:
    clock.tick(fps)
    text_surface = font.render('hello world', True, (0, 0, 0))
    screen.blit(text_surface, screen.get_rect().center)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            destroy()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                destroy()
    pg.display.update()
    
```
而使用`easygame`:
```python
import easygame as eg
window = eg.window()
text = eg.Text(window, 'Hello World!', size=50,
               position=window.rectangle.center)
text.pack()
window.mainloop()
```
------
`easygame`的另一个优点是与`tkinter`很相似。
`easygame`对于学习过Scratch的小朋友很适用。
# 文档
## 素材安装
使用如下命令安装`mblock`的图片素材(需要在WIFI环境下，并要等待):
```shell script
python -m easygame.installer install
```
使用如下命令卸载`mblock`的图片素材:
```shell script
python -m easygame.installer uninstall
```
安装后使用如下代码获取一个资源:
```python
import easygame as eg
path = eg.get_downloaded_image('Airplane15.svg')
# path = "downloads/Airplane15.svg"
```
## 窗口
使用`easygame.window`创建一个窗口对象：
```python
import easygame as eg
window = eg.window()
```
`eg.window`的参数:
```python
window(
    title='easygame.screen',  # 窗口标题, str
    size=(800, 800),   # 窗口大小, Tuple[int, int]
    full_screen=False,   # 是否全屏, bool
    fps=70,  # 每秒帧率, int
    depth=0,   # 位深, int
    display=0,   # 媒体, int
    vsync=0,   # 同步, int
    icon=None,   # 窗口图标路径，支持png、jpg等等，str
    icon_title='game',  # 图标标题, str
    bgcolor=(255, 255, 255)  # 背景色, Tuple[int, int, int]
)
```
*(`easygame`是白色主题的)*<br>
由于`easygame`使用`pygame`编写，它对`pygame`有很好的兼容性。
```python
import easygame as eg
window = eg.window()
surface = window.get_surface()  # 通过get_surface方法获得pygame.Surface的窗口对象
```
`window`有一个组件队列`window.widgets`，在前面的Widget可能被后面的遮挡(Background类永远置于底层)
在0项的组件置于底层，在最后一项的组件置于顶层。
```python
import easygame as eg
window = eg.window()
widget = eg.Widget(window)
widgets = window.widgets  # 获取组件队列(list)
widgets_deque = window.widget_queue  # 获取组件队列(collections.deque)
window.add_widget(widget)  # 添加一个组件，必须为easygame.Widget类或其子类
window.delete_widget(widget)  # 删除一个组件，必须为easygame.Widget类或其子类，从底层开始匹配
window.random_widget()  # 获取随机组件
window.move_widget_to(widget, 0)  # 改变组件图层关系，将组件移动至某层
```
`window`有如下标题方法:
```python
import easygame as eg
window = eg.window()
title = window.get_title()  # 获取窗口标题
window.set_title('new title', 'new icon-title')  # 重设窗口标题
```
`window`有如下pygame方法:
```python
import easygame as eg
window = eg.window()
window.init()  # 初始化pygame，多次调用安全。在环境变量中"EASY_GAME_INIT"不为空的情况下将自动初始化
window.quit(0)  # 退出pygame和python程序,0为退出状态码。
```
`window`有如下Getter属性:
```python
import easygame as eg
window = eg.window()
rect = window.rectangle  # 获取窗口的pygame.Rect对象
center = rect.center  # 获取窗口中心
pos = window.mouse_position  # 获取鼠标位置
```
使用`stop`关闭`window`:
```python
import easygame as eg
window = eg.window()
window.stop(a=1)  # 关闭window，调用over_function，传入的是over_function的参数。
```
使用`mainloop`显示窗口:
```python
import easygame as eg
window = eg.window()
window.mainloop(
    status=0,  # 退出状态码
    esc_quit=True,  # 按下ESC键是否退出
    event_handler=eg.do_something,  # 处理pygame事件的函数，要有一个入参。
    up_func=eg.do_something,  # 事件处理前调用的函数，用于绘制组件。
    down_func=eg.do_something,  # 事件处理后调用的函数，用于判断并反馈。
    over_function=eg.do_something,  # 退出后调用的函数
)
```
Tips: `window.mainloop`方法会返回*Game Over*的字符。
## 异常
在`easygame`中可能抛出`EasyGameError`:
```python
import easygame as eg
try:
    window = eg.window()
except eg.EasyGameError:
    pass
```
## 颜色
`easygame`收录了一些颜色的RGB元组:
```python
import easygame as eg
eg.red = (255, 0, 0)
eg.green = (0, 255, 0)
eg.blue = (0, 0, 255)
eg.black = (0, 0, 0)
eg.white = (255, 255, 255)
eg.brown = (142, 88, 60)
eg.yellow = (255, 255, 0)
eg.pink = (255, 174, 201)
eg.purple = (128, 0, 255)
eg.orange = (255, 128, 0)
eg.grey = (128, 128, 128)
eg.rose = (255, 0, 128)
eg.banana = (255, 255, 50)
eg.sea = (0, 255, 255)
```
## 组件
### secret-key
`get_secret_key`可以保证安全性。
```python
import easygame as eg
if eg.get_secret_key() != eg.SECRET_KEY:
    raise SystemExit('secret-key is wrong')
```
### Widget
`Widget`为组件基类，参数:
```python
Widget(
    screen,  # easygame.window对象
    *images,  # 造型图片
    size=(40, 40),   # 图片大小
    position=(0, 0),  # 初始位置
)
```
使用`pack`方法添加到组件队列:
```python
import easygame as eg
window = eg.window()
widget = eg.Widget(window, 'test.png')
widget.pack()  # 等同于 window.add_widget(widget)
window.mainloop()
```
widget对象具有__call__方法:
```python
import easygame as eg
window = eg.window()
widget = eg.Widget(window, 'test.png')
widget = widget(window, 'test2.png')  # 重设widget
widget = widget.reset(window, 'test3.png')  # 使用此方法与上面的相同
widget.pack()  # 等同于 window.add_widget(widget)
window.mainloop()
```
使用`update`绘制widget:
```python
import easygame as eg
def up_func():  # 回调函数
    widget.update()
window = eg.window()
widget = eg.Widget(window, 'test.png')
window.mainloop(up_func=up_func)
```
`widget`有如下造型方法:
```python
import easygame as eg
window = eg.window()
widget = eg.Widget(window, 'test.png', 'test2.png')
widget.add_modelling()  # 增加一个造型编号
widget.set_modelling(0)  # 设置造型编号
number = widget.modelling  # 获取造型编号
widget.pack()  # 等同于 window.add_widget(widget)
window.mainloop()
```
`widget`有如下pygame方法:
```python
import easygame as eg
window = eg.window()
widget = eg.Widget(window, 'test.png')
rect = widget.rectangle  # 组件的pygame.Rect对象
surface = widget.get_screen()  # 窗口对象
widget.pack()  # 等同于 window.add_widget(widget)
window.mainloop()
```
`widget`有如下图层方法:
```python
import easygame as eg
window = eg.window()
widget1 = eg.Widget(window, 'test.png')
widget2 = eg.Widget(window, 'test2.png')
widget1.pack()
widget2.pack()
# pack之后才能对图层操作
widget1.set_layer(0)  # 设置图层为0层(底层)
widget1.set_layer_down()  # 移动至底层
widget2.set_layer_up()   # 移动至顶层
window.mainloop()
```
`widget`有如下移动方法:
```python
import easygame as eg
window = eg.window()
widget = eg.Widget(window, 'test.png')
widget.move_to(100, 100)  # 移动至(100, 100)
widget.move_x(50)  # 增加x坐标50
widget.move_y(100)  # 增加y坐标100
widget.move_to_mouse()  # 移动至鼠标指针
widget.pack()
window.mainloop()
```
我们可以写一个当鼠标点击就移动过去的程序:
```python
import easygame as eg
def handler(event):
    if event.type == eg.MOUSEBUTTONDOWN:
        widget.move_to_mouse()
window = eg.window()
widget = eg.Widget(window, 'test.png')
widget.pack()
window.mainloop(event_handler=handler)
```
`widget`有如下检测方法:
```python
import easygame as eg
window = eg.window()
widget = eg.Widget(window, 'test.png')
widget2 = eg.Widget(window, 'test2.png')
widget.pack()
near_x_side, near_y_side = widget.near_edge()
# widget.near_edge方法返回两个值，第一个值为碰到上/下边缘，第二个值为碰到左/右边缘
is_collide = widget.collide_other(widget2)  # 判断组件矩形对象是否相撞
window.mainloop(esc_quit=False)
```
`widget`有如下转换方法:
```python
import easygame as eg
window = eg.window()
widget = eg.Widget(window, 'test.png', 'test2.png')
widget.set_angel(0, 45)  # 将造型0设为45度
widget.set_size(1, (60, 60))  # 将造型1设为60×60
widget.pack()
window.mainloop()
```
`widget`有如下音乐方法:
```python
import easygame as eg
window = eg.window()
widget = eg.Widget(window, 'test.png')
widget.play_sound('test.wav', async_play=True)  # 异步播放音频，不支持MP3
widget.play_sound('test.mp3', async_play=False)  # 同步播放音频，支持音频与操作系统有关
widget.pause_sound()  # 暂停异步播放音频
widget.unpause_sound()  # 继续异步播放音频
widget.stop_sound()   # 停止异步播放音频
widget.pack()
window.mainloop()
```
### Background
`Background`是一个背景类，默认置于底层。继承`Widget`类。
```python
import easygame as eg
window = eg.window()
background = eg.Background(window, 'back.png')
background.pack()
window.mainloop()
```
`Background`会自动适应窗口大小。<br>
`Background`可以实现滚动背景:
```python
import easygame as eg
def up_func():  # 更新回调
    background1.rolling(speed=3)  # 滚动背景，速度为3
    background2.rolling(speed=3)  # 需要2个背景对象
window = eg.window()
background1 = eg.Background(window, 'back.png')
background2 = eg.Background(window, 'back.png')
background1.pack()
background2.pack()
window.mainloop(up_func=up_func)
```
### Button
`Button`是一个按钮类，继承`Widget`类。
```python
import easygame as eg
window = eg.window()
# 按钮类需要两个造型，为鼠标离开时的造型和鼠标碰到时的造型
button = eg.Button(window, 'up.png', 'down.png')
button.pack()
window.mainloop()
```
`Button`提供了如下鼠标方法:
```python
import easygame as eg
def handler(event: eg.EVENT_TYPE):  # 事件处理回调
    if button.near_mouse():  # 鼠标指针碰到
        print('near mouse')
    if button.click(event):  # 按钮被点击
        button.play_sound('pop.wav', async_play=False)  # 播放点击音效
window = eg.window()
# 按钮类需要两个造型，为鼠标离开时的造型和鼠标碰到时的造型
button = eg.Button(window, 'up.png', 'down.png')
button.pack()
window.mainloop(event_handler=handler)
```
### Text
`Text`是一个文字类，继承`Widget`类，无法执行大多数组件方法。
```python
import easygame as eg
window = eg.window(title='hello world', size=(200, 200),
                   bgcolor=eg.orange)
text = eg.Text(window, 'hello world', font='test.ttf',
               color=eg.black, size=40)   # 设置文字类
text.set_text('hello easy-game')  # 重设文字
text.pack() 
window.mainloop(esc_quit=False)      
```
### Input
`Input`类继承至`Button`类，按钮按下时输入才有效。<br>
`Input`类的稳定性差，开发中不要使用。
```python
import easygame as eg
def handler(event: eg.EVENT_TYPE): 
    print(input_btn.input(event))  # 获取输入值
window = eg.window(title='hello world', size=(200, 200),
                   bgcolor=eg.orange)
input_btn = eg.Input(window, 'up.png', 'down.png')
window.mainloop(esc_quit=False, event_handler=handler)      
```
### Sprite
`Sprite`继承至`Widget`类，与`Widget`无区别。<br>
以下是它的增加的方法:
```python
import easygame as eg
window = eg.window()
sprite = eg.Sprite(window, 'test.png')
sprite.say('hello!')  # 显示一个提示框，内容为hello
sprite.pack()
window.mainloop()
```
在开发中建议使用`Sprite`而不是`Widget`。
### Canvas
画布类，画笔只能在画布上绘画，继承至`Widget`
类似tkinter中的Canvas。
通过`pen = Canvas.init_pen()`获取一个画笔对象。
```python
import easygame as eg
window = eg.window()
canvas = eg.Canvas(window, position=(100, 100), size=(300, 300),
                   bgcolor=eg.red)
pen = canvas.init_pen(pen_position=(100, 100), pen_color=eg.banana)   # 创建画笔对象
pen.go_to(200, 200)  # 移动至(200, 200)
pen.clear()  # 清空画布
pen.go_to(200, 300)     # 移动至(200, 300)   
canvas.pack()
window.mainloop()
```
## CMD
使用如下命令测试`easygame`的安装:
```shell script
python -m easygame debug
```
使用如下命令测试`easygame`中`Pen`的安装:
```shell script
python -m easygame pen
```
# 更新日志
- 0.9.3版本: 实现基础功能
- 1.0.0版本: 增加mblock资源下载功能
- 1.0.1版本: 增加`EVENT_TYPE`类型
- 1.0.2版本: 完善文档和`setup`