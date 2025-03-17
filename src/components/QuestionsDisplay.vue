<template>
  <div class="question-display card" v-loading="props.isLoading">
    <!-- 题目序号导航 -->
    <div class="question-nav">
      <button
          v-for="(q, index) in questions.slice(currentPage * 10, (currentPage + 1) * 10)"
          :class="{ 'correct': isTrue(index + currentPage * 10),
                    'wrong': isWrong(index + currentPage * 10),
                    'active': index + currentPage * 10 === currentIndex }"
          @click="() => {
            currentIndex = index + currentPage * 10;
            reset();
          }"
      >
        {{ index + 1 + currentPage * 10 }}
      </button>
    </div>

    <!-- 题目展示 -->
    <div class="question">
      <!--  题目图片（如果存在）  -->
      <h3>{{ currentQuestion.text }}</h3>
      <h2>
        <img v-if="currentQuestion.image" :src="currentQuestion.image" @click="openImage(currentQuestion.image)" />
      </h2>

      <!-- 如果是大题，循环渲染子题 -->
      <template v-if="currentQuestion.sub_questions">
        <div v-for="(subQ, index) in currentQuestion.sub_questions" :key="subQ.id" class="sub-question">
          <h4>{{ subQ.text }}</h4>

          <!-- 单选框 -->
          <div v-if="subQ.type === 'single'">
            <el-radio-group v-model="selectedOptions[subQ.id]" class="radio-group">
              <el-radio v-for="(option, key) in subQ.options"
                        :value="option"
                        :label="option"
                        :disabled="hasAnswered(subQ.id)"
                        class="radio-option"
                        :class="{
                          'wrong-answer': shouldShowWrongCss(key,subQ.id),
                          'is-checked': isSelected(key,subQ.id),
                        }"
              >
                <span>{{ key }}. {{ option }}</span>
                <span v-if="isSelected(key,subQ.id)">
                  &nbsp;{{ answerIncludeKey(key,subQ.id) ? '✅' : '❌' }}
                </span>
                <span v-if="shouldShowCorrectAnswer(key,subQ.id)"
                      style="color:#279043">
                &nbsp;{{ '✅（正确答案）' }}
                </span>
              </el-radio>
            </el-radio-group>
          </div>

          <!-- 多选框 -->
          <div v-if="subQ.type === 'multiple'">
            <el-checkbox-group v-model="selectedOptions[subQ.id]" class="checkbox-group">
              <el-checkbox v-for="(option, key) in subQ.options"
                           :value="option"
                           :label="option"
                           :disabled="hasAnswered(subQ.id)"
                           class="checkbox-option"
                           :class="{
                             'wrong-answer': shouldShowWrongCss(key,subQ.id),
                             'is-checked': isSelected(key,subQ.id),
                           }"
              >
                <span>{{ key }}. {{ option }}</span>
                <span v-if="isSelected(key,subQ.id)">
                  &nbsp;{{ answerIncludeKey(key,subQ.id) ? '✅' : '❌' }}
                </span>
                <span v-if="shouldShowCorrectAnswer(key,subQ.id)"
                      style="color:#279043">
                &nbsp;{{ '✅（正确答案）' }}
                </span>
              </el-checkbox>
            </el-checkbox-group>
          </div>

          <!-- 答案和解析 -->
          <div class="explanation">
            <p v-if="isCorrect(subQ.id)" class="explanation-correct">回答正确</p>
            <p v-else class="explanation-wrong">正确答案：{{ currentQuestion.sub_questions[index].answer.join(', ') }}</p>
            <p>解析：{{ currentQuestion.sub_questions[index].explanation }}</p>
          </div>
        </div>
      </template>

      <template v-else>
        <!-- 单选框 -->
        <div v-if="currentQuestion.type === 'single'">
          <el-radio-group v-model="selectedOptions[currentQuestion.id]" class="radio-group">
            <!--  option 存储选项内容，key 存储选项  -->
            <!--  selectedOptions 存储选项内容，currentQuestions.answer 和 userAnswers[index].selected 均存储选项   -->
            <el-radio v-for="(option,key) in currentQuestion.options"
                      :value="option"
                      :label="option"
                      class="radio-option"
                      :disabled="hasAnswered()"
                      :class="{
                        'wrong-answer': shouldShowWrongCss(key),
                        'is-checked': isSelected(key),
                      }"
            >
              <span>{{ key }}. {{ option }}</span>
              <span v-if="isSelected(key)">
                &nbsp;{{ isCorrect() ? '✅' : '❌' }}
              </span>
              <span v-if="shouldShowCorrectAnswer(key)"
                    style="color:#279043">
                &nbsp;{{ '✅（正确答案）' }}
              </span>
            </el-radio>
          </el-radio-group>
        </div>

        <!-- 多选框 -->
        <div v-if="currentQuestion.type === 'multiple'">
          <el-checkbox-group v-model="selectedOptions[currentQuestion.id]" class="checkbox-group">
            <!--  option 存储选项内容，key 存储选项  -->
            <el-checkbox v-for="(option,key) in currentQuestion.options"
                         :value="option"
                         :label="option"
                         :disabled="hasAnswered()"
                         class="checkbox-option"
                         :class="{
                          'is-checked': isSelected(key),
                          'wrong-answer': shouldShowWrongCss(key),
                         }"
            >
              <span>{{ key }}. {{ option }}</span>
              <span v-if="isSelected(key)">
                &nbsp;{{ currentQuestion.answer.includes(key) ? '✅' : '❌' }}
              </span>
              <span v-if="shouldShowCorrectAnswer(key)"
                    style="color:#279043">
                &nbsp;{{ '✅（正确答案）' }}
              </span>
            </el-checkbox>
          </el-checkbox-group>
        </div>
      </template>
    </div>

    <!-- 按钮 -->
    <div class="buttons">
      <el-button @click="prevQuestion" :disabled="currentIndex === 0">上一题</el-button>
      <el-button @click="submitAnswer" :disabled="submitted">提交</el-button>
      <el-button @click="nextQuestion" :disabled="currentIndex === questions.length - 1">下一题</el-button>
    </div>

    <!-- 答案与解析 -->
    <div class="explanation" v-if="!currentQuestion.sub_questions">
      <p v-if="isCorrect()" class="explanation-correct">回答正确</p>
      <p v-else class="explanation-wrong">正确答案：{{ currentQuestion.answer.join(', ') }}</p>
      <p>解析：{{ currentQuestion.explanation }}</p>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-button @click="prevPage" :disabled="currentPage === 0">上一页</el-button>
      <el-button @click="nextPage" :disabled="(currentPage + 1) * 10 >= questions.length">下一页</el-button>
    </div>

    <!-- 提示 -->
    <div class="unfinished-prompt">
      <el-dialog
          v-model="dialogVisible"
          title="提示"
          width="500"
          :before-close="handleClose"
      >
        <span>还有题目没做完呢，不要太着急哦！</span>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="dialogVisible = false">关闭</el-button>
            <el-button type="primary" @click="dialogVisible = false">
              确认
            </el-button>
          </div>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import {gsap} from "gsap";
import { ElMessageBox } from 'element-plus'
// 传入参数
const props = defineProps({
  questions: {
    type: Array,
    default: () => [
      {
        id: 1, text: "地球的公转周期是多少天？", type: "single",
        options: { A: "365天", B: "366天", C: "360天" }, answer: ["A"],
        explanation: "地球公转周期约为365.25天。"
      },
      {
        id: 2, text: "太阳系的行星有哪些？", type: "multiple",
        options: { A: "地球", B: "火星", C: "冥王星" }, answer: ["A", "B"],
        explanation: "冥王星已被降级为矮行星。"
      },
      {
        id: 3, text: "地球的公转周期是多少天？", type: "single",
        options: { A: "365天", B: "366天", C: "360天" }, answer: ["A"],
        explanation: "地球公转周期约为365.25天。"
      },
      {
        id: 4, text: "太阳系的行星有哪些？", type: "multiple",
        options: { A: "地球", B: "火星", C: "冥王星" }, answer: ["A", "B"],
        explanation: "冥王星已被降级为矮行星。"
      },
      {
        id: 5, text: "地球的公转周期是多少天？", type: "single",
        options: { A: "365天", B: "366天", C: "360天" }, answer: ["A"],
        explanation: "地球公转周期约为365.25天。"
      },
      {
        id: 6, text: "太阳系的行星有哪些？", type: "multiple",
        options: { A: "地球", B: "火星", C: "冥王星" }, answer: ["A", "B"],
        explanation: "冥王星已被降级为矮行星。"
      },
      {
        id: 7, text: "地球的公转周期是多少天？", type: "single",
        options: { A: "365天", B: "366天", C: "360天" }, answer: ["A"],
        explanation: "地球公转周期约为365.25天。"
      },
      {
        id: 8, text: "太阳系的行星有哪些？", type: "multiple",
        options: { A: "地球", B: "火星", C: "冥王星" }, answer: ["A", "B"],
        explanation: "冥王星已被降级为矮行星。"
      },
      {
        id: 9, text: "地球的公转周期是多少天？", type: "single",
        options: { A: "365天", B: "366天", C: "360天" }, answer: ["A"],
        explanation: "地球公转周期约为365.25天。"
      },

      // ❸ 大题（含多个小题）
      {
        id: 10, text: "苏州工业园区是中国和新加坡两国政府间的重要合作项目。图1示意苏州工业园区中的中新合作区1994-2000年实施的功能区布局规划。规划思路是通过基础设施建设，优先开发工业用地；当人口集聚到一定规模后，加大开发居住用地；当人口进一步集聚后，再重点开发商业用地。据此完成下面小题。",
        image: '../src/assets/test/img.png',
        sub_questions: [
          {
            id: "10-1",
            text: "1. 中新合作区的工业区对商业区形成强力支撑的原因是工业区带动了（    ）\n"  +
                "①人口集聚    ②服务业集聚    ③人才集聚    ④技术集聚",
            type: "single",
            options: { A: "①②", B: "②③", C: "③④", D: "①④" },
            answer: ["A"],
            explanation: "结合所学知识，阅读图文材料可知，中新合作区的工业区的建立，将吸引大量的人口集中到居住区，对商业区带来大量的人流量，①正确;同时工业区就业人数数量大，可以带动服务业的发展，促进服务业在商业区集中，②正确;人才的集聚和技术的集聚对商业区的影响起不到支撑作用，③和④错误。"
          },
          {
            id: "10-2",
            text: "2. 住宅区规划在商业区和工业区之间，主要有利于（    ）",
            type: "single",
            options: { A: "节约土地资源", B: "增加绿地面积", C: "组织内外交通", D: "完善市政设施" },
            answer: ["C"],
            explanation: "结合所学知识，阅读图文材料可知，住宅区规划在商业区和工业区之间，并不能节约土地资源，A错误;住宅区范围较大，位于两者之间，绿化带的范围大小主要看设计思想，于位置关系不大，B错误;图中显示城市主干道贯穿住宅区、商业区和工业区，而住宅区位于中间，主要是为了加强居民工作和休闲的交通，因此主要有利于组织内外交通，C正确;住宅区所处任何位置都可以完善市政设施，因此主要目的不是完善市政设施，D错误。"
          },
          {
            id: "10-3",
            text: "3. 苏州老城主干道向东延伸串联中新合作区各功能区，体现的布局思路是（    ）\n" +
                "①轴向发展    ②职住平衡    ③均衡发展    ④地租递减",
            type: "single",
            options: { A: "①③", B: "②④", C: "②③", D: "①④" },
            answer: ["A"],
            explanation: "结合所学知识，阅读图文材料可知，图中显示其整体功能分区明确，商业区位于老城区和住宅区之间，体现功能中心地位，同时向城市主干道方向发展，最终延伸到最外围的工业区，体现其轴向发展的布局思想，①正确;老城区主干道延伸串联各功能区后，老城区在工业区居住人员较远，没有体现职住平衡的思路，②错误;将各功能区串联后，可以促进新区的发展，平衡老城和新城共同发展，③正确;图中显示老城区地租较高，串联新合作区功能各功能区后，地租逐渐升高的是商业区，且商业区地租将高于老城区，并未体现地租递减的思路，④错误。"
          }
        ]
      }
    ],
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

// 题目对象
const questions = ref(props.questions);

const currentIndex = ref(0); // 题号
const currentPage = ref(0); // 页码
const submitted = ref(false); // 是否提交
const selectedOptions = ref({}); // 选中选项内容
const userAnswers = ref({}) // 用户回答对象
const dialogVisible = ref(false) // 是否显示对话框

// 当前问题对象
const currentQuestion = computed(() => questions.value[currentIndex.value]);

// 当前题目是否已经作答
const hasAnswered = (index = currentIndex.value) => {
  if (index === currentIndex.value) {
    // 单题
    return userAnswers.value[currentIndex.value] !== undefined
  } else {
    // 含有小题
    return userAnswers.value[currentIndex.value] ? userAnswers.value[currentIndex.value][index] !== undefined : false;
  }
};

// 判断某个选项是否被用户选择
const isSelected = (key,index = currentIndex.value) => {
  if (index === currentIndex.value) {
    // 单题
    return hasAnswered(index) ? userAnswers.value[currentIndex.value].selected.includes(key) : false;
  } else {
    // 含有小题
    return hasAnswered(index) ? userAnswers.value[currentIndex.value] ? userAnswers.value[currentIndex.value][index].selected.includes(key) : false : false;
  }
};

// 导航栏正确样式
const isTrue = (index) => {
  const question = questions.value[index];
  if (!question.sub_questions) {
    // 单题
    return userAnswers.value[index]?.correct === true;
  } else {
    // 大题
    let correct = true;
    if (userAnswers.value[index]) {
      Object.values(userAnswers.value[index]).forEach((item) => {
        if (item.correct === false) {
          correct = false;
        }
      });
      return correct;
    }
    return false;
  }
};

// 导航栏错误样式
const isWrong = (index) => {
  const question = questions.value[index];
  if (!question.sub_questions) {
    // 单题
    return userAnswers.value[index]?.correct === false;
  } else {
    // 大题
    let wrong = false;
    if (userAnswers.value[index]) {
      Object.values(userAnswers.value[index]).forEach((item) => {
        if (item.correct === false) {
          wrong = true;
        }
      });
      return wrong;
    }
    return false;
  }
};

// 子问题答案包含某选项
const answerIncludeKey = (key,index) => {
  return currentQuestion.value.sub_questions[index[index.length - 1] - 1].answer.includes(key)
}

// 判断是否显示正确答案 （以下三个条件分别是：已提交、答案包含该选项、用户没有选择该选项）
const shouldShowCorrectAnswer = (key, index = currentIndex.value) => {
  if (!userAnswers.value[currentIndex.value]) return false;

  if (index === currentIndex.value) {
    return submitted.value && currentQuestion.value.answer.includes(key) && !isSelected(key);
  } else {
    return submitted.value && answerIncludeKey(key,index) && !isSelected(key,index);
  }
};

// 判断是否显示错误样式 （已提交、用户选择该选项、答案不包含该选项）
const shouldShowWrongCss = (key, index = currentIndex.value) => {
  if (!userAnswers.value[currentIndex.value]) return false;

  if (index === currentIndex.value) {
    return submitted.value && isSelected(key) && !currentQuestion.value.answer.includes(key);
  } else {
    return submitted.value && isSelected(key,index) && !answerIncludeKey(key,index);
  }
};

// 判断当前题目是否正确
const isCorrect = (index = currentIndex.value) => {
  if (!userAnswers.value[currentIndex.value]) return false;

  let answerData;
  if (index === currentIndex.value) {
    answerData = userAnswers.value[currentIndex.value];
  } else {
    answerData = userAnswers.value[currentIndex.value][index];
  }
  return answerData ? answerData.correct : null;
};

// 检查用户答案正误
const checkUserAnswer = (question) => {
  const correctSet = new Set(question.answer);
  let selectedKeys;
  if (question.type === "multiple") {
    selectedKeys = [];
    for (let i = 0; i < selectedOptions.value[question.id].length; i++) {
      selectedKeys.push(Object.keys(question.options).find(key => question.options[key] === selectedOptions.value[question.id][i]));
    }
  } else if (question.type === "single") {
    selectedKeys = Object.keys(question.options).find(key => question.options[key] === selectedOptions.value[question.id].toString());
  }
  const selectedSet = new Set(selectedKeys);

  // 判断正误（选择的都是对的，对的全部被选择）
  const isCorrect = [...selectedSet].every(ans => correctSet.has(ans)) &&
      [...correctSet].every(ans => selectedSet.has(ans));

  return {selectedKeys, isCorrect};
}

// 提交答案
const submitAnswer = () => {
  if (submitted.value) return; // 防止重复提交

  if (currentQuestion.value.sub_questions) {
    // 处理大题带小题
    userAnswers.value[currentIndex.value] = {};
    // 统计做题数，若小于题目数，给出提示并拒绝提交
    let answerCount = 0;
    Object.keys(selectedOptions.value).forEach((key) => {
      if (key.startsWith(currentIndex.value + 1) && selectedOptions.value[key].length > 0) {
        answerCount++;
      }
    });
    if (answerCount !== currentQuestion.value.sub_questions.length) {
      dialogVisible.value = true;
      return;
    }
    currentQuestion.value.sub_questions.forEach((subQ) => {
      const {selectedKeys, isCorrect} = checkUserAnswer(subQ)
      userAnswers.value[currentIndex.value][subQ.id] = {
        selected: [...selectedKeys], // 记录选项
        correct: isCorrect, // 记录对错
      }
    })
  } else {
    // 处理单题
    const {selectedKeys, isCorrect} = checkUserAnswer(currentQuestion.value);

    // 记录答案（防止被 reset 清除）
    userAnswers.value[currentIndex.value] = {
      selected: [...selectedKeys], // 记录选项
      correct: isCorrect, // 记录对错
    };
  }
  console.log(userAnswers.value)
  submitted.value = true;
  displayExplanation();
};

// 显示解析动画
const displayExplanation = () => {
  gsap.timeline()
      .set('.explanation', { display: 'block', opacity: 0, transform: 'translateY(10px)' })
      .to('.explanation', { opacity: 1, transform: 'translateY(0)', duration: 0.5 });
}

// 下一题
const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++;
    reset();
  }
}

// 上一题
const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
    reset();
  }
}

// 下一页
const nextPage = () => {
  if ((currentPage.value + 1) * 10 < questions.value.length) {
    currentPage.value++;
  }
}

// 上一页
const prevPage = () => {
  if (currentPage.value > 0) {
    currentPage.value--;
  }
}

// 重置状态（切换题目时）
const reset = () => {
  if (currentQuestion.value.sub_questions) {
    submitted.value = false;
    const prevAnswers = userAnswers.value[currentIndex.value] || {};
    let hasAnswered = true;
    let selectedKeys = {};

    currentQuestion.value.sub_questions.forEach((subQ) => {
      if (prevAnswers[subQ.id]) {
        // 获取键名
        selectedKeys[subQ.id] = [...prevAnswers[subQ.id].selected];
        // 利用子问题 id 最后一位即子问题题号来查找具体子问题
        let currentSubQ = currentQuestion.value.sub_questions[subQ.id[subQ.id.length - 1] - 1];
        // 获取选项对象
        let currentOptions = currentSubQ.options;

        if (subQ.type === "multiple") {
          // 多选则遍历选项列表并添加
          selectedOptions.value[subQ.id] = [];
          selectedKeys[subQ.id].forEach((key) => {
            selectedOptions.value[subQ.id].push(currentOptions[key]);
          })
        } else if (subQ.type === "single") {
          // 单选则获取选项列表的第一个
          selectedOptions.value[subQ.id] = currentOptions[selectedKeys[subQ.id][0]];
        }
      } else if (subQ.type === "multiple") {
        selectedOptions.value[subQ.id] = [];
        hasAnswered = false;
      } else {
        selectedOptions.value[subQ.id] = '';
        hasAnswered = false;
      }
    });
    if (hasAnswered) {
      submitted.value = true;
      requestAnimationFrame(displayExplanation);
    } else {
      submitted.value = false;
      gsap.set('.explanation', { display: 'none' });
    }
  } else {
    const prevAnswer = userAnswers.value[currentIndex.value];

    if (prevAnswer) {
      // 如果已经作答，恢复选项 & 解析
      if (currentQuestion.value.type === "multiple") {
        selectedOptions.value[currentQuestion.value.id] = [];
        for (let i = 0 ; i < prevAnswer.selected.length; i++) {
          selectedOptions.value[currentQuestion.value.id].push(currentQuestion.value.options[prevAnswer.selected[i]]);
        }
      } else {
       selectedOptions.value[currentQuestion.value.id] = currentQuestion.value.options[prevAnswer.selected[0]];
      }
      submitted.value = true;
      requestAnimationFrame(displayExplanation);
    } else if (currentQuestion.value.type === "multiple") {
      // 否则清空
      selectedOptions.value[currentQuestion.value.id] = [];
      submitted.value = false;
      gsap.set('.explanation', { display: 'none' });
    } else {
      selectedOptions.value[currentQuestion.value.id] = '';
      submitted.value = false;
      gsap.set('.explanation', { display: 'none' });
    }
  }
};

// 放大图片
const openImage = (imageURL) => {

}

// 关闭对话框
const handleClose = (done) => {
  ElMessageBox.confirm('要记得做完题目哟！')
      .then(() => {
        done()
      })
      .catch(() => {
        console.log('对话框组件出现错误')
      })
}

onMounted(() => {
  reset();
})
</script>

<style scoped>
/* 外层容器 */
.question-display {
  position: absolute;
  top: 10%;
  left: 16.5%;
  width: 80%;
  height: 85%;
  margin: auto;
  text-align: center;
  overflow-y: auto;
}

/* 题号导航栏 */
.question-nav {
  position: sticky;
  top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 20px;
  gap: 10px; /* 题号间距 */
  z-index: 2;
}

/* 通用小球样式 */
.question-nav button {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: none;
  background: radial-gradient(circle at 35% 25%, #ffffff 10%, #cccccc 40%, #999999 100%);
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: inset 2px 2px 5px rgba(255, 255, 255, 0.6), /* 内部高光 */
  inset -2px -2px 5px rgba(0, 0, 0, 0.2), /* 内部暗部 */
  2px 2px 6px rgba(0, 0, 0, 0.3); /* 外部阴影 */
  font-weight: bold;
  font-size: 16px;
  color: #444;
  text-shadow: 1px 2px 3px rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  line-height: 1;
  transform: translateY(-1px); /* 让数字略微上移，使光照更自然 */
}

/* 悬停时放大 */
.question-nav button:hover {
  background: radial-gradient(circle at 30% 20%, #ffffff 5%, #dddddd 50%, #aaaaaa 100%);
  box-shadow: inset 3px 3px 6px rgba(255, 255, 255, 0.8),
  inset -3px -3px 6px rgba(0, 0, 0, 0.25),
  3px 3px 8px rgba(0, 0, 0, 0.4);
  transform: scale(1.1);
}

/* 答对的题目 - 绿色 */
.question-nav button.correct {
  background: radial-gradient(circle at 30% 20%, #b6f5c6 5%, #4CAF50 50%, #2E7D32 100%);
  box-shadow: inset 3px 3px 6px rgba(255, 255, 255, 0.6),
  inset -3px -3px 6px rgba(0, 0, 0, 0.3),
  3px 3px 10px rgba(76, 175, 80, 0.5);
  color: white;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.4);
}

/* 答错的题目 - 红色 */
.question-nav button.wrong {
  background: radial-gradient(circle at 30% 20%, #ffb3b3 5%, #E53935 50%, #B71C1C 100%);
  box-shadow: inset 3px 3px 6px rgba(255, 255, 255, 0.6),
  inset -3px -3px 6px rgba(0, 0, 0, 0.3),
  3px 3px 10px rgba(229, 57, 53, 0.5);
  color: white;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.4);
}

/* 选中题目 */
.question-nav button.active {
  background: radial-gradient(circle at 30% 20%, #ffcc00 5%, #ffaa00 50%, #cc8800 100%);
  box-shadow: inset 3px 3px 6px rgba(255, 255, 255, 0.6),
  inset -3px -3px 6px rgba(0, 0, 0, 0.3),
  3px 3px 10px rgba(255, 170, 0, 0.5);
  color: white;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.4);
}

/* 题目容器 */
.question {
  display: flex;
  flex-direction: column;
  margin: 20px auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 题目文本 */
.question h3 {
  font-size: 20px;
  font-weight: bold;
  line-height: 1.6;
  color: #333;
  margin-bottom: 15px;
  text-align: left;
  display: flex;
  align-items: flex-start;
}

/* 题目编号 */
.question h3::before {
  content: "Q.";
  font-size: 22px;
  font-weight: bold;
  color: #2E7D32; /* 绿色编号 */
  margin-right: 10px;
}

/* 小题文本 */
.question h4 {
  font-size: 16px;
  font-weight: bold;
  line-height: 1.6;
  color: #333;
  margin-bottom: 15px;
  text-align: left;
  display: flex;
  white-space: pre-wrap;
}

/* 题目图片 */
.question img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s;
}

/* 悬停放大 */
.question img:hover {
  transform: scale(1.05);
  box-shadow: 4px 8px 12px rgba(0, 0, 0, 0.3);
}

/* 单选/多选容器 */
.radio-group,.checkbox-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}

/* 让所有的单选/多选框都变成圆角方框 */
:deep(.el-radio-button__inner) {
  border-radius: 5px !important;
}
:deep(.el-checkbox-button__inner) {
  border-radius: 5px !important;
  outline: none;
}

/* 被禁用且没有被选中（单选 + 多选） */
:deep(.el-radio.is-disabled:not(.is-checked) .el-radio__label) {
  color: #6d6969;
}
:deep(.el-checkbox.is-disabled:not(.is-checked) .el-checkbox__label) {
  color: #6d6969;
}

/* 没禁用也没被选中（单选 + 多选） */
:deep(.el-radio:not(.is-checked):not(.is-disabled) .el-radio__label) {
  color: #0d0f1a;
}
:deep(.el-checkbox:not(.is-checked):not(.is-disabled) .el-checkbox__label) {
  color: #0d0f1a;
}

/* 单选设置 */
.radio-option {
  margin: 0 2em;
  padding: 0 10px;
  width: auto;
  border-radius: 10px;
}

/* 正确答案（选中 + 禁用） */
.el-radio.is-checked.is-disabled {
  background-color: #d4edda !important;
  border-color: #28a745 !important;
  border: 1px solid;
  transition: all 0.15s linear;
}
/* 文本颜色（选中 + 禁用） */
:deep(.el-radio.is-checked.is-disabled .el-radio__label) {
  color: #155724 !important;
  font-weight: bold;
}
/* 单选框圆圈 + 小圆点（选中 + 禁用） */
:deep(.el-radio.is-checked.is-disabled .el-radio__inner) {
  background-color: #28a745 !important;
  border-color: #28a745 !important;
}
:deep(.el-radio.is-checked.is-disabled .el-radio__inner::after) {
  transform: translate( -50%, -50%);
  background-color: #d4edda !important;
}

/* 错误答案 （选中 + 禁用） */
.el-radio.is-checked.is-disabled.wrong-answer {
  background-color: #f8d7da !important;
  border-color: #dc3545 !important;
  font-weight: bold;
  border: 1px solid;
}
/* 文本颜色（选中 + 禁用） */
:deep(.el-radio.is-checked.is-disabled.wrong-answer .el-radio__label) {
  color: #721c24 !important;
  font-weight: bold;
}
/* 单选框圆圈 + 小圆点（选中 + 禁用） */
:deep(.el-radio.is-checked.is-disabled.wrong-answer .el-radio__inner) {
  background-color: #dc3545 !important;
  border-color: #dc3545 !important;
}
:deep(.el-radio.is-checked.is-disabled.wrong-answer .el-radio__inner::after) {
  background-color: #f8d7da !important;
}


/* 多选框设置 */
:deep(.checkbox-option) {
  margin: 0 2em;
  padding: 0 10px;
  width: auto;
  border-radius: 5px;
}

/* 对勾 */
:deep(.el-checkbox__inner::after) {
  transform: rotate(45deg);
  height: 8px !important;
  border-width: 2px !important;
}
:deep(.el-checkbox.is-disabled:not(.is-checked) .el-checkbox__inner::after) {
  opacity: 0; /* 隐藏被禁用且未选中的对勾 */
}

/* 正确答案（选中 + 禁用） */
.el-checkbox.is-checked.is-disabled {
  background-color: #d4edda !important;
  border-color: #28a745 !important;
  font-weight: bold;
  border: 1px solid;
  transition: all 0.15s linear;
}
/* 文本颜色（选中 + 禁用） */
:deep(.el-checkbox.is-checked.is-disabled .el-checkbox__label) {
  color: #155724 !important;
  font-weight: bold;
}
/* 多选框方框（选中 + 禁用） */
:deep(.el-checkbox.is-checked.is-disabled .el-checkbox__inner) {
  background-color: #28a745 !important;
  border-color: #28a745 !important;
}
/* 多选框内的对勾 */
:deep(.el-checkbox.is-checked.is-disabled .el-checkbox__inner::after) {
  border-color: #fff !important;
}

/* 错误答案（选中 + 禁用） */
.el-checkbox.is-checked.is-disabled.wrong-answer {
  background-color: #f8d7da !important;
  border-color: #dc3545 !important;
  font-weight: bold;
  border: 1px solid;
}
/* 文本颜色（选中 + 禁用） */
:deep(.el-checkbox.is-checked.is-disabled.wrong-answer .el-checkbox__label) {
  color: #721c24 !important;
  font-weight: bold;
}
/* 复选框方框（选中 + 禁用） */
:deep(.el-checkbox.is-checked.is-disabled.wrong-answer .el-checkbox__inner) {
  background-color: #dc3545 !important;
  border-color: #dc3545 !important;
}
/* 复选框内的对勾 */
:deep(.el-checkbox.is-checked.is-disabled.wrong-answer .el-checkbox__inner::after) {
  border-color: #fff !important;
}


/* 按钮区按钮 */
.buttons {
  margin: 10px;
  padding: 5px 10px;
}

/* 解释文字整体样式 */
.explanation {
  margin-top: 20px;
  padding: 15px 20px;
  border-radius: 8px;
  background: linear-gradient(to right, #f9f9f9, #ffffff);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  opacity: 0;
  display: none;
  text-align: left;
}

/* 回答正确 */
.explanation-correct {
  font-size: 18px;
  font-weight: bold;
  color: #2E7D32; /* 绿色 */
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 正确答案（回答错误后显示） */
.explanation-wrong {
  font-size: 18px;
  font-weight: bold;
  color: #D32F2F; /* 红色 */
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 解析内容 */
.explanation p:last-child {
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  border-top: 1px solid #ddd;
  margin-top: 10px;
  padding-top: 10px;
}

/* ✅ / ❌ 图标 */
.explanation-correct::before {
  content: "✅";
  font-size: 20px;
  color: #2E7D32;
}

.explanation-wrong::before {
  content: "❌";
  font-size: 20px;
  color: #D32F2F;
}

.pagination {
  margin-top: 20px;
}

.unfinished-prompt {
  text-align: left;
}
</style>