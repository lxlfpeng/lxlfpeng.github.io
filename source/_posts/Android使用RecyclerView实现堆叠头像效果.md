---
title: Android使用RecyclerView实现堆叠头像效果
---

第二个盖住第一个视图:
![在这里插入图片描述](/images/7d6d98125ebc92e8620abeb2bb46a2a1.webp)
item.layout
```
<?xml version="1.0" encoding="utf-8"?>
<androidx.cardview.widget.CardView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="24dp"
    android:layout_height="24dp"
    android:layout_marginRight="-10dp"
    android:elevation="0dp"
    app:cardBackgroundColor="@color/white"
    app:cardCornerRadius="12dp"
    app:cardElevation="0dp">

</androidx.cardview.widget.CardView>
```
adapter:
```
 if (holder.adapterPosition == 0) {
        setMargins(holder.itemView, 0, 0, 0, 0);
 }
```

```
    private fun setMargins(v: View, l: Int, t: Int, r: Int, b: Int) {
        if (v.layoutParams is ViewGroup.MarginLayoutParams) {
            val p = v.layoutParams as ViewGroup.MarginLayoutParams
            p.setMargins(l, t, r, b)
            v.requestLayout()
        }
    }
```
layout:
```
 LinearLayoutManager(requireContext(), LinearLayoutManager.HORIZONTAL, false)
```

第一个盖住第二个视图堆叠:
![在这里插入图片描述](/images/4792aa21b9842634fbf930034a82a3a5.webp)
```
<?xml version="1.0" encoding="utf-8"?>
<androidx.cardview.widget.CardView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="24dp"
    android:layout_height="24dp"
    android:layout_marginRight="-10dp"
    android:elevation="0dp"
    app:cardBackgroundColor="@color/white"
    app:cardCornerRadius="12dp"
    app:cardElevation="0dp">

</androidx.cardview.widget.CardView>
```
adapter:
```
 if (holder.adapterPosition == 0) {
        setMargins(holder.itemView, 0, 0, 0, 0);
 }
```

```
    private fun setMargins(v: View, l: Int, t: Int, r: Int, b: Int) {
        if (v.layoutParams is ViewGroup.MarginLayoutParams) {
            val p = v.layoutParams as ViewGroup.MarginLayoutParams
            p.setMargins(l, t, r, b)
            v.requestLayout()
        }
    }
```
layout:
```
 LinearLayoutManager(requireContext(), LinearLayoutManager.HORIZONTAL, true)
```
>注意:此时数据的顺序实际是反过来的如果需要正序排列需要对设置adapter的数据集合进行倒序排列.
