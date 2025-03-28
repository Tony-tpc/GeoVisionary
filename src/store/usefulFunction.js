import {userState} from "@/store/userStore.js";

// 禁用滚动
const disableScroll = () => {
    document.documentElement.style.overflow = "hidden"; // 禁止滚动
    document.documentElement.style.pointerEvents = "none"; // 禁止交互
}

// 恢复滚动
const enableScroll = () => {
    document.documentElement.style.overflow = "auto";
    document.documentElement.style.pointerEvents = "auto";
    document.documentElement.style.overflowX = "hidden";
}

// 传输日志信息
const logActivity = async (action, contentType = null) => {
    console.log(contentType)
    const userId = userState.user.user_id;
    if (!userId) return;

    const data = {
        user_id: userId,
        action: action,
        content_type: contentType,
    };

    try {
        const response = await fetch("http://localhost:8040/api/log-user-activity/",{
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json",
            }
        })
        const responseData = await response.json();
        console.log(responseData);
    } catch (e) {
        console.error(e);
    }
}

export { disableScroll, enableScroll, logActivity };