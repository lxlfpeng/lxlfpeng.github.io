---
title: Kotlin封装一个DSL语法的DialogFragment
date: 2020-07-12
categories: 
  - Kotlin
---

# 一.领域特定语言 DSL的概念
### 1.什么是DSL
DSL（domain specific language），即领域专用语言：专门解决某一特定问题的计算机语言。由于它是以简洁的形式进行表达，整体上直观易懂，使得调用代码和读代码的成本都得以降低，即使是不懂编程语言的一般人都可以进行使用。比如大家比较熟悉的SQL语句和正则表达式。 所谓领域也就是限定语言是适用于一定范围的。可以看做是封装了一套东西, 用于特定的功能, 优势是复用性和可读性的增强。
##### (1.)DSL的特点
- 用于专门领域，不能用于其他领域。
- 有更高级的抽象，不涉及类似数据结构的细节。  
- 表现力有限，其只能描述该领域的模型。

##### (2.)通用编程语言和DSL的区别:
通用编程语言（如 Java、Kotlin、Python等），往往提供了全面的库来帮助开发者开发完整的应用程序，而 DSL 只专注于某个领域，比如 SQL 仅支持数据库的相关处理，而正则表达式只用来检索和替换文本，无法用 SQL 或者正则表达式来开发一个完整的应用。

### 2.``外部 DSL`` 和``内部 DSL``
DSL分为外部DSL和内部 DSL
##### (1.)外部DSL
在主程序设计语言之外，用一种单独的语言表示领域专有语言。可以是定制语法，或者遵循另外一种语法，如 XML、JSON。（从零开始构建的语言，需要实现语法解析器等）。

##### (2.)内部 DSL
通常是基于通用编程语言实现，具有特定的风格，如Android 的主流编译工具 Gradle。（从一种宿主语言构建而来）。

# 二.Koltin封装DSL风格弹窗
许多现代语言为创建内部 DSL 提供了一些先进的方法, Kotlin 也不例外。下面就通过kotlin的高阶函数和扩展方法, 封装一个简单的DSL风格的弹窗:
### 1.编写弹窗布局文件
```
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_gravity="center"
    android:minHeight="200dp">
    <TextView
        android:id="@+id/title_tv"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:textColor="@android:color/black"
        android:textSize="20sp"
        android:textStyle="bold"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        tools:text="title text" />

    <TextView
        android:id="@+id/message_tv"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginBottom="16dp"
        android:padding="16dp"
        android:textColor="@android:color/black"
        android:textSize="16sp"
        app:layout_constraintBottom_toTopOf="@+id/right_button"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/title_tv"
        tools:ignore="RtlCompat"
        tools:text="message" />

    <TextView
        android:id="@+id/left_button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginEnd="16dp"
        android:textAllCaps="true"
        android:textColor="@color/colorAccent"
        android:textSize="18sp"
        android:textStyle="bold"
        app:layout_constraintBottom_toBottomOf="@+id/right_button"
        app:layout_constraintEnd_toStartOf="@+id/right_button"
        app:layout_constraintTop_toTopOf="@+id/right_button"
        tools:ignore="RtlCompat"
        tools:text="cancle" />

    <TextView
        android:id="@+id/right_button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginEnd="16dp"
        android:layout_marginBottom="16dp"
        android:textAllCaps="true"
        android:textColor="@color/colorAccent"
        android:textSize="18sp"
        android:textStyle="bold"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        tools:ignore="RtlCompat"
        tools:text="sure" />
</androidx.constraintlayout.widget.ConstraintLayout>
```
### 2.封装确认弹窗
```
class ConfirmDialogFragment : DialogFragment() {

    private var titleTv: TextView? = null
    private var messageTv: TextView? = null
    private var leftButton: TextView? = null
    private var rightButton: TextView? = null

    //左边按钮点击回调
    private var leftClicks: (() -> Unit)? = null
    //右边边按钮点击回调
    private var rightClicks: (() -> Unit)? = null
    //是否可以消失
    var cancelOutside: Boolean = true
    //弹窗标题
    var title: String? = null
    //弹窗内容
    var message: String? = null
    //左边按钮文字
    var leftValue: String? = null
    //左边按钮点击是否关闭弹窗
    var leftButtonDismissAfterClick = true
    //右边按钮文字
    var rightValue: String? = null
    //右边按钮点击是否关闭弹窗
    var rightButtonDismissAfterClick = true

    companion object {
        fun newInstance(): ConfirmDialogFragment {
            return ConfirmDialogFragment()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setStyle(DialogFragment.STYLE_NO_TITLE, android.R.style.Theme_Material_Light_Dialog)
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.dialog_custom, container).apply {
            titleTv = findViewById(R.id.title_tv)
            messageTv = findViewById(R.id.message_tv)
            leftButton = findViewById(R.id.left_button)
            rightButton = findViewById(R.id.right_button)
        }
        init()
        return view
    }

    private fun init() {
        dialog?.setCancelable(cancelOutside)

        title?.let { text ->
            titleTv?.visibility = View.VISIBLE
            titleTv?.text = text
        }

        message?.let { text ->
            messageTv?.visibility = View.VISIBLE
            messageTv?.text = text
        }

        leftClicks?.let { onClick ->
            leftButton?.text = leftValue
            leftButton?.visibility = View.VISIBLE
            leftButton?.setOnClickListener {
                onClick()
                if (leftButtonDismissAfterClick) {
                    dismissAllowingStateLoss()
                }
            }
        }

        rightClicks?.let { onClick ->
            rightButton?.text = rightValue
            rightButton?.setOnClickListener {
                onClick()
                if (rightButtonDismissAfterClick) {
                    dismissAllowingStateLoss()
                }
            }
        }
    }

    fun leftClicks(key: String = "取消", dismissAfterClick: Boolean = true, callback: () -> Unit) {
        leftValue = key
        leftButtonDismissAfterClick = dismissAfterClick
        leftClicks = callback
    }

    fun rightClicks(key: String = "确定", dismissAfterClick: Boolean = true, callback: () -> Unit) {
        rightValue = key
        rightButtonDismissAfterClick = dismissAfterClick
        rightClicks = callback
    }
}
```
### 3.给AppCompatActivity添加扩展方法
```
inline fun AppCompatActivity.showDialog(settings: ConfirmDialogFragment.() -> Unit) : ConfirmDialogFragment {
    val dialog = ConfirmDialogFragment.newInstance()
    dialog.apply(settings)
    val ft = this.supportFragmentManager.beginTransaction()
    val prev = this.supportFragmentManager.findFragmentByTag("confirm_dialog")
    if (prev != null) {
        ft.remove(prev)
    }
    ft.addToBackStack(null)
    dialog.show(ft, "dialog")
    return dialog
}
```

### 4.在Activity中通过扩展方法使用DSL风格的弹窗
```
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        findViewById<View>(R.id.button_dialog).setOnClickListener {
            showDialog {
                cancelOutside = true //可以取消
                title = "我是弹窗的标题"
                message =
                    "我是弹窗里面的内容,我是弹窗里面的内容,我是弹窗里面的内容,我是弹窗里面的内容"
                leftClicks("取消", true) {
                    toast("左边按钮被点击!")
                }
                rightClicks("确定", true) {
                    toast("右边按钮被点击!")
                }
            }
        }
    }
}
```
### 5.效果展示
![](/images/0141a2061aa7b2168233423babe50b32.webp)