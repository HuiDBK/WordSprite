# 英文打字游戏项目

## 需求分析

> **英文打字小游戏，要有多界面交互，界面整洁、美观，可调节游戏等级难度，可配置游戏信息。**
>
> **要有游戏分数，游戏时间，动画特效，背景音乐，不同游戏等级的历史最高分记录。**
>
> **拼写成功的英文单词显示中文意思。支持长按回删键[backspace]，快速删除单词字母。**
>
> **多种游戏困难等级让玩家可以侧重提高打字速度、或者练习英语单词。**

<br/>

### 游戏开始界面

- 游戏开始选项
- 游戏设置选项
- 游戏历史最高选项
- 实现各选项点击进入相对应的功能界面

<br/>

### 游戏设置界面

- 展示游戏配置信息
  - 游戏困难等级
  - 游戏初始血量
  - 英文单词的大小
  - 英文单词的颜色
- 实现动态调节游戏配置信息
  - 游戏等级、初始血量
  - 单词的大小、颜色
  - 可更换游戏背景图、背景音乐
- 分别实现暂时保存游戏配置信息、永久游戏配置信息

<br/>

### 游戏历史最高纪录界面

- 展示各游戏困难等级的历史最高纪录
  - 游戏困难等级
  - 最高分
  - 耗时
  - 创建时间

<br/>

### 游戏运行界面

- 加载背景音乐(可设为静音模式)

- 英文单词从上向下降落
- 可在界面上英文打字并显示
- 显示游戏血量、游戏分数
- 支持长按回删键，快速删除单词字母
- 实现英文单词拼写成功的颜色突出、分数计分功能
- 在游戏中，可临时调节游戏信息

<br/>

### 游戏结束界面

- 显示当局游戏分数信息
  
  - 游戏困难等级
  
  - 累计得分
  - 所耗时间
  - 历史最高分
  
- 退出、重玩游戏选项

<br/>

## 开发环境

### 编程语言

| 编程语言 | 版本号 |
| -------- | ------ |
| Python   | 3.7.1  |

<br/>

### 开发工具

| 工具名称 | 工具版本 |
| -------- | -------- |
| PyCharm  | 2019.3.1 |

<br/>

### 第三方库

| 第三库名称  | 版本号 |
| ----------- | ------ |
| pygame      | 1.9.6  |
| pyinstaller | 4.0    |
| PySimpleGUI | 4.26.0 |

#### 第三方库说明

**pygame：** 用于绘制英文打字游戏运行窗口，整体实现游戏动画效果。

**pyinstaller：** 把项目打包成可执行文件(**.exe**)，可在 **Windows** 环境下运行程序，无需 **Python** 环境。

**PySimpleGUI：** 绘制游戏整体交互窗口（开始、设置、历史最高窗口）。

<br/>

### 游戏素材

| 素材             | 文件/路径               |
| ---------------- | ----------------------- |
| 游戏音乐         | `resource/music/…`      |
| 游戏字体         | `resource/font/HUI.TTF` |
| 游戏背景图、图标 | `resource/image/…`      |
| 英语四级单词文本 | `resource/en_word.txt`  |

<br/>

## 项目架构概览

### 目录树形结构

```Python
WordSprite
├─.idea
│  └─inspectionProfiles
├─bin
│  └─resource
│      ├─font
│      ├─image
│      │  └─animation
│      └─music
├─document
└─source
│    └─resource
│        ├─font
│        ├─image
│        │  └─animation
│        └─music
├─readme.md
```

<br/>

### 项目目录结构图

![项目目录结构图](https://img-blog.csdnimg.cn/20201007213830567.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNjI5ODU3,size_16,color_FFFFFF,t_70#pic_center '项目目录结构图')

<br/>

### 页面功能图

![英文打字游戏项目架构概览图](https://img-blog.csdnimg.cn/20200801235016696.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNjI5ODU3,size_16,color_FFFFFF,t_70 '英文打字游戏项目架构概览图')

<br/>

## 使用说明

### 游戏主界面

![游戏主界面](https://img-blog.csdnimg.cn/20201007230047411.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNjI5ODU3,size_16,color_FFFFFF,t_70#pic_center '游戏主界面')

<br/>

### 游戏运行界面

![游戏运行界面](https://img-blog.csdnimg.cn/20201007234329315.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNjI5ODU3,size_16,color_FFFFFF,t_70#pic_center '游戏运行界面')

<br/>

游戏运行界面，会根据你键盘输入的单词去匹配游戏垂直降落的单词。

- 单词前缀匹配成功有颜色突出。
- 完全匹配（单词拼写成功）会显示相对应的中文意思，游戏分数加一，游戏血条增加，并且显示拼写动画特效。
- 游戏运行期间游戏血条会一直逐渐减少，游戏结束、暂停才会停止。
- 降落的单词超出游戏屏幕，游戏血条减少。
- 游戏每增加10分、游戏血条快满时，降落的单词速度短暂增速。
- 游戏血条不同状态有不同的颜色显示。
- 可打开游戏设置界面（游戏暂停），动态调节游戏配置信息。
- 播放背景音乐。

<br/>

### 游戏设置界面

![游戏设置界面](https://images.gitee.com/uploads/images/2020/1008/194124_647096c5_4986021.png '游戏设置界面')



游戏设置界面用于调节游戏配置信息，游戏运行时也可以调出动态调节。

#### 调节游戏等级

游戏分为五个等级，分别为

| 游戏等级 | 名称                             | 单词下落速度 |
| -------- | -------------------------------- | ------------ |
| 1        | <font color='green'>简单</font>  | 0.3          |
| 2        | <font color='blue'>上手</font>   | 0.5          |
| 3        | <font color='orange'>中等</font> | 1.0          |
| 4        | <font color='red'>困难</font>    | 1.5          |
| 5        | <font color='purple'>魔鬼</font> | 2.0          |

**游戏运行期间游戏血条会一直逐渐减少、降落的单词超出游戏屏幕，游戏血条减少，游戏血条减少的程度都随着游戏等级的提高而提高。**

<br/>

#### 其他调节

- 游戏字体大小
- 游戏初始血条
- 游戏静音状态
- 游戏单词字体颜色
- 单词拼写匹配成功的突出颜色

<br/>

#### 配置信息保存

**临时保存**

临时保存，可用于试探不同的配置信息的游戏效果如何，看看是否满意，如果不满意，又可换回原来的配置信息。

临时保存适用于当局游戏有效，重玩、重开都无效。

**永久保存**

永久保存将把游戏配置信息写入配置文件中，永久生效。

**注意：游戏静音状态的调节，无需保存也可实现效果，但每次打开游戏的时候都是声音开放状态。**

<br/>

### 游戏历史最高界面

![历史最高界面](https://img-blog.csdnimg.cn/20201008002049517.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNjI5ODU3,size_16,color_FFFFFF,t_70#pic_center '历史最高界面')

<br/>

历史最高界面，显示着不同游戏等级的历史最高分记录。

- 最高分
- 游戏耗时
- 记录创建时间

<br/>

### 游戏版本信息、关于作者

![关于作者](https://img-blog.csdnimg.cn/20201008002237276.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNjI5ODU3,size_16,color_FFFFFF,t_70#pic_center '关于作者')

最后就是游戏版本、作者信息。制作不易，留下你的小红心:heart:，万分感谢。

<br/>

## 源代码

源代码已上传到 **GitHub** [Word Sprite](https://github.com/HuiDBK/WordSprite)，欢迎大家下载玩耍。

**✍ 码字不易，留下你小赞 :+1: 收藏 :star:，万分感谢:ok_hand:**

