import {userState} from "@/store/userStore.js";
/**
 * @typedef {"text" | "video"} RecommendType
 * @typedef {"video" || "text" || ""} ContentType
 * @typedef {"rating" | "favorite" | ""} RatingType
 */


const rawUrl = "http://localhost:8040/api/";
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

export { disableScroll, enableScroll };

/**
 * @param {string} action 日志上传的行为（如 "study", "click"）
 * @param {string | null} contentType 上传的内容类别（当行为是 "click" 时，传入 "video" 或 "article" 以区分类型）
 * @param {string | null} contentKey 上传内容的关键词
 * @returns {Promise<void>}
 **/
export async function logActivity (action, contentType = null, contentKey = null){
    console.log(contentKey);
    const userId = userState.user.user_id;
    if (!userId) return;

    const data = {
        user_id: userId,
        action: action,
        content_type: contentType,
        content_key: contentKey,
    };

    try {
        const response = await fetch(rawUrl + "log-user-activity/",{
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

/**
 * 记录评分或收藏信息
 * @param {ContentType} contentType - 内容类型（只能是 "video" 或 "text"）
 * @param {RatingType} ratingType - 评分类型，只能是 "rating" 或 "favorite"
 * @param {Object} ratingObject - 评分对象
 * @returns {Promise<void>}
 */
export async function logRatings (
    contentType="",
    ratingType="",
    ratingObject={}
){
    // 如果用户未登录，直接结束
    const userId = userState.user.user_id;
    if (!userId || !contentType || !ratingType) return;

    // 确保 ratingObject 是对象，避免后续代码报错
    if (typeof ratingObject !== "object" || ratingObject === null || Object.values(ratingObject).length === 0) return;

    const backendUrl = rawUrl + 'log-user-rating/';
    const ratingList = [];

    if (ratingType === 'rating') {
        // 处理类型为评分 (rating) 的评价
        Object.entries(ratingObject).forEach(([key, value]) => {
            ratingList.push({[key]: value})
        })
    } else if (ratingType === 'favorite') {
        // 处理类型为收藏 (favorite) 的评价
        Object.entries(ratingObject).forEach(([key, value]) => {
            if (value !== 0) {
                ratingList.push(key)
            }
        })
    } else {
        // 未知评价类型，报错
        throw new Error(`不合法的评价类型:"${ratingType}"`);
    }

    // if (ratingList.length === 0) return;
    const response = await fetch(backendUrl,{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: userId,
            content_type: contentType,
            rating_type: ratingType,
            rating: ratingList
        })
    })

    if (!response.ok) throw response.message;

    const data = await response.json();
    console.log(data)
}

/**
 * 获取推荐内容 (图文 (text) | 视频 (video))
 * @param{RecommendType} recommendType
 * @returns {Promise<Array>}
 */
export async function getRecommendations (recommendType) {
    const userId = userState.user? userState.user.user_id : "";
    const recommendTypes = ["text", "video"];
    if (!recommendTypes.includes(recommendType)) throw new Error("未知推荐类型！");
    const response = await fetch(rawUrl + `get-recommend-items/?recommend_type=${recommendType}&user_id=${userId}`, {
        method: "GET",
    })

    if (!response.ok) throw response.message;

    const responseData = await response.json();
    return responseData.data;
}

/**
 * 加载用户历史评价
 * @param{ContentType} contentType
 * @param{RatingType} ratingType
 * @returns {Promise<Array>}
 */
export async function loadRatings(
    contentType,
    ratingType,
){
    const userId = userState.user? userState.user.user_id : "";
    if (!userId) throw new Error("用户不存在，不能查询历史记录");

    const response = await fetch(rawUrl + "get-user-rating/",{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: userId,
            content_type: contentType,
            rating_type: ratingType,
        })
    })

    if (!response.ok) throw response.message;
    const data = await response.json();
    return data.data;
}