---
title: AndroidJetpack分页组件paging3
---

# 一.什么是paging
Jetpack Paging提供了列表中分页数据加载的解决方案，已经被广泛熟知和使用，目前这个库升级到了3.0版本。Paging3 基于Kotlin协程进行了重写，兼容Flow、Rxjava、LiveData等多种API方式。
- 每一页的数据会缓存至内存中，以此保证处理分页数据时更有效的使用系统资源
- 内置请求重复数据删除功能，确保应用有效地使用网络带宽和系统资源
- 支持Kotlin协程、Flow、LiveData以及RxJava
- 内置错误处理支持，如刷新和重试功能。
# 二.引入依赖
```
//java
implementation 'androidx.paging:paging-runtime:3.0.0-alpha07'
//kotlin
implementation 'androidx.paging:paging-runtime-ktx:3.0.0-alpha07'
```
# 三.初步使用
### 1. 配置数据源
```
class ArticleDataSource : PagingSource<Int, DemoReqData.DataBean.DatasBean>() {
    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, DemoReqData.DataBean.DatasBean> {
        return try {
            //param.key页码未定义置为1 默认加载第1页数据。
            var currentPage = params.key ?: 1
            //仓库层请求数据
            Log.d("PagingSource", "请求第${currentPage}页")
            var demoReqData = RetrofitService.api.getArticleListData(currentPage)
            //数据获取成功返回LoadResult数据
            LoadResult.Page(
                    //需要加载的数据
                    data = demoReqData.data.datas,
                    //如果可以往上加载更多就设置该参数，否则不设置
                    prevKey = null,
                    //加载下一页的key 如果传null就说明到底了
                    nextKey = if (currentPage < demoReqData.data?.pageCount ?: 0) {
                        //当前页码 小于 总页码 页面加1
                        currentPage + 1
                    } else {
                        null
                    }
            )
        } catch (e: Exception) {
            Log.d("PagingSource", "----error--->${e.message}")
            LoadResult.Error(throwable = e)
        }
    }
}
```
### 2.生成可观察的数据集
观察数据集包括 LiveData 、Flow 以及 RxJava 中的 Observable 和 Flowable，其中，RxJava 需要单独引入扩展库去支持的。
```
class PagingViewModel : ViewModel()  {
    fun getArticleData(): Flow<PagingData<DemoReqData.DataBean.DatasBean>> = Pager(PagingConfig(pageSize = 1)) {
        ArticleDataSource()
    }.flow
}
```
- PagerConfig 可以提供分页的参数，比如每一页的加载数、初始加载数和最大数等。
- pagingSourceFactory 和 remoteMediator 都是数据源，我们使用其中的一个即可。



PagingData是数据源和RecyclerView Adapter之间的一个桥梁，每一页数据就是一个PagingData首先创建Flow<PagingData<XXX>>,可以通过Pager().flow()去实现
，可以传入PagingConfig到Pager中去设置一些分页的参数，比如：

- pageSize : 每一页的数据量

- prefetchDistance : 预取数据的距离，也就是距离最后一个item多远时开始加载下一页数据，默认是一页的数据量ppagesize，也就是说你获取到N页数据之后会自动开始获取第N+1页的数据，如果设置为0那么loadmore的效果就会消失

- initialLoadSize : 初始化加载的数量，默认为pagesize * 3


Flow<PagingData>有一个方便的cachedIn()方法，使我们可以将内容缓存Flow<PagingData>在CoroutineScope中，如果我们放在viewmodel中，
这样我们就可以在配置被更改之后，activity能够接收到原有的数据而不用重新开始获取，如果你要在flow上用map等操作符的时候，要确保cachedIn()是在最后面的，
如果没有缓存，那么在切换横竖屏的时候就会重新开始请求.


### 3.创建Adapter
用Paging库时需要recyclerview的adapter继承PagingDataAdapter
```
// 首先构造方法里需要传入diffutil的callback
class PagingWanAdapter : PagingDataAdapter<ArticleDataListData.DataBean.DatasBean, PagingWanAdapter.CustomViewHolder>(ArticleDiffCallback()) {
    override fun onBindViewHolder(holder: CustomViewHolder, position: Int) {
        val dataBean = getItem(position)
        holder.txtInfo.text = dataBean?.desc
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CustomViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.test_item_paging, parent, false)
        return CustomViewHolder(view)
    }

    class CustomViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val txtInfo: TextView = itemView.findViewById(R.id.txt_view)
    }
}

//这是判断item是否需要更新的部分
class ArticleDiffCallback : DiffUtil.ItemCallback<ArticleDataListData.DataBean.DatasBean>() {
    override fun areItemsTheSame(oldItem: ArticleDataListData.DataBean.DatasBean, newItem: ArticleDataListData.DataBean.DatasBean): Boolean {
        return oldItem.id == newItem.id
    }
    @SuppressLint("DiffUtilEquals")
    override fun areContentsTheSame(oldItem: ArticleDataListData.DataBean.DatasBean, newItem: ArticleDataListData.DataBean.DatasBean): Boolean {
        return oldItem == newItem
    }

}
```

paging3的设计理念是不建议对列表数据直接修改；而是对数据源进行操作，数据源的变化会自动更新到列表；
DiffUtil.ItemCallback 就是用来比对数据变化，从而决定更新对应UI；并执行条目动画；

- areItemsTheSame
比对新旧条目是否是同一个条目；
一般比对条目的唯一标示id即可，谨慎对待，如果条目不同则可能不会更新UI；

- areContentsTheSame
当上面的方法确定是同一个条目之后，这里比对条目的内容是否一样，不一样则会更新条目UI
建议这里的比对把UI展示的数据都写上，写漏了会导致UI不更新对应字段；

- getChangePayload （可选）
用于条目内部的局部刷新；

### 4.在界面中使用
```
class PagingHomeMainActivity : AppCompatActivity(), CoroutineScope by MainScope() {
    private val btnLoadData by lazy {
        findViewById<Button>(R.id.btn_load_data)
    }
    private val rlvData by lazy {
        findViewById<RecyclerView>(R.id.rlv_data)
    }
    private val mPagingWanAdapter: PagingWanAdapter by lazy {
        PagingWanAdapter()
    }
    private val mPagingViewModel: PagingViewModel by lazy {
        ViewModelProvider(this).get(PagingViewModel::class.java)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.test_activity_paging_home_main)
        rlvData.adapter = mPagingWanAdapter
        btnLoadData.setOnClickListener {
            launch {
                // 在activity中订阅pager的数据流，并且通过submitData方法把数据传给adapter
                mPagingViewModel?.getArticleData()?.collectLatest {
                    //  mPagingData=it
                // 把数据转化成itemview然后让adapter刷新ui
                    mPagingWanAdapter.submitData(it)
                }
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        cancel()
    }
}
```


# 四.注意事项
### 1.调整预取阈值
构建Pager时，使用到PagingConfig，其中有一个属性值为prefetchDistance，用于表示距离底部多少条数据开始预加载，设置0则表示滑到底部才加载。默认值为分页大小。
若要让用户对加载无感，适当增加预取阈值即可。比如调整到分页大小的5倍。
```
class PagingViewModel : ViewModel() {
    fun getArticleData() = Pager(PagingConfig(pageSize = 10, prefetchDistance = 50)) {
        ArticleDataSource()
    }.flow.cachedIn(viewModelScope)
}
```
### 2.Paging的加载状态


想要监听数据获取的状态在PagingDataAdapter里有两个方法

- addDataRefreshListener 这个方法是当新的PagingData被提交并且显示的回调

- addLoadStateListener这个相较于上面那个比较复杂，listener中的回调会返回一个CombinedLoadStates对象


上面我们在Activity中创建了dataRecycleViewAdapter来显示页面数据，我们可以使用addLoadStateListener方法添加加载状态的监听事件，如下所示：
```
mPagingWanAdapter.addLoadStateListener {
    when (it.refresh) {
        is LoadState.NotLoading -> {
            Log.d(TAG, "is NotLoading")
        }
        is LoadState.Loading -> {
            Log.d(TAG, "is Loading")
        }
        is LoadState.Error -> {
            Log.d(TAG, "is Error")
        }
    }
}
```

状态返回的参数 CombinedLoadStates，包含了
- refresh:刷新(在初始化刷新的使用)
- prepend:向前加载更多
- append:向后加载更多(在加载更多的时候使用)
- source:数据源
- mediator:调解员
每个行为分为3中状态：

- LoadState.Loading 加载中 (加载数据时候回调)
- LoadState.NotLoading 没有加载中 (加载数据前和加载数据完成后回调)
- LoadState.Error 加载失败 （加载数据失败回调）

也就是说如果监测的是it.refresh，当加载第二页第三页的时候，状态是监听不到的，这里只以it.refresh为例。

监听方式除了addLoadStateListener外，还可以直接使用loadStateFlow的方式，由于flow内部是一个挂起函数 所以我们需要在协程中执行(,代码如下所示:
```
lifecycleScope.launch {
    mPagingWanAdapter.loadStateFlow.collectLatest {
        when (it.refresh) {
            is LoadState.NotLoading -> {
 
            }
            is LoadState.Loading -> {
 
            }
            is LoadState.Error -> {
 
            }
        }
    }
}
```
### 3.刷新和重试
##### (1.) 使用第三方刷新库
在下拉刷新控制的下拉监听中直接调用adapter.refresh()方法就可以完成刷新了，那什么时候关闭刷新动画呢，需要调用adapter.loadStateFlow.collectLatest方法来监听
```
lifecycleScope.launchWhenCreated {
            @OptIn(ExperimentalCoroutinesApi::class)
            adapter.loadStateFlow.collectLatest {
                if(it.refresh !is LoadState.Loading){
                    refreshView.finishRefresh()
                }
            }
        }
```
收集流的状态，如果是不是Loading状态的说明加载完成了，可以关闭动画了。

##### (2.)使用PagingDataAdapter添加刷新和加载更多


|方法|使用|
|-|-|
|fun withLoadStateHeader(header: LoadStateAdapter<*> )                                    |头部添加状态适配器|
|fun withLoadStateFooter(footer: LoadStateAdapter<*> )                                    |底部添加状态适配器|
|fun withLoadStateHeaderAndFooter(header: LoadStateAdapter<*>, footer: LoadStateAdapter<*> )|头尾都添加状态适配器|


```
class ArticleLoadStateAdapter(val retrycallback: () -> Unit) : LoadStateAdapter<ArticleLoadStateAdapter.ArticleLoadStateViewHolder>() {


    class ArticleLoadStateViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val pbLoading = itemView.findViewById<ProgressBar>(R.id.pb_loading)
        val btnerror = itemView.findViewById<Button>(R.id.btn_error)
        val txtEnd = itemView.findViewById<TextView>(R.id.txt_end)
    }

    override fun onBindViewHolder(holder: ArticleLoadStateViewHolder, loadState: LoadState) {
        when (loadState) {
            is LoadState.Error -> {
                LogTest.d("LoadState.Error")
                holder.pbLoading.visibility = View.GONE
                holder.btnerror.visibility = View.VISIBLE
                holder.txtEnd.visibility = View.GONE
                holder.btnerror.setOnClickListener {
                    retrycallback()
                }
            }
            is LoadState.Loading -> {
                LogTest.d("LoadState.Loading")
                holder.pbLoading.visibility = View.VISIBLE
                holder.btnerror.visibility = View.GONE
                holder.txtEnd.visibility = View.GONE
            }
            is LoadState.NotLoading -> {
                LogTest.d("LoadState.NotLoading")
                holder.pbLoading.visibility = View.GONE
                holder.btnerror.visibility = View.GONE
                holder.txtEnd.visibility = View.VISIBLE
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, loadState: LoadState): ArticleLoadStateViewHolder {
        val rootView = LayoutInflater.from(parent.context).inflate(R.layout.test_item_loadstate, parent, false)
        return ArticleLoadStateViewHolder(rootView)
    }

//    override fun displayLoadStateAsItem(loadState: LoadState): Boolean {
//       // return super.displayLoadStateAsItem(loadState)
//        return true
//    }
}

```

参考资料:
[Android Paging3 LoadStateAdapter显示已加载完所有数据](https://juejin.cn/post/6911620350581145614)