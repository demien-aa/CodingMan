(function(){
  var cache = {};

  this.microTemplate = function microTemplate(str, data){
    // Figure out if we're getting a template, or if we need to
    // load the template - and be sure to cache the result.
    var fn = !/\W/.test(str) ?
      cache[str] = cache[str] ||
          microTemplate(document.getElementById(str).innerHTML) :

      // Generate a reusable function that will serve as a template
      // generator (and which will be cached).
      new Function("data",
        "var p=[];" +

        // Introduce the data as local variables using with(){}
        "p.push('" +

        // Convert the template into pure JavaScript
        str
          .replace(/[\r\t\n]/g, " ")
          .split("<%").join("\t")
          .replace(/((^|%>)[^\t]*)'/g, "$1\r")
          .replace(/\t=(.*?)%>/g, "',$1,'")
          .split("\t").join("');")
          .split("%>").join("p.push('")
          .split("\r").join("\\'")
      + "');return p.join('');");

    // Provide some basic currying to the user
    return data ? fn( data ) : fn;
  };
})();
(function() {
    function range(start, end) {
        var result = [];

        if(typeof end === 'undefined') {
            end = start;
            start = 0;
        }
        for(;start < end; start++) {
            result.push(start);
        }

        return result;
    }

    Array.prototype.randomEach = function(func) {
        if (typeof func != "function") {
            throw new TypeError();
        }

        var len = this.length,
            indexes = range(len);

        while(len) {
            var cursor = Math.floor(Math.random() * (len--));
            if(func(this[indexes[cursor]]) === false) {
                break;
            }
            indexes[cursor] = indexes[len];
        }
    };

    Array.prototype.confound = function () {
        this.sort(function () {
            return Math.random() - 0.5;
        });
    };

    if (!Array.prototype.forEach) {
        Array.prototype.forEach = function(func /*, thisp*/) {
            var len = this.length;

            if (typeof func != "function") {
                throw new TypeError();
            }

            var thisp = arguments[1];

            for (var i = 0; i < len; i++) {
                if (i in this)
                    func.call(thisp, this[i], i, this);
            }
        };
    }
}());

/**
 *  影子克隆��?��对象
 *
 *  @method _shadowClone
 *  @param {Object} obj 待克隆的对象
 *  @return {Object} 克隆产生的对��? */
function _shadowClone(obj) {
    var result = {};

    for(var key in obj) {
        if(obj.hasOwnProperty(key)) {
            result[key] = obj[key];
        }
    }
    return result;
}
function AutoLoader(generator, timeout) {
    if (typeof generator != "function") {
        throw new TypeError();
    }
    this._generator = generator;
    this._timeout = timeout;
    this._context = arguments[2];
    this._pool = [];

    this._load();
}

AutoLoader.prototype._load = function() {
    var self = this;

    clearTimeout(this._loading);

    this._loading = setTimeout(function() {
        self._pool.push(self._generator.apply(self._context));
        //console.debug('自动填充完毕');
    }, this._timeout);
};

AutoLoader.prototype.get = function() {
    var result;
    clearTimeout(this._loading);

    if(this._pool.length > 0) {
        //console.debug('取自缓存');
        result = this._pool.pop();
    } else {
        //console.debug('立即生成');
        result = this._generator.apply(this._context);
    }
    this._load();
    return result;
};

AutoLoader.prototype.regenerate = function() {
    this._pool.length = 0;
    this._load();
};window.tagConfig = {
    areas: {
        cols_40_60: [
            {
                width: 40,
                rows:  [
                    { height: 100 }
                ]
            },
            {
                width: 60,
                rows: [
                    { height: 100 }
                ]
            }
        ],
        cols_50_50: [
            {
                width: 50,
                rows:  [
                    { height: 100 }
                ]
            },
            {
                width: 50,
                rows: [
                    { height: 100 }
                ]
            }
        ],
        cols_32_32_36: [
            {
                width: 32,
                rows:  [
                    { height: 100 }
                ]
            },
            {
                width: 32,
                rows:  [
                    { height: 100 }
                ]
            },
            {
                width: 36,
                rows: [
                    { height: 100 }
                ]
            }
        ]
    }
};

window.tagConfig.pageLayout = {
    top: 0,
    left: 0,
    width: 100,
    height: 100,

    random: false,
    cols:  [
        {
            width: 45,
            rows:  [
                {
                    random: false,
                    height: 100,
                    rows:  [
                        {
                            height: 45,
                            cols: [
                                {
                                    width: 100
                                }
                            ]
                        },
                        {
                            height: 30,
                            cols: [
                                {
                                    width: 100
                                }
                            ]
                        },
                        {
                            height: 25,
                            cols:  [
                                {
                                    width: 100,
                                    cols: [
                                        {
                                            width: 35,
                                            rows: [
                                                {
                                                    height: 100
                                                }
                                            ]
                                        },
                                        {
                                            width: 25,
                                            rows: [
                                                {
                                                    height: 50
                                                },
                                                {
                                                    height: 50
                                                }
                                            ]
                                        },
                                        {
                                            width: 15,
                                            rows: [
                                                {
                                                    height: 50
                                                },
                                                {
                                                    height: 50
                                                }
                                            ]
                                        },
                                        {
                                            width: 25,
                                            rows: [
                                                {
                                                    height: 60
                                                },
                                                {
                                                    height: 40
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            width: 55,
            random: false,
            rows: [
                {
                    height: 50,
                    random: false,
                    cols: [
                        {
                            width: 65,
                            rows: [
                                {
                                    height: 50
                                },
                                {
                                    height: 50
                                }
                            ]
                        },
                        {
                            width: 35,
                            random: false,
                            rows: [
                                {
                                    height: 65
                                },
                                {
                                    height: 35
                                }
                            ]
                        }
                    ]
                },
                {
                    height: 28,
                    cols: [
                        {
                            width: 30,
                            rows: [
                                {
                                    height: 100
                                }
                            ]
                        },
                        {
                            width: 40,
                            rows: [
                                {
                                    height: 50
                                },
                                {
                                    height: 50,
                                    cols: window.tagConfig.areas.cols_40_60
                                }
                            ]
                        },
                        {
                            width:30,
                            rows:[
                                {
                                    height: 40
                                },
                                {
                                    height: 60,
                                    cols: window.tagConfig.areas.cols_40_60
                                }
                            ]
                        }
                    ]
                },
                {
                    height: 22,
                    cols: [
                        {
                            width: 35,
                            rows: [
                                {
                                    height: 100
                                }
                            ]
                        },
                        {
                            width: 15,
                            rows: [
                                {
                                    height: 100
                                }
                            ]
                        },
                        {
                            width: 15,
                            rows: [
                                {
                                    height: 50
                                },
                                {
                                    height: 50
                                }
                            ]
                        },
                        {
                            width: 20,
                            rows: [
                                {
                                    height: 40
                                },
                                {
                                    height: 60
                                }
                            ]
                        },
                        {
                            width: 15,
                            rows: [
                                {
                                    height: 50
                                },
                                {
                                    height: 50
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
};

window.tagConfig.colorPatterns = [
    [
        {
            backgrounds: [

                '#595e90',
                '#686fa7'
            ],
            fontColor: '#FFF',
            borderColor: '#5c666f'
        },
        {
            backgrounds: [
                '#d17a4d',
                '#e3895c'
            ],
            fontColor: '#FFF',
            borderColor: '#5c666f'
        },
        {
            backgrounds: [
                '#8e6da0',
                '#a181b2'
            ],
            fontColor: '#FFF',
            borderColor: '#5c666f'
        },
        {
            backgrounds: [
                '#869259',
                '#9ca868'
            ],
            fontColor: '#FFF',
            borderColor: '#5c666f'
        }
    ]
];

window.tagConfig.tagLevels = {
    '1': {
        count: 8
    },
    '2': {
        count: 8
    },
    '3': {
        count: 8
    },
    '4': {
        count: 4
    }
};

window.tagConfig.navConfig = {
    currentPos : 'news',
    dataNames : ['tagDataNews', 'tagDataMoney', 'tagDataTech', 'tagDataSports', 'tagDataAuto', 'tagDataEnt'],
    hashReg : /news|money|tech|sports|auto|ent/
}
/**
 *  根据配置遍历��?��区域下的��?��小区��? *
 *  @method _cutGrid
 *  @param {Object} grid 区域的描��? *  @param {Function} callback 回调函数，每处理��?��小区域都会被调用��?��
 */
function _cutGrid(grid, callback) {
    var mainAxis, crossAxis;

    if(grid.rows) {
        mainAxis = {
            name: 'rows',
            measure: 'height',
            offset: 'top'

        };
        crossAxis = {
            name: 'cols',
            measure: 'width',
            offset: 'left'
        };
    } else {
        mainAxis = {
            name: 'cols',
            measure: 'width',
            offset: 'left'

        };
        crossAxis = {
            name: 'rows',
            measure: 'height',
            offset: 'top'
        };
    }

    var mainAxisOffset = 0, crossAxisOffset = 0,
        mainAxisAmount = grid[mainAxis.name].length,
        mainAxisCounter = 0;

    function mainAxisHandler(main) {
        var mainAxisLength,
            crossAxisAmount = main[crossAxis.name].length,
            crossAxisCounter = 0;

        mainAxisCounter++;
        mainAxisLength = mainAxisCounter === mainAxisAmount ? (grid[mainAxis.measure] - mainAxisOffset)
            : Math.floor(main[mainAxis.measure] * grid[mainAxis.measure] / 100);

        function crossAxisHandler(cross) {
            var crossAxisLength,
                obj = _shadowClone(cross);

            crossAxisCounter++;
            crossAxisLength = crossAxisCounter === crossAxisAmount ? (grid[crossAxis.measure] - crossAxisOffset)
                : Math.floor(cross[crossAxis.measure] * grid[crossAxis.measure] / 100);

            obj[mainAxis.offset] = mainAxisOffset + grid[mainAxis.offset];
            obj[crossAxis.offset] = crossAxisOffset + grid[crossAxis.offset];
            obj[mainAxis.measure] = mainAxisLength;
            obj[crossAxis.measure] = crossAxisLength;
            obj.colorPattern = grid.colorPattern;

            callback(obj);
            crossAxisOffset += crossAxisLength;
        }
        if(main.random === false) {
            main[crossAxis.name].forEach(crossAxisHandler);
        } else {
            main[crossAxis.name].randomEach(crossAxisHandler);
        }

        crossAxisOffset = 0;
        mainAxisOffset += mainAxisLength;
    }

    if(grid.random === false) {
        grid[mainAxis.name].forEach(mainAxisHandler);
    } else {
        grid[mainAxis.name].randomEach(mainAxisHandler);
    }
}

function _getGrids(config) {
    var result = [],
        cursor = 0,
        fontSizeFactor = 0.18,
        colorPatterns = config.colorPatterns[0];

    _cutGrid(config.pageLayout, function(gridConfig) {
        if(!gridConfig.colorPattern) {
            gridConfig.colorPattern = colorPatterns[cursor++];
        }
        if(gridConfig.rows || gridConfig.cols) {
            _cutGrid(gridConfig, arguments.callee);
        } else {
            var colorPattern = gridConfig.colorPattern,
                backgrounds = colorPattern.backgrounds,
                backgroundsLength = backgrounds.length,
                //borderColor = colorPattern.borderColor,
                fontColor = colorPattern.fontColor;

            gridConfig.fontSize = Math.floor(Math.sqrt(gridConfig.width * gridConfig.height) * fontSizeFactor);
            gridConfig.backgroundColor = backgrounds[Math.floor(Math.random() * backgroundsLength)];
            gridConfig.fontColor = fontColor;
            //gridConfig.borderColor = borderColor;

            result.push(gridConfig);
        }
    });

    return result;
}

function getTagData() {
    // 由后台生成的数据
    var result = [],
        tagData = window['tagData'],
        levels = window.tagConfig.tagLevels;

    for(var key in tagData) {
        if(tagData.hasOwnProperty(key)) {
            var counter = 0,
                total = levels[key].count;

            tagData[key].randomEach(function(item) {
                if (total <= counter) {
                    return false;
                }
                result.push(item);
                counter++;
                return true;
            });
        }
    }
    return result;
}

function reflowTagElem(elem, config) {
    elem.style.top = config.top + 'px';
    elem.style.left = config.left + 'px';
    elem.style.width = config.width - 2 + 'px';
    elem.style.height = config.height - 2 + 'px';
    elem.style.fontSize = config.fontSize + 'px';
    elem.style.color = config.fontColor;

    elem.style.backgroundColor = config.backgroundColor;
    //elem.style.borderColor = conf.borderColor;

    elem.order = config.width * config.height;
}

var tagElems = [],
    gridsAutoLoader,
    tagDataAutoLoader;

function _appendImg(elem, imgs) {
    var width = elem.style.width.split('px')[0];
    var height = elem.style.height.split('px')[0];
    var maxColNum = parseInt((width-10)/50);
    var maxRowNum = parseInt((height)/50);
    var imgDiv = document.createElement('div');
    imgDiv.style.position = 'fixed';
    imgDiv.style.display = 'none';
    var top = -35;
    var imgIndex = 0;
    for(var i = 0; i < maxRowNum; i++){
        top += 50;
        var left = -30;
        for(var j = 0; j < maxColNum; j++){
            var img = document.createElement('img');
            img.className = 'app_icon';
            left += 50;
            img.style.left = left + 'px';
            img.style.top = top + 'px';
            img.src = imgs[imgIndex].src;
            img.title = imgs[imgIndex].title;
            console.log(imgs[imgIndex].src);
            imgIndex += 1;
            //if(j%2 === 0)
            //    img.src = 'https://static-s.aa-cdn.net/img/ios/284882215/414fb5243cf13d547113e8741d51c3f2';
            //else if (j%3 === 0)
            //    img.src = 'https://static-s.aa-cdn.net/img/ios/529479190/785445a28148203e2761939fd365c445';
            //else if (j%5 === 0)
            //    img.src = 'https://static-s.aa-cdn.net/img/ios/389801252/80d861160a6231294e4c067430a698e4';
            //else if (j%7 === 0)
            //    img.src = 'https://static-s.aa-cdn.net/img/ios/389801252/80d861160a6231294e4c067430a698e4';
            //else if (j%11 === 0)
            //    img.src = 'https://static-s.aa-cdn.net/img/ios/389801252/80d861160a6231294e4c067430a698e4';
            //else
            //    img.src = 'https://static-s.aa-cdn.net/img/ios/529479190/785445a28148203e2761939fd365c445';
            //img.title = 'Facebook';
            imgDiv.appendChild(img);
        }
    }
    elem.appendChild(imgDiv);
}

function _appendSmallImgTag(elem,span, tagData, index) {
    var width = parseInt(elem.style.width.split('px')[0]);
    var height = parseInt(elem.style.height.split('px')[0]);
    var imgSize = width > height? height:width;
    var imgSpan = document.createElement('span');
    imgSpan.className = 'doc-title';
    //var marginLeft = (width - (imgSize*0.9))/6;
    //for(var i = 0; i < 3; i++){
    //    var img = document.createElement('img');
    //    img.style.width = imgSize*0.3+'px';
    //    img.style.height = imgSize*0.3+'px';
    //    img.style.position = 'relative';
    //    img.style.marginLeft= marginLeft+'px';
    //    img.style.borderRadius = '8px';
    //    if(i === 0)
    //        img.src = 'https://static-s.aa-cdn.net/img/ios/284882215/414fb5243cf13d547113e8741d51c3f2';
    //    else if (i === 1)
    //        img.src = 'https://static-s.aa-cdn.net/img/ios/529479190/785445a28148203e2761939fd365c445';
    //    else if (i === 2)
    //        img.src = 'https://static-s.aa-cdn.net/img/ios/389801252/80d861160a6231294e4c067430a698e4';
    //    img.title = 'Facebook';
    //    imgSpan.appendChild(img);
    //}
    var subTitle = 'This is a tag for filter apps, total number is 123'
    imgSpan.innerHTML = subTitle;
    span.appendChild(imgSpan);
}

function _setContent() {
    var tagDatas = window.tagData;

    // 按面积，从大到小排列tag区块
    tagElems.sort(function(a, b) {
        return b.order - a.order;
    });

    tagElems.forEach(function(elem, i) {
        var tagData = tagDatas[i];
        elem.innerHTML = '';

        _appendImg(elem,tagData['imgs']);
        var title = document.createElement('span');

        title.className = 'inner';
        title.innerHTML = tagData['tagName'];
        _appendSmallImgTag(elem,title,tagData['imgs'],i);
        elem.appendChild(title);
    });
    console.log("total tag elements num is : "+tagElems.length);
}


var animationTemplate = microTemplate('animation_template'),
    animationRules = document.getElementById('animation_rules');

function _initStage(stage, config) {
    try{
        var offset = stage.clientWidth,
            rules = '';

        ['-moz-', '-webkit-', '-o-', '-ms-', ''].forEach(function(prefix) {
            rules += animationTemplate({
                prefix: prefix,
                offset: offset
            });
        });
        animationRules.innerHTML = rules;
    }
    catch(e) {
    }

    config.pageLayout.width = stage.clientWidth;
    config.pageLayout.height = stage.clientHeight;
}

function fillStage(stage) {
    var grids = gridsAutoLoader.get();

    grids.forEach(function(grid) {
        var elem = document.createElement('div');

        elem.className = 'tag';
        reflowTagElem(elem, grid);
        stage.appendChild(elem);
        tagElems.push(elem);
        elem.onmouseover = function() {
            var title = elem.getElementsByTagName('span')[0];
            title.style.display = 'none';
            var imgDiv = elem.getElementsByTagName('div')[0];
            imgDiv.style.display = 'initial';
        }
        elem.onmouseout = function() {
            var title = elem.getElementsByTagName('span')[0];
            title.style.display = 'block';
            var imgDiv = elem.getElementsByTagName('div')[0];
            imgDiv.style.display = 'none';
        }
    });
    _setContent();
}

function refreshStage() {
    tagElems.confound();
    var grids = gridsAutoLoader.get();

    grids.forEach(function(grid, i) {
        reflowTagElem(tagElems[i], grid);
    });
    _setContent();
}

function slideStage(offset, callback) {
    var total = tagElems.length,
        completed = 0,
        animationIn, animationOut;

    if(offset > 0 ) {
        animationOut = 'right-out';
        animationIn = 'left-in';
    } else {
        animationOut = 'left-out';
        animationIn = 'right-in';
    }

    tagElems.forEach(function(elem) {
        setTimeout(function() {
            elem.style.animationName = animationOut;
            elem.style.webkitAnimationName = animationOut;
            setTimeout(function(){
                elem.style.animationName = animationIn;
                elem.style.webkitAnimationName = animationIn;
            }, 800);

            completed++;
            if(completed === total) {
                callback();
            }
        }, Math.random() * 400);
    });
}

var stage = document.getElementById('stage'),
    resizeTimer,
    // 切换导航数据的�?��?
    navBar = document.getElementById('nav_bar'),
    indicator = document.getElementById('nav_current'),
    buttons = navBar.getElementsByTagName('a'),
    currentButton, currentIndex,
    // 导航数据的变量名
    tagDataNames = window.tagConfig.navConfig.dataNames;


Array.prototype.forEach.call(buttons, function(button, index) {
    // 根据url的hash值，将当前按钮定位到特定的位置上
    if(button.className.indexOf(window.tagConfig.navConfig.currentPos) !== -1) {
        indicator.style.left = button.offsetLeft + 'px';
        indicator.style.display = 'block';
        button.className += ' current';

        currentButton = button;
        currentIndex = index;
        window.tagData = window.tagDatas[index];
    }

    button.onclick = function() {
        changeNav(button, index);
    };
});


function changeNav(button, index) {
        //if(window[tagDataNames[index]]) {
        //    window.tagData = window[tagDataNames[index]];
        //    tagDataAutoLoader.regenerate();
        //}

        indicator.style.left = button.offsetLeft + 'px';
        button.className += ' current';
        window.tagConfig.navConfig.currentPos = button.getAttribute('href').split('#')[1];

        currentButton.className = currentButton.className.replace(/\s*current/, '');

        slideStage(currentIndex - index, function() {
            setTimeout(function() {
                _setContent();
            }, 400);
        });

        currentButton = button;
        currentIndex = index;
}
// 自动填充下次刷新��?��的布��?��格，以加快用户响应�?��?
gridsAutoLoader = new AutoLoader(function() {
    return _getGrids(window.tagConfig);
}, 1000);

// 自动填充下次刷新��?��的Tag数据，以加快用户响应速度
//tagDataAutoLoader = new AutoLoader(function() {
//    return getTagData();
//}, 1000);

_initStage(stage, window.tagConfig);
fillStage(stage);

function resize() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
        gridsAutoLoader.regenerate();
        _initStage(stage, window.tagConfig);
        refreshStage();
    }, 500);
}

window.onresize = resize;

var circle_count = 0;
document.getElementById('refresh').onclick = function () {
    var transform = 'rotate(' + 360 * ++circle_count + 'deg)';

    this.style.transform = transform;
    this.style.webkitTransform = transform;
    refreshStage();
};


