
# Table of Contents

1.  [目录规范](#org2bc3f85)
2.  [文档规范](#org2de25a2)
    1.  [接口文档](#org0f622da)
    2.  [环境依赖文档](#org2419a7a)
    3.  [使用说明](#org9d8387a)
3.  [代码规范](#orgd18a3fb)
    1.  [命名规范](#org767a1b9)
    2.  [风格规范](#org341cecf)
    3.  [类型提示规范](#orgb6b063e)
4.  [日志规范](#org97abb7c)
    1.  [创建Logger](#org4f3b9f4)
    2.  [日志格式](#org2904d0d)
    3.  [日志输出](#org9753137)
5.  [单元测试](#org33ac887)
6.  [版本管理](#org082b183)
    1.  [Git基本操作](#orga3ca75a)
    2.  [Commit格式规范](#org85d58db)



<a id="org2bc3f85"></a>

# 目录规范

-   **code (或同名于项目名称):** 存储项目代码
-   **tests:** 存储单元测试
-   **binder:** 存储项目依赖
-   **docs:** 存储项目文档


<a id="org2de25a2"></a>

# 文档规范


<a id="org0f622da"></a>

## 接口文档

接口文档应包含如下内容：

1.  接口功能简述
2.  接口调用方式
3.  接口输入示例
4.  接口输出示例


<a id="org2419a7a"></a>

## 环境依赖文档

1.  python版本
2.  requirements.txt
3.  其他依赖


<a id="org9d8387a"></a>

## 使用说明

1.  安装文档
2.  运行文档


<a id="orgd18a3fb"></a>

# 代码规范


<a id="org767a1b9"></a>

## 命名规范

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">类型</th>
<th scope="col" class="org-left">公有</th>
<th scope="col" class="org-left">内部</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">包</td>
<td class="org-left">lower_with_under</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">模块</td>
<td class="org-left">lower_with_under</td>
<td class="org-left">_lower_with_under</td>
</tr>


<tr>
<td class="org-left">类</td>
<td class="org-left">CapWords</td>
<td class="org-left">_CapWords</td>
</tr>


<tr>
<td class="org-left">异常</td>
<td class="org-left">CapWords</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">函数</td>
<td class="org-left">lower_with_under()</td>
<td class="org-left">_lower_with_under()</td>
</tr>


<tr>
<td class="org-left">全局常量/类常量</td>
<td class="org-left">CAPS_WITH_UNDER</td>
<td class="org-left">_CAPS_WITH_UNDER</td>
</tr>


<tr>
<td class="org-left">全局变量/类变量</td>
<td class="org-left">lower_with_under</td>
<td class="org-left">_lower_with_under</td>
</tr>


<tr>
<td class="org-left">实例变量</td>
<td class="org-left">lower_with_under</td>
<td class="org-left">_lower_with_under</td>
</tr>


<tr>
<td class="org-left">方法名</td>
<td class="org-left">lower_with_under()</td>
<td class="org-left">_lower_with_under()</td>
</tr>


<tr>
<td class="org-left">函数参数/方法参数</td>
<td class="org-left">lower_with_under</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">局部变量</td>
<td class="org-left">lower_with_under</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
</table>


<a id="org341cecf"></a>

## 风格规范

使用[ruff](https://docs.astral.sh/ruff/)对代码同时进行静态检查与格式化，该工具集成了代码检查工具flake8与代码格式化工具black。
该工具支持超过700条代码书写[规则](https://docs.astral.sh/ruff/rules/)，例如：

1.  包的导入放于代码顶部；
2.  一行代码长度过长时应换行；
3.  每个public函数应有注释，包括功能概述与输入输出说明。


<a id="orgb6b063e"></a>

## 类型提示规范

1.  使用[typing](https://docs.python.org/zh-cn/3/library/typing.html)模块编写类型提示。
2.  使用[mypy](https://mypy.readthedocs.io/en/stable/)插件自动检查类型。


<a id="org97abb7c"></a>

# 日志规范

使用[logging](https://docs.python.org/zh-cn/3/library/logging.html)模块输出运行日志


<a id="org4f3b9f4"></a>

## 创建Logger

    import logging
    
    logger = logging.getLogger(__name__)
    logging.basicConfig( # 配置日志记录工具
        stream=sys.stdout, # 设置日志输出方式为标准输出
        level=logging.DEBUG, # 设置日志输出等级为DEBUG
        format="[%(asctime)s] - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
    )


<a id="org2904d0d"></a>

## 日志格式


<a id="org9753137"></a>

## 日志输出

1.  在每个功能的开头使用logger.info()记录功能开始，并在结尾处使用logger.info()记录功能完成
2.  使用logger.debug()输出调试数据


<a id="org33ac887"></a>

# 单元测试

使用[pytest](https://docs.pytest.org/en/7.1.x/contents.html)模块为每个功能编写单元测试

1.  创建context.py以将项目代码引入测试程序中


<a id="org082b183"></a>

# 版本管理

使用[Git](https://www.runoob.com/git/git-tutorial.html)管理项目版本


<a id="orga3ca75a"></a>

## Git基本操作

1.  拉取远程代码到本地
    
        git pull
2.  提交代码到本地
    
        git commit -m "message about changes"
3.  提交本地代码到远程
    
        git push


<a id="org85d58db"></a>

## Commit格式规范

1.  Commit书写格式如下：
    
        Commit类型: 简述
        
        具体描述(可选项)
2.  Commit类型应为下列之一:
    -   **feat:** 引入的新特性
    -   **fix:** bug修复
    -   **chore:** 非bug修复或新特性引入的修改，且不涉及源码与测试，如依赖更新等
    -   **refactor:** 非bug修复或新特性引入的源码重构
    -   **docs:** 更新文档，如README等
    -   **style:** 不改变源码含义的修改，如加入空格、分号的代码格式调整等
    -   **test:** 添加新测试或修正已有测试
    -   **perf:** 优化性能
    -   **tool:** 部署或开发工具，如部署脚本、启动脚本等
    -   **ci:** 持续集成相关
    -   **build:** 影响项目构建或外部依赖的修改
    -   **revert:** 撤销之前的commit
3.  Commit示例
    
        Commit类型: 简述
        fix: fix foo to enable bar
        
        This fixes the broken behavior of the component by doing xyz.

