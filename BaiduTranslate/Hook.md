## 常用Hook代码

### Hook Cookie

* 定位`Cookie`中关键参数生成位置，例：定位`__dfp`关键字

```javascript
// 自执行函数
(function () {
    'use strict';
    var cookieTemp = '';
    // 为cookie对象设定setter,遇到__dfp参数时插入断点
    Object.defineProperty(document, 'cookie', {
        set: function (val) {
            if (val.indexOf('__dfp') != -1) {
                debugger;
            }
            console.log('Hook捕获到cookie设置=>', val);
            cookieTemp = val;
            return val;
        },
        get: function () {
            return cookieTemp;
        }
    })
})();
```

### Hook Header

* 用于定位`Header`中关键参数生成位置，例：当`Header`中出现`Authorization`关键字时，插入断点：

```javascript
(function () {
    // 重写Header的setter方法，在合适的位置插入断点
    var org = window.XMLHttpRequest.prototype.setRequestHeader;
    window.XMLHttpRequest.prototype.setRequestHeader = function (key, value) {
        if (key == 'Authorization') {
            debugger;
        }
        return org.apply(this, arguments);
    }
})();
```

### Hook Url

* 用于定位请求URL中关键参数生成位置，例：当请求URL中包含`login`关键字时，插入断点：

```javascript
(function () {
    // 重写创建请求的open方法
    var open = window.XMLHttpRequest.prototype.open;
    window.XMLHttpRequest.prototype.open = function (method, url, async) {
        if (url.indexOf('login') != -1) {
            debugger;
        }
        return open.apply(this, arguments);
    }
})();
```

### Hook JSON.stringify,JSON.parse

* 在遇到JSON.stringify和JSON.parse方法时插入断点：

```javascript
(function () {
    var stringify = JSON.stringify;
    // var parse = JSON.parse;
    JSON.stringify = function (params) {
        console.log('Hook JSON.stringify =>', params);
        debugger;
        return stringify(params);
    }
})();
```

### Hook eval

* `eval()`用于计算JavaScript字符串并将其当作脚本代码来执行，经常被用来动态执行js。例：捕获所有
  `eval()`使其执行前在控制台输出将要执行的js源码：

```javascript
(function () {
    // 保存原始方法
    window.__cr_eval = window.eval;
    // 重写eval
    var myeval = function (src) {
        console.log(src);
        console.log('========= eval end =========');
        debugger;
        return window.__cr_eval(src);
    }
    // 屏蔽JS中对原生函数native属性的检测
    var _myeval = myeval.bind(null);
    _myeval.toString = window.__cr_eval.toString();
    Object.defineProperty(window, 'eval', {
        value: _myeval
    });
})();
```

### Hook Function

* 劫持所有函数操作，使其在执行前在控制台输出JS源码:

```javascript
(function () {
    // 保存原始方法
    window.__cr_func = window.Function;
    // 重写function
    var myfunc = function () {
        var args = Array.prototype.slice.call(arguments, 0, -1).join(','),
            src = arguments[arguments.length - 1];
        console.log(src);
        console.log('============== Function end ==============');
        debugger;
        return window.__cr_func.apply(this, arguments)
    }
    // 屏蔽JS中对原生函数native属性的检测
    myfunc.toString = function () {
        return window.__cr_func + ''
    }
    Object.defineProperty(window, 'Function', {
        value: myfunc
    })
})();
```