document.addEventListener('DOMContentLoaded', function () {
    const userMenuButton = document.getElementById('user-menu-button');
    const userSidebar = document.getElementById('user-sidebar');
    const closeSidebarButton = document.getElementById('close-sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');

    // 显示侧边栏
    if (userMenuButton) {
        userMenuButton.addEventListener('click', function () {
            userSidebar.classList.remove('hidden');
            userSidebar.classList.add('visible');
            sidebarOverlay.classList.add('visible');
            document.body.style.overflow = 'hidden';
        });
    }

    // 隐藏侧边栏
    function hideSidebar() {
        userSidebar.classList.remove('visible');
        userSidebar.classList.add('hidden');
        sidebarOverlay.classList.remove('visible');
        document.body.style.overflow = '';
    }

    // 关闭按钮
    if (closeSidebarButton) {
        closeSidebarButton.addEventListener('click', hideSidebar);
    }

    // 点击遮罩关闭
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', hideSidebar);
    }

    // ESC键关闭
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && userSidebar && userSidebar.classList.contains('visible')) {
            hideSidebar();
        }
    });

    // 防止侧边栏内部点击冒泡
    if (userSidebar) {
        userSidebar.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
});