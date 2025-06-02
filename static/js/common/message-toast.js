class MessageToast {
    constructor() {
        this.toastContainer = null;
        this.initialized = false;
    }

    /**
     * 初始化模块（延迟初始化）
     */
    init() {
        if (this.initialized) return;

        // 确保 DOM 已加载
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initContainer());
        } else {
            this.initContainer();
        }

        this.initialized = true;
    }

    /**
     * 初始化消息容器
     */
    initContainer() {
        // 如果已存在容器则直接返回
        if (document.querySelector('.toast-container')) {
            this.toastContainer = document.querySelector('.toast-container');
            return;
        }

        // 确保 body 存在
        if (!document.body) {
            setTimeout(() => this.initContainer(), 10);
            return;
        }

        // 创建消息容器
        this.toastContainer = document.createElement('div');
        this.toastContainer.className = 'toast-container';
        this.toastContainer.style.cssText = `
            position: fixed;
            top: 30px; /* MODIFIED: 原来是 20px, 向下移动一点 */
            right: 20px;
            z-index: 10000;
            pointer-events: none;
            max-width: 400px;
        `;
        document.body.appendChild(this.toastContainer);
    }

    /**
     * 确保已初始化
     */
    ensureInitialized() {
        if (!this.initialized) {
            this.init();
        }
        if (!this.toastContainer) {
            this.initContainer();
        }
    }

    /**
     * 显示消息提示
     * @param {string} message 消息内容
     * @param {string} type 消息类型: success, error, warning, info
     * @param {number} duration 显示时长(毫秒)，默认3000ms
     */
    show(message, type = 'success', duration = 3000) {
        this.ensureInitialized();

        // 创建消息元素
        const messageDiv = document.createElement('div');
        messageDiv.className = `message-toast message-${type}`;
        messageDiv.textContent = message;

        // 设置基础样式
        messageDiv.style.cssText = `
            padding: 15px 25px; /* MODIFIED: 原来是 12px 20px, 增大内边距使其更大 */
            margin-bottom: 10px;
            border-radius: 6px;
            color: white;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transform: translateX(100%);
            transition: all 0.3s ease;
            max-width: 100%;
            word-wrap: break-word;
            pointer-events: auto;
            cursor: pointer;
            font-size: 15px; /* MODIFIED: 原来是 14px, 增大字体使其更大 */
            line-height: 1.5;
            position: relative;
            overflow: hidden;
        `;

        // 设置不同类型的背景色
        this.setTypeStyle(messageDiv, type);

        // 添加关闭按钮
        this.addCloseButton(messageDiv); // addCloseButton 会调整 paddingRight

        // 添加到容器
        this.toastContainer.appendChild(messageDiv);

        // 显示动画
        setTimeout(() => {
            messageDiv.style.transform = 'translateX(0)';
        }, 100);

        // 自动隐藏
        const hideTimeout = setTimeout(() => {
            this.hide(messageDiv);
        }, duration);

        // 点击关闭
        messageDiv.addEventListener('click', () => {
            clearTimeout(hideTimeout);
            this.hide(messageDiv);
        });

        return messageDiv;
    }

    /**
     * 显示确认对话框
     * @param {string} message 确认消息
     * @param {Object} options 选项配置
     * @returns {Promise<boolean>} 用户选择结果
     */
    confirm(message, options = {}) {
        this.ensureInitialized();

        return new Promise((resolve) => {
            const {
                title = '确认操作',
                confirmText = '确定',
                cancelText = '取消',
                type = 'warning'
            } = options;

            // 创建遮罩层
            const overlay = document.createElement('div');
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 15000;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity 0.3s ease;
            `;

            // 创建对话框
            const dialog = document.createElement('div');
            dialog.style.cssText = `
                background: white;
                border-radius: 8px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                max-width: 400px;
                width: 90%;
                padding: 0;
                transform: scale(0.8);
                transition: transform 0.3s ease;
                overflow: hidden;
            `;

            // 创建标题栏
            const header = document.createElement('div');
            header.style.cssText = `
                padding: 20px 20px 15px;
                border-bottom: 1px solid #eee;
                display: flex;
                align-items: center;
                gap: 10px;
            `;

            // 添加图标
            const icon = document.createElement('span');
            icon.style.cssText = `
                font-size: 20px;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
            `;

            const iconStyles = {
                warning: { text: '⚠️', color: '#ffc107' },
                error: { text: '❌', color: '#dc3545' },
                info: { text: 'ℹ️', color: '#17a2b8' },
                success: { text: '✅', color: '#28a745' }
            };

            const iconConfig = iconStyles[type] || iconStyles.warning;
            icon.textContent = iconConfig.text;
            icon.style.color = iconConfig.color;

            const titleElement = document.createElement('h3');
            titleElement.textContent = title;
            titleElement.style.cssText = `
                margin: 0;
                font-size: 18px;
                color: #333;
                font-weight: 600;
            `;

            header.appendChild(icon);
            header.appendChild(titleElement);

            // 创建内容区
            const content = document.createElement('div');
            content.style.cssText = `
                padding: 20px;
                color: #666;
                line-height: 1.6;
                font-size: 14px;
            `;
            content.textContent = message;

            // 创建按钮区
            const buttonArea = document.createElement('div');
            buttonArea.style.cssText = `
                padding: 15px 20px 20px;
                display: flex;
                justify-content: flex-end;
                gap: 12px;
                border-top: 1px solid #f0f0f0;
            `;

            // 取消按钮（如果需要）
            if (cancelText) {
                const cancelButton = document.createElement('button');
                cancelButton.textContent = cancelText;
                cancelButton.style.cssText = `
                    padding: 8px 20px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background: white;
                    color: #666;
                    cursor: pointer;
                    font-size: 14px;
                    transition: all 0.2s ease;
                `;
                cancelButton.addEventListener('mouseenter', () => {
                    cancelButton.style.background = '#f8f9fa';
                    cancelButton.style.borderColor = '#adb5bd';
                });
                cancelButton.addEventListener('mouseleave', () => {
                    cancelButton.style.background = 'white';
                    cancelButton.style.borderColor = '#ddd';
                });
                cancelButton.addEventListener('click', () => handleClose(false));
                buttonArea.appendChild(cancelButton);
            }

            // 确认按钮
            const confirmButton = document.createElement('button');
            confirmButton.textContent = confirmText;

            const buttonStyles = {
                warning: '#ffc107',
                error: '#dc3545',
                info: '#17a2b8',
                success: '#28a745'
            };

            const buttonColor = buttonStyles[type] || buttonStyles.warning;
            confirmButton.style.cssText = `
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                background: ${buttonColor};
                color: white;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                transition: all 0.2s ease;
            `;
            confirmButton.addEventListener('mouseenter', () => {
                confirmButton.style.transform = 'translateY(-1px)';
                confirmButton.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
            });
            confirmButton.addEventListener('mouseleave', () => {
                confirmButton.style.transform = 'translateY(0)';
                confirmButton.style.boxShadow = 'none';
            });

            // 组装对话框
            dialog.appendChild(header);
            dialog.appendChild(content);
            buttonArea.appendChild(confirmButton);
            dialog.appendChild(buttonArea);
            overlay.appendChild(dialog);

            // 事件处理
            const handleClose = (result) => {
                overlay.style.opacity = '0';
                dialog.style.transform = 'scale(0.8)';
                setTimeout(() => {
                    if (document.body.contains(overlay)) {
                        document.body.removeChild(overlay);
                    }
                    resolve(result);
                }, 300);
            };

            confirmButton.addEventListener('click', () => handleClose(true));

            // 点击遮罩层关闭
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    handleClose(false);
                }
            });

            // ESC 键关闭
            const handleKeydown = (e) => {
                if (e.key === 'Escape') {
                    document.removeEventListener('keydown', handleKeydown);
                    handleClose(false);
                }
            };
            document.addEventListener('keydown', handleKeydown);

            // 显示对话框
            document.body.appendChild(overlay);

            // 动画显示
            setTimeout(() => {
                overlay.style.opacity = '1';
                dialog.style.transform = 'scale(1)';
            }, 10);

            // 聚焦到确认按钮
            setTimeout(() => {
                confirmButton.focus();
            }, 100);
        });
    }

    /**
     * 显示警告提示（替代 alert）
     * @param {string} message 警告消息
     * @param {Object} options 选项配置
     * @returns {Promise<void>}
     */
    alert(message, options = {}) {
        return new Promise((resolve) => {
            const {
                title = '提示',
                buttonText = '确定',
                type = 'info'
            } = options;

            this.confirm(message, {
                title,
                confirmText: buttonText,
                cancelText: null, // 不显示取消按钮
                type
            }).then(() => resolve());
        });
    }

    /**
     * 设置消息类型样式
     * @param {HTMLElement} element 消息元素
     * @param {string} type 消息类型
     */
    setTypeStyle(element, type) {
        const styles = {
            success: 'linear-gradient(135deg, #28a745, #20c997)',
            error: 'linear-gradient(135deg, #dc3545, #e74c3c)',
            warning: 'linear-gradient(135deg, #ffc107, #fd7e14)',
            info: 'linear-gradient(135deg, #17a2b8, #007bff)'
        };

        element.style.background = styles[type] || styles.info;
    }

    /**
     * 添加关闭按钮
     * @param {HTMLElement} element 消息元素
     */
    addCloseButton(element) {
        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            position: absolute;
            top: 8px; /* 调整关闭按钮位置以适应新的padding */
            right: 12px;
            font-size: 20px; /* 可选：稍微增大关闭按钮 */
            font-weight: bold;
            cursor: pointer;
            opacity: 0.8;
        `;
        closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.opacity = '1';
        });
        closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.opacity = '0.8';
        });
        element.appendChild(closeBtn);

        // 为了给关闭按钮留空间，调整padding-right
        // 基于新的 padding: 15px 25px; 和关闭按钮尺寸，40px 可能仍然合适
        // 如果关闭按钮变大很多，或者希望右侧有更多空间，可以增加这个值
        element.style.paddingRight = '40px';
    }

    /**
     * 隐藏消息
     * @param {HTMLElement} element 消息元素
     */
    hide(element) {
        element.style.transform = 'translateX(100%)';
        element.style.opacity = '0';

        setTimeout(() => {
            if (element.parentNode) {
                element.parentNode.removeChild(element);
            }
        }, 300);
    }

    /**
     * 清除所有消息
     */
    clear() {
        if (this.toastContainer) {
            const messages = this.toastContainer.querySelectorAll('.message-toast');
            messages.forEach(msg => this.hide(msg));
        }
    }

    // 便捷方法
    success(message, duration) {
        return this.show(message, 'success', duration);
    }

    error(message, duration) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration) {
        return this.show(message, 'info', duration);
    }
}

// 模块化初始化函数
function initMessageToast() {
    // 创建全局实例（如果不存在）
    if (typeof window.messageToast === 'undefined') {
        window.messageToast = new MessageToast();
        window.messageToast.init();
    }

    // 兼容旧版本的 showMessage 函数
    if (typeof window.showMessage === 'undefined') {
        window.showMessage = function(message, type = 'success', duration = 3000) {
            return window.messageToast.show(message, type, duration);
        };
    }

    // 替代原生 alert 和 confirm 函数
    if (typeof window.showAlert === 'undefined') {
        window.showAlert = function(message, options = {}) {
            return window.messageToast.alert(message, options);
        };
    }

    if (typeof window.showConfirm === 'undefined') {
        window.showConfirm = function(message, options = {}) {
            return window.messageToast.confirm(message, options);
        };
    }

    return window.messageToast;
}

// 自动初始化（当脚本加载时）
if (typeof window !== 'undefined') {
    // 浏览器环境
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMessageToast);
    } else {
        initMessageToast();
    }
}

// 导出（支持多种模块系统）
if (typeof module !== 'undefined' && module.exports) {
    // CommonJS (Node.js)
    module.exports = MessageToast;
} else if (typeof define === 'function' && define.amd) {
    // AMD (RequireJS)
    define([], function() { return MessageToast; });
} else if (typeof window !== 'undefined') {
    // 浏览器全局变量
    window.MessageToast = MessageToast;
    window.initMessageToast = initMessageToast;
}