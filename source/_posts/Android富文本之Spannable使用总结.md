---
title: Android富文本之Spannable使用总结
date: 2021-01-11
categories: 
  - Android开发
---

# 使用SpannableStringBuilder设置多个属性
```
    val builder = SpannableStringBuilder()
            builder.append("小明回复小红：你在干嘛呀。")

            val styleSpan = StyleSpan(Typeface.BOLD) //粗体

            builder.setSpan(styleSpan, 0, 2, Spannable.SPAN_EXCLUSIVE_INCLUSIVE)
            val styleSpan2 = StyleSpan(Typeface.ITALIC) //斜体

            builder.setSpan(styleSpan2, 4, 6, Spannable.SPAN_EXCLUSIVE_INCLUSIVE)
            val styleSpan3 = StyleSpan(Typeface.BOLD_ITALIC) //粗斜体

            builder.setSpan(styleSpan3, 7, builder.length, Spannable.SPAN_EXCLUSIVE_INCLUSIVE)
            textVideo.text = builder
```
# 追加新的 Spannable
```
   val builder = SpannableStringBuilder()
            // 将原有文本追加到 SpannableStringBuilder 中
            builder.append(textVideo.text)
            // 创建并设置所需的 Span 对象，如 ForegroundColorSpan、StyleSpan 等
            val foregroundColorSpan = ForegroundColorSpan(Color.RED)
            // 将新的 SpannableString 追加到 SpannableStringBuilder 中
            builder.setSpan(foregroundColorSpan, 0, 2, Spannable.SPAN_EXCLUSIVE_INCLUSIVE)
            // 更新 TextView 的内容
            textVideo.text = builder
            // 继续设置其他样式的 Spannable（可选）
            // ...
```
# 获取已经设置过的Spannable
```
       // 获取 TextView 中的文本内容
            val originalText  = textVideo.text
            if (originalText is Spanned) {
                // 将 CharSequence 转换为 Spanned 对象
                val spannedText = originalText as Spanned
                // 获取所有的 StyleSpan 类型的 Spannable 对象
                val spans = spannedText.getSpans(0, spannedText.length, Any::class.java)
                // 遍历所有的 StyleSpan 对象
                for (span in spans) {
                    // 在这里处理你想要的 Spannable 对象 符判断所需的 Spannable 类型
                    when (span) {
                        is StyleSpan -> {
                            // 处理 StyleSpan 类型的 Spannable 对象
                        }

                        is ForegroundColorSpan -> {
                            // 处理 ForegroundColorSpan 类型的 Spannable 对象
                        }

                        is BackgroundColorSpan -> {
                            // 处理 BackgroundColorSpan 类型的 Spannable 对象
                        }
                    }
                }
            }
```

# Spannable设置圆角背景
[利用SpannableString富文本方式设置圆角标签背景](https://juejin.cn/post/7133412865519648799)
[Android SpannableString 设置文字圆角背景](https://blog.csdn.net/zyldzs27/article/details/75091299)
[自定义圆角背景实现富文本标题展示(纯需求实现)](https://www.jianshu.com/p/a9269def0d23)
# 参考资料
[SpannableStringBuilder从简单到复杂的使用](https://blog.csdn.net/wuqingsen1/article/details/88577532)