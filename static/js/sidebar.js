document.addEventListener('DOMContentLoaded', function () {
    const userMenuButton = document.getElementById('user-menu-button');
    const userSidebar = document.getElementById('user-sidebar');
    const closeSidebarButton = document.getElementById('close-sidebar');

    // 显示侧边栏
    userMenuButton?.addEventListener('click', function () {
        userSidebar.classList.remove('hidden');
        userSidebar.classList.add('visible');
    });

    // 隐藏侧边栏
    closeSidebarButton?.addEventListener('click', function () {
        userSidebar.classList.remove('visible');
        userSidebar.classList.add('hidden');
    });

    // 点击页面其他地方关闭侧边栏
    document.addEventListener('click', function (event) {
        if (!userSidebar.contains(event.target) && event.target !== userMenuButton) {
            userSidebar.classList.remove('visible');
            userSidebar.classList.add('hidden');
        }
    });
});