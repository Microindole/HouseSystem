// 新闻展示功能
document.addEventListener('DOMContentLoaded', function() {
    const newsCarousel = document.getElementById('news-carousel');
    const prevBtn = document.getElementById('prev-news');
    const nextBtn = document.getElementById('next-news');
    const indicators = document.querySelectorAll('.indicator');
    const viewMoreBtn = document.getElementById('view-more-news');
    
    if (!newsCarousel) return;
    
    let currentSlide = 0;
    const totalSlides = Math.ceil(newsCarousel.children.length / 3);
    
    function showSlide(index) {
        if (index < 0 || index >= totalSlides) return;
        
        currentSlide = index;
        const translateX = -index * 100;
        newsCarousel.style.transform = `translateX(${translateX}%)`;
        
        // 更新指示器
        indicators.forEach((indicator, i) => {
            indicator.classList.toggle('active', i === currentSlide);
        });
        
        // 更新按钮状态
        prevBtn.disabled = currentSlide === 0;
        nextBtn.disabled = currentSlide === totalSlides - 1;
    }
    
    // 上一页按钮
    prevBtn.addEventListener('click', () => {
        if (currentSlide > 0) {
            showSlide(currentSlide - 1);
        }
    });
    
    // 下一页按钮
    nextBtn.addEventListener('click', () => {
        if (currentSlide < totalSlides - 1) {
            showSlide(currentSlide + 1);
        }
    });
    
    // 指示器点击
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            showSlide(index);
        });
    });
    
    // 自动轮播
    let autoSlideInterval = setInterval(() => {
        if (currentSlide < totalSlides - 1) {
            showSlide(currentSlide + 1);
        } else {
            showSlide(0);
        }
    }, 5000);
    
    // 鼠标悬停暂停自动轮播
    newsCarousel.addEventListener('mouseenter', () => {
        clearInterval(autoSlideInterval);
    });
    
    newsCarousel.addEventListener('mouseleave', () => {
        autoSlideInterval = setInterval(() => {
            if (currentSlide < totalSlides - 1) {
                showSlide(currentSlide + 1);
            } else {
                showSlide(0);
            }
        }, 5000);
    });
    
    // 查看更多新闻按钮点击事件（如果需要额外处理）
    if (viewMoreBtn) {
        viewMoreBtn.addEventListener('click', function(e) {
            // 如果需要在跳转前做一些处理，可以在这里添加
            console.log('跳转到新闻列表页面');
            // 注意：不要 preventDefault()，让 <a> 标签正常跳转
        });
    }
    
    // 新闻标题点击跳转
    const newsTitles = document.querySelectorAll('.news-title a');
    newsTitles.forEach(title => {
        title.addEventListener('click', function(e) {
            // 添加点击效果
            this.style.color = '#4f46e5';
        });
    });
    
    // 阅读全文按钮点击
    const readMoreBtns = document.querySelectorAll('.read-more');
    readMoreBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // 添加点击效果
            this.style.opacity = '0.7';
            setTimeout(() => {
                this.style.opacity = '1';
            }, 200);
        });
    });
});