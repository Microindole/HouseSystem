// 新闻展示功能
document.addEventListener('DOMContentLoaded', function() {
    initNewsCarousel();
    initLoadMoreFunction();
});
// 新闻轮播功能
function initNewsCarousel() {
    const carousel = document.getElementById('news-carousel');
    const newsItems = document.querySelectorAll('.news-item');
    const indicators = document.querySelectorAll('.indicator');
    const prevBtn = document.getElementById('prev-news');
    const nextBtn = document.getElementById('next-news');
    if (!carousel || newsItems.length === 0) return;
    const itemsPerView = 3;
    const totalSlides = Math.ceil(newsItems.length / itemsPerView);
    let currentSlide = 0;
    // 如果新闻少于等于3条，隐藏导航
    if (newsItems.length <= itemsPerView) {
        if (prevBtn) prevBtn.style.display = 'none';
        if (nextBtn) nextBtn.style.display = 'none';
        indicators.forEach(indicator => indicator.style.display = 'none');
        return;
    }
    // 更新轮播位置
    function updateCarousel() {
        const translateX = -(currentSlide * (100 / itemsPerView) * itemsPerView);
        carousel.style.transform = `translateX(${translateX}%)`;

        // 更新指示器
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentSlide);
        });

        // 更新按钮状态
        if (prevBtn) prevBtn.disabled = currentSlide === 0;
        if (nextBtn) nextBtn.disabled = currentSlide === totalSlides - 1;
    }
    // 下一张
    function nextSlide() {
        if (currentSlide < totalSlides - 1) {
            currentSlide++;
            updateCarousel();
        }
    }
    // 上一张
    function prevSlide() {
        if (currentSlide > 0) {
            currentSlide--;
            updateCarousel();
        }
    }
    // 跳转到指定幻灯片
    function goToSlide(slideIndex) {
        currentSlide = slideIndex;
        updateCarousel();
    }
    // 绑定事件
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);

    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => goToSlide(index));
    });
    // 自动播放（可选）
    let autoPlayInterval;
    function startAutoPlay() {
        autoPlayInterval = setInterval(() => {
            if (currentSlide === totalSlides - 1) {
                goToSlide(0);
            } else {
                nextSlide();
            }
        }, 5000);
    }

    function stopAutoPlay() {
        clearInterval(autoPlayInterval);
    }

    // 鼠标悬停时停止自动播放
    if (carousel) { // Ensure carousel exists before adding event listeners
        carousel.addEventListener('mouseenter', stopAutoPlay);
        carousel.addEventListener('mouseleave', startAutoPlay);
    }
    // 启动自动播放
    startAutoPlay();
    // 初始化
    updateCarousel();
}

// 加载更多新闻功能
function initLoadMoreFunction() {
    const loadMoreBtn = document.getElementById('load-more-news');
    const totalNewsSpan = document.getElementById('total-news');
    // currentOffset 应该从按钮的 data 属性或一个隐藏的 input 获取，或者从0开始
    let currentOffset = parseInt(loadMoreBtn?.dataset.offset || document.querySelectorAll('#news-carousel .news-item').length);
    let isLoading = false;
    if (!loadMoreBtn) return;
    loadMoreBtn.addEventListener('click', function() {
        if (isLoading) return;
        isLoading = true;
        loadMoreBtn.textContent = '加载中...';
        loadMoreBtn.disabled = true;
        fetch(`/house/load_more_news?start=${currentOffset}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.news && data.news.length > 0) {
                    const carousel = document.getElementById('news-carousel');
                    data.news.forEach((newsItemData, index) => { // Renamed 'news' to 'newsItemData'
                        const newsElement = createNewsElement(newsItemData, currentOffset + index);
                        if (carousel) carousel.appendChild(newsElement);
                    });
                    currentOffset += data.news.length;
                    if (loadMoreBtn) loadMoreBtn.dataset.offset = currentOffset; // Update offset
                    // 重新初始化轮播，但要考虑现有项
                    // initNewsCarousel(); // This might reset the view, better to update dynamically if possible or ensure it handles additions
                    if (!data.has_more) {
                        loadMoreBtn.style.display = 'none';
                    }
                } else {
                    loadMoreBtn.style.display = 'none';
                    // MODIFIED: 使用 window.showMessage
                    if (window.showMessage) {
                        window.showMessage('没有更多新闻了', 'info');
                    } else {
                        alert('没有更多新闻了');
                    }
                }
            })
            .catch(error => {
                console.error('加载新闻失败:', error);
                // MODIFIED: 使用 window.showMessage
                if (window.showMessage) {
                    window.showMessage('加载新闻失败，请稍后重试', 'error');
                } else {
                    alert('加载新闻失败，请稍后重试');
                }
            })
            .finally(() => {
                isLoading = false;
                loadMoreBtn.textContent = '查看更多新闻';
                loadMoreBtn.disabled = false;
            });
    });
}
// 创建新闻元素
function createNewsElement(newsData, index) { // Renamed 'news' to 'newsData'
    const newsItem = document.createElement('div');
    newsItem.className = 'news-item';
    newsItem.setAttribute('data-index', index);

    const newsContent = document.createElement('div');
    newsContent.className = 'news-content';

    const title = document.createElement('h3');
    title.className = 'news-title';
    title.textContent = newsData.title;

    const desc = document.createElement('p');
    desc.className = 'news-desc';
    const description = newsData.desc || '暂无详细描述';
    desc.textContent = description.length > 100 ? description.substring(0, 100) + '...' : description;

    const footer = document.createElement('div');
    footer.className = 'news-footer';

    const date = document.createElement('span');
    date.className = 'news-date';
    date.textContent = formatDate(newsData.time);

    footer.appendChild(date);

    if (newsData.house_name) {
        const house = document.createElement('span');
        house.className = 'news-house';
        // newsData.house_id 应该在后台传过来，以便生成链接
        if (newsData.house_id) {
            const houseLink = document.createElement('a');
            houseLink.href = `/house/${newsData.house_id}`; // 假设的房源详情页链接格式
            houseLink.textContent = newsData.house_name;
            house.appendChild(houseLink);
        } else {
            house.textContent = newsData.house_name;
        }
        footer.appendChild(house);
    }

    newsContent.appendChild(title);
    newsContent.appendChild(desc);
    newsContent.appendChild(footer);
    newsItem.appendChild(newsContent);

    return newsItem;
}

// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '未知时间';

    try {
        const date = new Date(dateString);
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${month}月${day}日`;
    } catch (e) {
        console.warn("Error formatting date:", dateString, e);
        // Try to return a more user-friendly part of the string if direct parsing fails
        if (typeof dateString === 'string' && dateString.includes(' ')) {
            return dateString.split(' ')[0]; // e.g., "YYYY-MM-DD"
        }
        return '日期格式错误';
    }
}

// // MODIFIED: 移除了本地的 showMessage 函数，将使用全局的 window.showMessage

// 导出函数供其他脚本使用（如果需要的话，但通常DOMContentLoaded中的函数是自执行的）
// 如果其他脚本确实需要调用 initNewsCarousel，可以保留它。
// window.initNewsCarousel = initNewsCarousel;