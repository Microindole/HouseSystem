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
    carousel.addEventListener('mouseenter', stopAutoPlay);
    carousel.addEventListener('mouseleave', startAutoPlay);
    
    // 启动自动播放
    startAutoPlay();
    
    // 初始化
    updateCarousel();
}

// 加载更多新闻功能
function initLoadMoreFunction() {
    const loadMoreBtn = document.getElementById('load-more-news');
    const totalNewsSpan = document.getElementById('total-news');
    let currentOffset = parseInt(totalNewsSpan?.textContent || 0);
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
                    // 添加新的新闻项
                    const carousel = document.getElementById('news-carousel');
                    data.news.forEach((news, index) => {
                        const newsElement = createNewsElement(news, currentOffset + index);
                        carousel.appendChild(newsElement);
                    });
                    
                    currentOffset += data.news.length;
                    if (totalNewsSpan) {
                        totalNewsSpan.textContent = currentOffset;
                    }
                    
                    // 重新初始化轮播（如果需要）
                    setTimeout(() => {
                        initNewsCarousel();
                    }, 100);
                    
                    // 如果没有更多新闻，隐藏按钮
                    if (!data.has_more) {
                        loadMoreBtn.style.display = 'none';
                    }
                } else {
                    loadMoreBtn.style.display = 'none';
                    showMessage('没有更多新闻了');
                }
            })
            .catch(error => {
                console.error('加载新闻失败:', error);
                showMessage('加载新闻失败，请稍后重试', 'error');
            })
            .finally(() => {
                isLoading = false;
                loadMoreBtn.textContent = '查看更多新闻';
                loadMoreBtn.disabled = false;
            });
    });
}

// 创建新闻元素
function createNewsElement(news, index) {
    const newsItem = document.createElement('div');
    newsItem.className = 'news-item';
    newsItem.setAttribute('data-index', index);
    
    const newsContent = document.createElement('div');
    newsContent.className = 'news-content';
    
    const title = document.createElement('h3');
    title.className = 'news-title';
    title.textContent = news.title;
    
    const desc = document.createElement('p');
    desc.className = 'news-desc';
    const description = news.desc || '暂无详细描述';
    desc.textContent = description.length > 100 ? description.substring(0, 100) + '...' : description;
    
    const footer = document.createElement('div');
    footer.className = 'news-footer';
    
    const date = document.createElement('span');
    date.className = 'news-date';
    date.textContent = formatDate(news.time);
    
    footer.appendChild(date);
    
    if (news.house_name) {
        const house = document.createElement('span');
        house.className = 'news-house';
        house.textContent = news.house_name;
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
        return dateString;
    }
}

// 显示消息
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.textContent = message;
    
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        background: ${type === 'error' ? '#f8d7da' : '#d1ecf1'};
        color: ${type === 'error' ? '#721c24' : '#0c5460'};
        border: 1px solid ${type === 'error' ? '#f5c6cb' : '#bee5eb'};
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    document.body.appendChild(messageDiv);
    
    // 淡入效果
    setTimeout(() => {
        messageDiv.style.opacity = '1';
    }, 10);
    
    // 自动移除
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 300);
    }, 3000);
}

// 导出函数供其他脚本使用
window.initNewsCarousel = initNewsCarousel;