export const PLANETS = [
    /* - - 太阳 - - */
    {
        name: "sun",
        displayName: "太阳",
        caption: "黄矮星",
        description: "太阳是我们太阳系的中心，也是地球生命的源泉。太阳核心温度约达1500万摄氏度（2700万华氏度）。",
        year: "2.3亿地球年",
        day: null,
        radius: 695508,
        meanTemp: 5500,
        timesLarger: 109.2,
        orbitalVelocity: 0,
        orbitObject: null,
        orbitalRadius: 0,
        scaledOrbitalRadius: 0,
        rotationVelocity: 2,
        orbitalInclination: 0,
        axialTilt: 7.25,
    },
    /* - - 太阳 - - */

    /* - - 行星 - - */
    {
        name: "mercury",
        displayName: "水星",
        caption: "类地行星",
        description: "水星是太阳系中最小且公转最快的行星。从水星表面看，太阳的视直径是地球视角的三倍。",
        year: "88个地球日",
        day: "59个地球日",
        moons: 0,
        distanceFromSun: 0.4,
        minTemp: -170,
        maxTemp: 449,
        radius: 2439.7,
        timesLarger: 0.38,
        orbitalVelocity: 47.9, 
        orbitObject: "太阳",
        orbitalRadius: 57909050, 
        scaledOrbitalRadius: 24, 
        rotationVelocity: 0.003,
        orbitalInclination: 7,
        axialTilt: 0.03,
    },
    {
        name: "venus",
        displayName: "金星",
        caption: "类地行星",
        description: "金星是太阳系最热的行星，其浓厚大气层能有效保存热量并引发剧烈的温室效应。",
        year: "225个地球日",
        day: "243个地球日",
        moons: 0,
        distanceFromSun: 0.7,
        meanTemp: 465,
        radius: 6051.8,
        timesLarger: 0.9,
        orbitalVelocity: 35.0, 
        orbitObject: "太阳",
        orbitalRadius: 108200000, 
        scaledOrbitalRadius: 31, 
        rotationVelocity: 0.003,
        orbitalInclination: 3.4,
        axialTilt: 177,
    },
    {
        name: "earth",
        displayName: "地球",
        caption: "我们的家园",
        description: "地球是太阳系中唯一表面存在液态水的行星。大气层不仅可供人类呼吸，还能抵御陨石的侵袭。",
        year: "365.25个地球日",
        day: "23.9小时",
        moons: 1,
        distanceFromSun: 1,
        minTemp: -89,
        maxTemp: 58,
        radius: 6371,
        timesLarger: -1,
        orbitalVelocity: 29.8,
        orbitObject: "太阳",
        orbitalRadius: 149600000, 
        scaledOrbitalRadius: 37,
        rotationVelocity: 0.46,
        orbitalInclination: 0,
        axialTilt: 23.44,
    },
    {
        name: "mars",
        displayName: "火星",
        caption: "类地行星",
        description: "火星是人类地外居住的最佳候选。它是唯一被人类派遣探测车的行星，毅力号采集的样本预计将于2033年抵达地球。",
        year: "1.88个地球年",
        day: "24.6小时",
        moons: 2,
        distanceFromSun: 1.5,
        minTemp: -125,
        maxTemp: 20,
        radius: 3389.5,
        timesLarger: 0.52,
        orbitalVelocity: 24.1, 
        orbitObject: "太阳",
        orbitalRadius: 227939366, 
        scaledOrbitalRadius: 45, 
        rotationVelocity: 0.241,
        orbitalInclination: 1.8,
        axialTilt: 25.19,
    },
    {
        name: "jupiter",
        displayName: "木星",
        caption: "巨行星",
        description: "木星是太阳系最大的行星。其大红斑风暴直径是地球的两倍，已持续肆虐超过百年。",
        year: "11.86个地球年",
        day: "9.93小时",
        moons: 79,
        distanceFromSun: 5.1,
        meanTemp: -110,
        radius: 69911,
        timesLarger: 11,
        orbitalVelocity: 24.1, 
        orbitObject: "太阳",
        orbitalRadius: 778412027, 
        scaledOrbitalRadius: 72, 
        rotationVelocity: 12.6,
        orbitalInclination: 1.3,
        axialTilt: 3.13,
    },
    {
        name: "saturn",
        displayName: "土星",
        caption: "环状行星",
        description: "土星并非唯一拥有行星环的星球，但其环系最为壮丽。土星环总计有7个主要环带。",
        year: "29.45个地球年",
        day: "10.7小时",
        moons: 82,
        distanceFromSun: 9.5,
        meanTemp: -140,
        radius: 58232,
        timesLarger: 9.1,
        orbitalVelocity: 9.7, 
        orbitObject: "太阳",
        orbitalRadius: 1433530000, 
        scaledOrbitalRadius: 108, 
        rotationVelocity: 9.87,
        orbitalInclination: 2.5,
        axialTilt: 26.73,
    },
    {
        name: "uranus",
        displayName: "天王星",
        caption: "冰巨星",
        description: "天王星是冰冻的气态巨行星，其自转轴倾斜角度极大，与金星同样呈现逆向自转。",
        year: "84个地球年",
        day: "17小时",
        moons: 27,
        distanceFromSun: 19.8,
        meanTemp: -195,
        radius: 25362,
        timesLarger: 4,
        orbitalVelocity: 6.8, 
        orbitObject: "太阳",
        orbitalRadius: 2870972000, 
        scaledOrbitalRadius: 145, 
        rotationVelocity: 2.59,
        orbitalInclination: 0.8,
        axialTilt: 82.23,
    },
    {
        name: "neptune",
        displayName: "海王星",
        caption: "蓝色巨行星",
        description: "海王星是太阳系中唯一肉眼不可见的行星。1989年NASA旅行者2号飞掠探测，目前仍是唯一近距离造访的探测器。",
        year: "164个地球年",
        day: "16小时",
        moons: 14,
        distanceFromSun: 30.1,
        meanTemp: -200,
        radius: 24622,
        timesLarger: 3.9,
        orbitalVelocity: 5.4, 
        orbitObject: "太阳",
        orbitalRadius: 4514953000, 
        scaledOrbitalRadius: 180, 
        rotationVelocity: 2.6,
        orbitalInclination: 1.8,
        axialTilt: 28.32,
    },
    /* - - 行星 - - */

    /* - - 卫星 - - */
    {
        name: "moon",
        displayName: "月球",
        caption: "今人不见古时月，今月曾经照古人",
        description: "月球是太阳系第五大卫星，迄今已有24位人类和超过105台机器人探测器造访。",
        year: "27天",
        radius: 1737.5,
        timesLarger: 0.27,
        distance: 385000,
        minTemp: -173,
        maxTemp: 127,
        orbitalVelocity: 1.022,
        orbitObject: "地球",
        orbitalRadius: 385000, 
        scaledOrbitalRadius: 3,
        rotationVelocity: 0.005,
        orbitalInclination: 5.1,
    },
    {
        name: "io",
        displayName: "木卫一（伊俄）",
        caption: "火山活动最活跃",
        description: "伊俄的火山活动极其剧烈，表面遍布熔岩湖。部分火山喷发规模之大，可通过望远镜从地球观测。",
        year: "42小时",
        radius: 1821.6,
        timesLarger: 0.285,
        distance: 262000,
        meanTemp: -143,
        orbitalVelocity: 17.334,
        orbitObject: "木星",
        orbitalRadius: 262000, 
        scaledOrbitalRadius: 10,
        rotationVelocity: 0.07,
        orbitalInclination: 0.05,
    },
    {
        name: "europa",
        displayName: "木卫二（欧罗巴）",
        caption: "潜在生命候选",
        description: "欧罗巴冰层下的咸水海洋含水量是地球的两倍，其冰冻地表之下可能存在生命形式。",
        year: "85小时",
        radius: 1560.8,
        timesLarger: 0.24,
        distance: 670900,
        minTemp: -220,
        maxTemp: -160,
        orbitalVelocity: 13.743,
        orbitObject: "木星",
        orbitalRadius: 670900, 
        scaledOrbitalRadius: 13,
        rotationVelocity: 0.03,
        orbitalInclination: 0.47,
    },
    {
        name: "ganymede",
        displayName: "木卫三（盖尼米德）",
        caption: "太阳系最大卫星",
        description: "盖尼米德体积大于水星，拥有地下海洋和稀薄氧大气层，是唯一具备自身磁场的卫星。",
        year: "172小时",
        radius: 2634.1,
        timesLarger: 0.416,
        distance: 1070400,
        minTemp: -180,
        maxTemp: -113,
        orbitalVelocity: 10.880,
        orbitObject: "木星",
        orbitalRadius: 1070400, 
        scaledOrbitalRadius: 15,
        rotationVelocity: 0.026,
        orbitalInclination: 0.2,
    },
    {
        name: "callisto",
        displayName: "木卫四（卡利斯托）",
        caption: "地质静止卫星",
        description: "卡利斯托是太阳系中陨击坑最密集的天体，表面几乎无地质活动，但冰层下可能存在海洋。",
        year: "17天",
        radius: 2410.3,
        timesLarger: 0.384,
        distance: 1883000,
        minTemp: -193,
        maxTemp: -108,
        orbitalVelocity: 8.204,
        orbitObject: "木星",
        orbitalRadius: 1883000, 
        scaledOrbitalRadius: 17.5,
        rotationVelocity: 0.01,
        orbitalInclination: 0.28,
    },
    {
        name: "titan",
        displayName: "土卫六（泰坦）",
        caption: "表面存在液态的卫星",
        description: "泰坦是太阳系唯一拥有云层和稠密大气的卫星，其地表湖泊由甲烷和乙烷构成。",
        year: "16天",
        radius: 2574.7,
        timesLarger: 0.4,
        distance: 1221865,
        meanTemp: -179,
        orbitalVelocity: 5.57,
        orbitObject: "土星",
        orbitalRadius: 1221865, 
        scaledOrbitalRadius: 16,
        rotationVelocity: 0.011,
        orbitalInclination: 0.33,
    },
    {
        name: "triton",
        displayName: "海卫一（特里同）",
        caption: "太阳系最冷天体",
        description: "特里同是太阳系最寒冷的卫星，也是唯一逆行公转的大型卫星。",
        year: "141小时",
        radius: 1353.4,
        timesLarger: 0.21,
        distance: 354759,
        meanTemp: -235,
        orbitalVelocity: 4.39,
        orbitObject: "海王星",
        orbitalRadius: 354759, 
        scaledOrbitalRadius: 7,
        rotationVelocity: 0.017,
        orbitalInclination: 156.885,
    },
    /* - - 卫星 - - */
]
