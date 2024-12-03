---
title: Android弹窗BottomSheetDialog总结
date: 2020-07-11
categories: 
  - Android开发
---

# 圆角效果

-   先设置原有背景透明

style.xml

```
    <!--实现BottomSheetDialog圆角效果-->
    <style name="BottomSheetDialog" parent="Theme.Design.Light.BottomSheetDialog">
        <item name="bottomSheetStyle">@style/bottomSheetStyleWrapper</item>
    </style>
    <style name="bottomSheetStyleWrapper" parent="Widget.Design.BottomSheet.Modal">
        <item name="android:background">@android:color/transparent</item>
    </style>
```

-   onCreate中设置style

```
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setStyle(STYLE_NORMAL, R.style.BottomSheetDialog)
    }
```

-   设置我们自己的style

在`根布局的view`上设置`background`

```
android:background="@drawable/shape_sheet_dialog_bg"
```

shape_sheet_dialog_bg

```
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <corners
        android:topLeftRadius="15dp"
        android:topRightRadius="15dp" />
    <solid android:color="@color/white" />
</shape>
```

# 去掉背景阴影
还是style，设置`backgroundDimEnabled`为`false`即可

```

    <!--实现BottomSheetDialog圆角效果 且无背景阴影-->
    <style name="BottomSheetDialogBg" parent="Theme.Design.Light.BottomSheetDialog">
        <item name="bottomSheetStyle">@style/bottomSheetStyleWrapper</item>
        <item name="android:backgroundDimEnabled">false</item>
    </style>
    <style name="bottomSheetStyleWrapper" parent="Widget.Design.BottomSheet.Modal">
        <item name="android:background">@android:color/transparent</item>
    </style>
```
  

# 默认展开
默认是不展开的，如果想展开，也就是全屏，可以设置`state`为`BottomSheetBehavior.STATE_EXPANDED`。

```
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)
    
    if (dialog is BottomSheetDialog) {
        val behaviour = (dialog as BottomSheetDialog).behavior 
        behaviour.state = BottomSheetBehavior.STATE_EXPANDED 
    }
}
```

# 禁止拖拽

官方对`setDraggable`的解释是：设置是否可以通过拖动折叠/展开，禁用拖动时，应用程序需要实现自定义方式来展开/折叠对话框。

```
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)
    
    if (dialog is BottomSheetDialog) {
        val behaviour = (dialog as BottomSheetDialog).behavior 
        behaviour.isDraggable=false
    }
}
```

# 监听展开收起
有时候还需要在向上拖拽时候做一些联动，就需要获取对话框滑动的值，可以通过behavior.addBottomSheetCallback来实现。

- STATE_DRAGGING：拖动状态
- STATE_SETTLING：松开手指后，自由滑动状态
- STATE_EXPANDED：完全展开状态
- STATE_COLLAPSED：折叠状态，或者称为半展开状态
- STATE_HIDDEN：隐藏状态



slideOffset的值是0-1之间，默认状态下是0，滑动到顶部的时候值是1，消失的时候值是-1,  
```
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)
    
    if (dialog is BottomSheetDialog) {
        val behaviour = (dialog as BottomSheetDialog).behavior 
        behaviour.addBottomSheetCallback(object :
            BottomSheetBehavior.BottomSheetCallback() {
            override fun onStateChanged(bottomSheet: View, newState: Int) {
                when (newState) {
                    BottomSheetBehavior.STATE_EXPANDED -> {
                        Log.d("bottom", "BottomSheetBehavior.STATE_EXPANDED")
                    }

                    BottomSheetBehavior.STATE_COLLAPSED -> {
                        Log.d("bottom", "BottomSheetBehavior.STATE_COLLAPSED")
                    }

                    BottomSheetBehavior.STATE_DRAGGING -> {
                        Log.d("bottom", "BottomSheetBehavior.STATE_DRAGGING")
                    }

                    BottomSheetBehavior.STATE_SETTLING -> {
                        Log.d("bottom", "BottomSheetBehavior.STATE_SETTLING")
                    }

                    BottomSheetBehavior.STATE_HIDDEN -> {
                        Log.d("bottom", "BottomSheetBehavior.STATE_HIDDEN")
                    }
                    BottomSheetBehavior.STATE_HALF_EXPANDED -> {
                        Log.d("bottom", "BottomSheetBehavior.STATE_HALF_EXPANDED")
                    }
                }
            }

            override fun onSlide(bottomSheet: View, slideOffset: Float) {

            }
        })
    }
}
```

# 设置默认进入展开状态下拉不进入折叠状态
```
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)
    
    if (dialog is BottomSheetDialog) {
        val behaviour = (dialog as BottomSheetDialog).behavior 
        behaviour.state = BottomSheetBehavior.STATE_EXPANDED
        //表示在隐藏时，跳过折叠状态，直接进入隐藏状态。
        behaviour.skipCollapsed = true;
    }
}
```

# 设置弹窗固定高度

### 方式一.

```
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)
    
    if (dialog is BottomSheetDialog) {
        val behaviour = (dialog as BottomSheetDialog).behavior 
        behaviour.state = BottomSheetBehavior.STATE_EXPANDED

        behaviour.isFitToContents = false
        //expandedOffset表示弹窗顶部距离屏幕顶部的距离
        behaviour.expandedOffset = 100
    }
}
```


### 方式二.

```
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)
        //设置最大高度
    val mMaxSlideHeight = (resources.displayMetrics.heightPixels * 1).toInt()
    val params = view.layoutParams
    params.height=mMaxSlideHeight
    view.layoutParams=params
}
```

# 折叠弹窗的高度
```
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)
    
    if (dialog is BottomSheetDialog) {
        val behaviour = (dialog as BottomSheetDialog).behavior 
        behaviour.state = BottomSheetBehavior.STATE_EXPANDED
        //设置折叠时的高度    
        behaviour.peekHeight = 100
    }
}
```

# 参考资料
[BottomSheetXXX实现下滑关闭菜单踩坑记](https://www.jianshu.com/p/e460d4b47dd4)