import { reactive, computed } from "vue";

// 用户状态（全局）
const userState = reactive({
    user: null,  // 初始用户信息
    access_token: "",
    refresh_token: "",
});

// 从 localStorage 读取用户信息
try {
    userState.user = JSON.parse(localStorage.getItem("user")) || null;
} catch (error) {
    console.error("解析用户信息失败", error);
    userState.user = null;
}

userState.access_token = localStorage.getItem("access_token") || "";
userState.refresh_token = localStorage.getItem("refresh_token") || "";

// 计算属性：判断用户是否已登录
const isLoggedIn = computed(() => !!userState.user && !!userState.access_token);

// 设置用户信息
const setUser = (response) => {
    if (!response || !response.user || !response.refresh_token || !response.access_token) {
        console.error("无效的用户数据", response);
        return;
    }

    userState.user = response.user;
    userState.access_token = response.access_token;
    userState.refresh_token = response.refresh_token;

    localStorage.setItem("user", JSON.stringify(response.user));
    localStorage.setItem("access_token", response.access_token);
    localStorage.setItem("refresh_token", response.refresh_token);
    localStorage.setItem("isApiavailable", true)
};

// 清除用户信息（退出登录）
const clearUser = () => {
    userState.user = null;
    userState.access_token = "";
    userState.refresh_token = "";
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("isApiavailable");
};

// 刷新 Access Token
const refreshAccessToken = async () => {
    if (!userState.refresh_token) {
        console.warn("无有效 refresh_token，无法刷新 access_token");
        clearUser(); // 退出登录
        return;
    }

    try {
        const response = await fetch("http://localhost:8040/api/token/refresh/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh_token: userState.refresh_token }),
        });

        if (!response.ok) {
            throw new Error("刷新 Token 失败");
        }

        const data = await response.json();

        if (data.access_token) {
            userState.access_token = data.access_token;
            localStorage.setItem("access_token", data.access_token);
            console.log("Access Token 已刷新");
        } else {
            throw new Error("未返回新的 Access Token");
        }
    } catch (error) {
        console.error("刷新 Access Token 失败", error);
        clearUser(); // 如果刷新失败，则强制退出登录
    }
};

// 自动登录
const autoLogin = async () => {
    if (!userState.access_token) {
        console.log('令牌不存在，无法自动登录')
        clearUser();
        return;
    }

    try {
        const response = await fetch("http://localhost:8040/api/token/auto-login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ access_token: userState.access_token }),
        });

        const data = await response.json();

        if (!response.ok) {
            console.log('access_token 失效，尝试刷新令牌...')
            await refreshAccessToken();
            if (!userState.user) {
                console.log('令牌已过期，无法自动登录')
                return;
            }
        } else {
            const userData = {user: data.user, access_token: userState.access_token, refresh_token: userState.refresh_token};
            setUser(userData);
            console.log("自动登录成功:", data.user);
        }
    } catch (error) {
        console.error("自动登录失败:", error);
        clearUser(); // 网络错误或其他问题时清除用户信息
    }
}

export { userState, isLoggedIn, setUser, clearUser, refreshAccessToken, autoLogin };