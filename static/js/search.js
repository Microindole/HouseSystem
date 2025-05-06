document.addEventListener("DOMContentLoaded", () => {
    const searchButton = document.getElementById("search-button");
    const searchModal = document.getElementById("search-modal");
    const closeSearchModal = document.getElementById("close-search-modal");

    // 打开搜索悬浮窗
    searchButton.addEventListener("click", () => {
        searchModal.classList.remove("hidden");
    });

    // 关闭搜索悬浮窗
    closeSearchModal.addEventListener("click", () => {
        searchModal.classList.add("hidden");
    });

    // 点击悬浮窗外部关闭
    window.addEventListener("click", (event) => {
        if (event.target === searchModal) {
            searchModal.classList.add("hidden");
        }
    });
});