document.addEventListener('DOMContentLoaded', function () {
    const newsList = document.getElementById('news-list');
    const loadMoreButton = document.getElementById('load-more-news');
    let currentIndex = 7; // 当前显示的新闻数量

    if (loadMoreButton) {
        loadMoreButton.addEventListener('click', function () {
            fetch(`/load_more_news?start=${currentIndex}`)
                .then(response => response.json())
                .then(data => {
                    data.news.forEach(news => {
                        const newsItem = document.createElement('div');
                        newsItem.classList.add('news-item');
                        newsItem.innerHTML = `
                            <h3>${news.title}</h3>
                            <p>${news.desc}</p>
                            <p class="news-date">${news.time}</p>
                        `;
                        newsList.appendChild(newsItem);
                    });
                    currentIndex += data.news.length;
                    if (!data.has_more) {
                        loadMoreButton.style.display = 'none'; // 隐藏按钮
                    }
                });
        });
    }

    const newsItems = document.querySelectorAll('.news-item');
    currentIndex = 0;

    function showNextNews() {
        // 隐藏当前新闻
        newsItems[currentIndex].classList.remove('active');

        // 显示下一条新闻
        currentIndex = (currentIndex + 1) % newsItems.length;
        newsItems[currentIndex].classList.add('active');
    }

    // 初始化显示第一条新闻
    if (newsItems.length > 0) {
        newsItems[currentIndex].classList.add('active');
        // 每隔5秒切换新闻
        setInterval(showNextNews, 3700);
    }
});